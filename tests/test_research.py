"""Artificial parser fixtures; never used as application fallback or NASA evidence."""

import copy
import hashlib
import json

import pandas as pd
import pytest

from astrocare import acquire_research, research
from astrocare.analysis import analyze_daily, compare_periods
from astrocare.data import METRICS, generate_demo_data, prepare_daily_data


@pytest.fixture
def nasa_fixture(tmp_path, isolated_research_directory, monkeypatch):
    # Values are deliberately invented unit-test inputs, not copied participant data.
    manifest = research.read_manifest()
    columns = ["Sample Name", *research.ANALYTES]
    frame = pd.DataFrame([["C001_serum_L-3", 4.0, 90.0, 140.0, 1.0],
                          ["C001_serum_R+1", 4.1, 91.0, 141.0, 1.1]], columns=columns)
    titles = ["Sample Name", "Source Name", "Factor Value: Spaceflight", "Factor Value: Time",
              "Characteristics: Organism", "Characteristics: Material Type"]
    rows = [{"Sample Name": sample, "Source Name": "C001", "Factor Value: Spaceflight": phase,
             "Factor Value: Time": time, "Characteristics: Organism": "Homo sapiens",
             "Characteristics: Material Type": "Serum", "a100012unit": "day"}
            for sample, phase, time in [("C001_serum_L-3", "Pre-flight", "Launch minus 3"),
                                        ("C001_serum_R+1", "Post-flight", "Return plus 1")]]
    metadata = {"study": {"OSD-575": {"version": 3, "additionalInformation": {
        "samples": {"s_OSD-575-txt": {"header": [{"title": t, "field": t} for t in titles], "raw": rows}}}}}}
    payload = frame.to_csv(index=False).encode()
    meta_bytes = json.dumps(metadata).encode()
    manifest.update(expected_rows=2, expected_columns=columns,
                    sha256=hashlib.sha256(payload).hexdigest(),
                    metadata_sha256=hashlib.sha256(meta_bytes).hexdigest())
    manifest_path = tmp_path / "fixture_manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    monkeypatch.setattr(research, "MANIFEST_PATH", manifest_path)
    root = isolated_research_directory
    root.mkdir()
    (root / manifest["file_name"]).write_bytes(payload)
    (root / "study_metadata.json").write_bytes(meta_bytes)
    receipt = {"dataset_id": "OSD-575", "study_version": 3, "license": "CC0-1.0", "restricted": False,
               "sha256": manifest["sha256"], "metadata_sha256": manifest["metadata_sha256"],
               "download_url": manifest["download_url"], "retrieved_at_utc": "2026-11-14T00:00:00+00:00"}
    (root / "receipt.json").write_text(json.dumps(receipt), encoding="utf-8")
    return root, manifest, payload, metadata


def test_offline_loader_preserves_original_values_units_context_and_provenance(nasa_fixture, monkeypatch):
    monkeypatch.setattr(acquire_research, "fetch_bytes", lambda *args: pytest.fail("Offline loading must not fetch"))
    bundle = research.load_research()
    assert len(bundle.observations) == 8
    selected = bundle.observations.query("sample_name == 'C001_serum_L-3' and analyte == 'Glucose'").iloc[0]
    assert selected.value == 90.0
    assert selected.unit == "mg/dL"
    assert selected.anchor == "Launch"
    assert selected.phase == "Pre-flight"
    assert not bool(selected.is_synthetic)
    assert selected.source_type == "nasa_research"
    assert set(bundle.observations.timepoint) == {"L-3", "R+1"}
    assert not any(m in bundle.observations for m in METRICS)


def test_missing_data_has_no_synthetic_fallback(isolated_research_directory):
    with pytest.raises(research.ResearchError, match="missing"):
        research.load_research()
    assert not isolated_research_directory.exists()


@pytest.mark.parametrize("target", ["csv", "metadata", "receipt"])
def test_tampered_files_are_rejected(nasa_fixture, target):
    root, manifest, _, _ = nasa_fixture
    name = {"csv": manifest["file_name"], "metadata": "study_metadata.json", "receipt": "receipt.json"}[target]
    (root / name).write_bytes(b"invalid replacement")
    with pytest.raises(research.ResearchError):
        research.load_research()


@pytest.mark.parametrize("problem", ["missing_metadata_field", "invalid_license", "receipt_type"])
def test_malformed_manifest_or_receipt_has_readable_error(nasa_fixture, problem):
    root, manifest, _, _ = nasa_fixture
    if problem == "receipt_type":
        (root / "receipt.json").write_text("[]", encoding="utf-8")
    else:
        if problem == "missing_metadata_field":
            manifest.pop("doi")
        else:
            manifest["license"] = "unknown"
        research.MANIFEST_PATH.write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(research.ResearchError):
        research.load_research()


@pytest.mark.parametrize("problem", ["schema", "duplicate", "non_numeric", "infinite", "phase", "time", "unit", "version", "sample", "analyte_unit", "organism"])
def test_parser_rejects_unreviewed_schema_or_context(nasa_fixture, problem):
    _, manifest, payload, metadata = nasa_fixture
    manifest = copy.deepcopy(manifest)
    metadata = copy.deepcopy(metadata)
    frame = pd.read_csv(__import__('io').BytesIO(payload))
    samples = metadata["study"]["OSD-575"]["additionalInformation"]["samples"]["s_OSD-575-txt"]["raw"]
    if problem == "schema":
        frame = frame.drop(columns="Sample Name")
    elif problem == "duplicate":
        frame.loc[1, "Sample Name"] = frame.loc[0, "Sample Name"]
    elif problem in ("non_numeric", "infinite"):
        frame["albumin_value_gram_per_deciliter"] = frame["albumin_value_gram_per_deciliter"].astype(object)
        frame.loc[0, "albumin_value_gram_per_deciliter"] = "bad" if problem == "non_numeric" else float("inf")
    elif problem == "phase":
        samples[0]["Factor Value: Spaceflight"] = "Post-flight"
    elif problem == "time":
        samples[0]["Factor Value: Time"] = "Daily heart rate"
    elif problem == "unit":
        samples[0]["a100012unit"] = "hour"
    elif problem == "version":
        metadata["study"]["OSD-575"]["version"] = 999
    elif problem == "sample":
        samples[0]["Sample Name"] = "another"
    elif problem == "analyte_unit":
        manifest["analytes"][0]["unit"] = "bpm"
    else:
        samples[0]["Characteristics: Organism"] = "Mus musculus"
    with pytest.raises(research.ResearchError):
        research.parse_cmp(frame.to_csv(index=False).encode(), metadata, manifest)


def test_missing_assay_value_not_zero(nasa_fixture):
    _, manifest, payload, metadata = nasa_fixture
    frame = pd.read_csv(__import__('io').BytesIO(payload))
    frame.loc[0, "albumin_value_gram_per_deciliter"] = float("nan")
    result = research.parse_cmp(frame.to_csv(index=False).encode(), metadata, manifest)
    assert pd.isna(result.query("sample_name == 'C001_serum_L-3' and analyte == 'Albumin'").iloc[0].value)


def test_research_cannot_enter_health_pipeline(nasa_fixture):
    from astrocare.charts import trend_chart

    frame = research.load_research().observations.query("analyte == 'Albumin'").copy()
    frame["measured_at"] = pd.date_range("2026-11-01", periods=len(frame))
    for metric in METRICS:
        frame[metric] = 60
    with pytest.raises(ValueError):
        prepare_daily_data(frame)
    with pytest.raises(ValueError):
        analyze_daily(frame)
    with pytest.raises(ValueError):
        compare_periods(frame.set_index("measured_at"), pd.Timestamp("2026-11-02"))
    with pytest.raises(ValueError):
        trend_chart(frame, "sleep_minutes")
    frame["source_type"] = "synthetic_demo"
    with pytest.raises(ValueError):
        analyze_daily(frame)


def test_research_chart_is_samples_not_continuous_telemetry(nasa_fixture):
    frame = research.load_research().observations.query("analyte == 'Albumin'")
    fig = research.research_chart(frame)
    assert list(fig.data[0].x) == ["L-3", "R+1"]
    assert list(fig.data[0].y) == [4.0, 4.1]
    assert fig.data[0].mode == "markers"
    assert fig.layout.yaxis.title.text == "g/dL"
    assert "Not daily telemetry" in fig.layout.annotations[0].text
    assert fig.to_json()
    with pytest.raises(research.ResearchError):
        research.research_chart(research.load_research().observations)
    fake = frame.copy()
    fake["is_synthetic"] = True
    with pytest.raises(research.ResearchError):
        research.research_chart(fake)


def test_existing_acquisition_is_offline_and_non_destructive(nasa_fixture, monkeypatch):
    root, manifest, payload, _ = nasa_fixture
    monkeypatch.setattr(acquire_research, "fetch_bytes", lambda *a: pytest.fail("Already acquired"))
    assert len(acquire_research.acquire().observations) == 8
    assert (root / manifest["file_name"]).read_bytes() == payload


def test_research_workspace_displays_loaded_samples_and_source_metadata(nasa_fixture):
    from pathlib import Path
    from streamlit.testing.v1 import AppTest

    app = AppTest.from_file(Path(__file__).resolve().parents[1] / "app.py").run(timeout=30)
    app.radio(key="workspace").set_value("NASA Research Data Explorer").run(timeout=30)
    assert not app.exception
    assert any("AUTHENTIC NASA RESEARCH DATA" in message.value for message in app.success)
    assert len(app.get("plotly_chart")) == 1
    assert len(app.dataframe[0].value) == 2
    assert app.dataframe[0].value.iloc[0].value == 4.0
    app.selectbox(key="research_analyte").select("Glucose").run(timeout=30)
    assert not app.exception
    assert app.dataframe[0].value.iloc[0].value == 90.0
    assert app.dataframe[0].value.unit.eq("mg/dL").all()
    assert any("CORRECTIONS REQUIRED" in c.value for c in app.caption)


def test_acquisition_writes_new_local_files_from_verified_responses(nasa_fixture, tmp_path, monkeypatch):
    _, manifest, payload, metadata = nasa_fixture
    root = tmp_path / "fresh-research"
    monkeypatch.setenv("ASTROCARE_RESEARCH_DIR", str(root))
    listing = {"studies": {"OSD-575": {"study_files": [{"file_name": manifest["file_name"],
               "restricted": False, "remote_url": manifest["download_url"].removeprefix("https://osdr.nasa.gov")} ]}}}
    responses = {manifest["files_api"]: json.dumps(listing).encode(),
                 manifest["download_url"]: payload, manifest["metadata_api"]: json.dumps(metadata).encode()}
    monkeypatch.setattr(acquire_research, "fetch_bytes", lambda url: responses[url])
    assert len(acquire_research.acquire().observations) == 8
    assert (root / manifest["file_name"]).read_bytes() == payload
    assert json.loads((root / "receipt.json").read_text())["restricted"] is False


@pytest.mark.parametrize("problem", ["restricted", "changed_url", "changed_bytes", "network"])
def test_failed_acquisition_does_not_manufacture_data(nasa_fixture, tmp_path, monkeypatch, problem):
    _, manifest, _, _ = nasa_fixture
    root = tmp_path / "failed-research"
    monkeypatch.setenv("ASTROCARE_RESEARCH_DIR", str(root))
    entry = {"file_name": manifest["file_name"], "restricted": problem == "restricted",
             "remote_url": "/wrong" if problem == "changed_url" else manifest["download_url"].removeprefix("https://osdr.nasa.gov")}
    def fetch(url):
        if problem == "network":
            raise research.ResearchError("Network unavailable")
        return json.dumps({"studies": {"OSD-575": {"study_files": [entry]}}}).encode() if url == manifest["files_api"] else b"wrong bytes"
    monkeypatch.setattr(acquire_research, "fetch_bytes", fetch)
    with pytest.raises(research.ResearchError):
        acquire_research.acquire()
    assert not root.exists()
