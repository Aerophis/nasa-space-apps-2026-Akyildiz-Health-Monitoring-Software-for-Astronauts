"""Artificial parser fixtures; never used as application fallback or NASA evidence."""

import copy
import hashlib
import json
from html import escape
from html.parser import HTMLParser

import pandas as pd
import pytest

from astrocare import acquire_research, research
from astrocare.analysis import analyze_daily, compare_periods
from astrocare.data import METRICS, generate_demo_data, prepare_daily_data


def _comparison_rows(view):
    return [row for phase in view.phases for row in phase.measurements]


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
    view = research.research_chart(frame)
    assert [row.label for row in _comparison_rows(view)] == ["L-3", "R+1"]
    assert [row.value for row in _comparison_rows(view)] == [4.0, 4.1]
    assert view.unit == "g/dL" and view.dataset_id == "OSD-575"
    assert view.valid_count == view.sample_count == 2
    with pytest.raises(research.ResearchError):
        research.research_chart(research.load_research().observations)
    fake = frame.copy()
    fake["is_synthetic"] = True
    with pytest.raises(research.ResearchError):
        research.research_chart(fake)


def test_research_cards_preserve_visit_phase_and_units(nasa_fixture):
    selected = research.load_research().observations.query("analyte == 'Albumin'").sort_values("relative_day")
    view = research.research_chart(selected)
    assert [phase.color for phase in view.phases] == ["#65B8D2", "#E4A17C"]
    assert [row.phase for row in _comparison_rows(view)] == list(selected.phase)
    assert [row.value_label for row in _comparison_rows(view)] == ["4.0", "4.1"]
    assert view.unit == "g/dL"
    assert [row.label for row in _comparison_rows(view)] == list(selected.timepoint)


@pytest.mark.parametrize("language", ["en", "tr", "fr", "de", "es"])
def test_research_language_preserves_values_and_moves_source_to_details(nasa_fixture, language):
    from pathlib import Path
    from streamlit.testing.v1 import AppTest
    from astrocare.i18n import Translator

    app = AppTest.from_file(Path(__file__).resolve().parents[1] / "app.py").run(timeout=30)
    app.radio(key="workspace").set_value("NASA Research Data Explorer").run(timeout=30)
    original = app.dataframe[0].value.copy(deep=True)
    app.selectbox(key="language").select(language).run(timeout=30)
    t = Translator(language)
    assert not app.exception
    header = next(item.value for item in app.markdown if 'data-testid="research-header"' in item.value)
    assert escape(t("verified_data")) in header
    assert escape(t("research_only")) in header
    assert escape(t("research_separation")) in header
    assert not app.success and not app.warning
    assert not app.title
    safety = next(exp for exp in app.expander if exp.label == t("safety"))
    assert any(item.value == t("research_status") for item in safety.caption)
    assert any(item.value == t("prototype") for item in safety.markdown)
    study = next(exp for exp in app.expander if exp.label == t("study_context"))
    assert any(item.value == t("research_limits") for item in study.markdown)
    assert any(item.value == t("serum_timeline") for item in study.caption)
    assert any(item.value == t("counts_note") for item in study.caption)
    pd.testing.assert_frame_equal(app.dataframe[0].value, original)
    details = next(exp for exp in app.expander if exp.label == t("provenance"))
    assert any("CC0-1.0" in item.value and "osdr.nasa.gov" in item.value for item in details.markdown)
    fig = research.research_chart(research.load_research().observations.query("analyte == 'Albumin'"), language)
    assert [row.value for row in _comparison_rows(fig)] == [4.0, 4.1]
    assert fig.unit == "g/dL"
    assert any(item.value == t("serum_timeline") for item in app.caption)
    assert any(item.value == t("timeline_key") for item in app.caption)
    assert any(exp.label == t("view_samples") for exp in app.expander)
    assert list(app.dataframe[0].value.timepoint) == ["L-3", "R+1"]
    html = next(item.value for item in app.markdown if 'data-testid="research-comparison"' in item.value)
    assert t("comparison_available", valid=2, total=2) in html
    assert "Albumin" in html and "C001" in html and "g/dL" in html


@pytest.mark.parametrize("invalid_file", ["csv", "metadata", "receipt", "manifest"])
def test_verified_indicator_is_withdrawn_when_local_integrity_fails(nasa_fixture, invalid_file):
    from pathlib import Path
    from streamlit.testing.v1 import AppTest

    root, manifest, _, _ = nasa_fixture
    app = AppTest.from_file(Path(__file__).resolve().parents[1] / "app.py").run(timeout=30)
    app.radio(key="workspace").set_value("NASA Research Data Explorer").run(timeout=30)
    assert any('data-testid="research-verified"' in item.value for item in app.markdown)
    target = {"csv": root / manifest["file_name"], "metadata": root / "study_metadata.json",
              "receipt": root / "receipt.json", "manifest": research.MANIFEST_PATH}[invalid_file]
    target.write_text("{}", encoding="utf-8")
    app.run(timeout=30)
    assert not app.exception and app.error
    header = next(item.value for item in app.markdown if 'data-testid="research-header"' in item.value)
    assert 'data-testid="research-verified"' not in header
    assert not any('data-testid="research-comparison"' in item.value for item in app.markdown)
    assert any(exp.label == "Safety & Scientific Review" for exp in app.expander)


@pytest.mark.parametrize("language", ["en", "tr", "fr", "de", "es"])
def test_research_phase_cards_context_and_scale_preserve_source_semantics(nasa_fixture, language):
    from astrocare.i18n import Translator
    from astrocare.research_cards import research_cards_html
    from astrocare.theme import COLORS

    frame = research.load_research().observations.query("analyte == 'Albumin'").sort_values("relative_day")
    view = research.research_chart(frame, language)
    t = Translator(language)
    rows = _comparison_rows(view)
    assert len(view.phases) == 2
    assert [row.label for row in rows] == ["L-3", "R+1"]
    assert [row.value for row in rows] == [4.0, 4.1]
    assert [row.context for row in rows] == [t("before_launch", days=3), t("after_return", days=1)]
    assert view.subject_id == "C001" and view.analyte == "Albumin"
    assert view.unit == "g/dL" and view.dataset_id == "OSD-575"
    assert [phase.title for phase in view.phases] == [t("pre_flight"), t("post_flight")]
    assert [phase.color for phase in view.phases] == [COLORS["research"], COLORS["heart"]]
    assert [row.value_label for row in rows] == ["4.0", "4.1"]
    assert view.scale_max > max(frame.value)
    assert [row.fraction for row in rows] == [row.value / view.scale_max for row in rows]
    html = research_cards_html(view)
    assert 'data-testid="research-comparison"' in html
    assert html.count('class="ac-phase"') == 2
    assert html.count('data-scale-max="' + str(view.scale_max) + '"') == 3
    for row, phase in zip(rows, view.phases):
        detail = t("comparison_row_info", subject=view.subject_id, analyte=view.analyte,
                   value=row.value_label, unit=view.unit, point=row.label, phase=phase.title,
                   context=row.context, dataset=view.dataset_id)
        assert escape(detail, quote=True) in html
    assert escape(t("shared_research_scale", maximum=view.scale_label, unit=view.unit)) in html


@pytest.mark.parametrize("value", [None, float("nan"), 0.0])
def test_card_values_preserve_missing_and_explicit_zero(nasa_fixture, value):
    from astrocare.i18n import Translator
    from astrocare.research_cards import research_cards_html

    frame = research.load_research().observations.query("analyte == 'Albumin'").copy()
    frame.loc[frame.timepoint.eq("R+1"), "value"] = value
    original = frame.copy(deep=True)
    view = research.research_chart(frame)
    pd.testing.assert_frame_equal(frame, original)
    row = view.phases[1].measurements[0]
    if pd.isna(value):
        assert row.value is None and row.fraction is None
        assert row.value_label == Translator()("missing_result")
        assert 'data-missing="true"' in research_cards_html(view)
        assert view.valid_count == 1
    else:
        assert row.value == row.fraction == 0
        assert row.value_label == "0.0"
        assert view.valid_count == 2
    assert view.phases[0].measurements[0].value_label == "4.0"


def test_column_groups_reject_unknown_phase_without_silently_dropping_samples(nasa_fixture):
    frame = research.load_research().observations.query("analyte == 'Albumin'").copy()
    frame.loc[frame.timepoint.eq("R+1"), "phase"] = "unknown"
    with pytest.raises(research.ResearchError):
        research.research_chart(frame)


class _CardHTML(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.elements = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        self.elements.append({"tag": tag, **dict(attrs)})

    def by_class(self, name):
        return [element for element in self.elements if name in element.get("class", "").split()]


def test_cards_use_one_global_scale_not_one_scale_per_phase(nasa_fixture):
    from astrocare.research_cards import research_cards_html

    frame = research.load_research().observations.query("analyte == 'Albumin'").copy()
    frame.loc[frame.phase.eq("Post-flight"), "value"] = 40.0
    view = research.research_chart(frame)
    rows = _comparison_rows(view)
    assert rows[0].fraction < .1
    assert rows[1].fraction > .8
    assert rows[0].fraction / rows[1].fraction == pytest.approx(4 / 40)
    parsed = _CardHTML(research_cards_html(view))
    assert [float(panel["data-scale-max"]) for panel in parsed.by_class("ac-phase")] == [view.scale_max] * 2
    fills = parsed.by_class("ac-fill")
    widths = [float(fill["style"].split("width:")[1].split("%")[0]) for fill in fills]
    assert widths == pytest.approx([row.value / view.scale_max * 100 for row in rows])


def test_empty_phase_is_visible_without_inventing_visits(nasa_fixture):
    from astrocare.i18n import Translator
    from astrocare.research_cards import research_cards_html

    frame = research.load_research().observations.query("analyte == 'Albumin' and phase == 'Post-flight'")
    view = research.research_chart(frame)
    assert len(view.phases) == 2
    assert not view.phases[0].measurements
    assert view.sample_count == view.valid_count == 1
    html = research_cards_html(view)
    assert Translator()("no_phase_samples") in html
    assert len(_CardHTML(html).by_class("ac-row")) == 1


@pytest.mark.parametrize("value", [-1.0, float("inf"), -float("inf")])
def test_shared_scale_rejects_unsupported_values_without_clamping(nasa_fixture, value):
    frame = research.load_research().observations.query("analyte == 'Albumin'").copy()
    frame.loc[frame.timepoint.eq("R+1"), "value"] = value
    original = frame.copy(deep=True)
    with pytest.raises(research.ResearchError, match="shared zero-based"):
        research.research_chart(frame)
    pd.testing.assert_frame_equal(frame, original)


def test_card_value_labels_retain_numeric_precision(nasa_fixture):
    from astrocare.research_cards import research_cards_html

    frame = research.load_research().observations.query("analyte == 'Albumin'").copy()
    value = 4.1234567891234
    frame.loc[frame.timepoint.eq("R+1"), "value"] = value
    view = research.research_chart(frame)
    assert view.phases[1].measurements[0].value_label == str(value)
    assert str(value) in research_cards_html(view)


def test_card_renderer_escapes_source_text_in_content_and_attributes(nasa_fixture):
    from dataclasses import replace
    from astrocare.research_cards import research_cards_html

    frame = research.load_research().observations.query("analyte == 'Albumin'")
    view = replace(research.research_chart(frame), subject_id='<img src=x onerror="alert(1)">')
    html = research_cards_html(view)
    assert "<img" not in html
    assert escape(view.subject_id, quote=True) in html
    assert all(element["tag"] != "img" for element in _CardHTML(html).elements)


@pytest.mark.parametrize("language", ["en", "tr", "fr", "de", "es"])
def test_all_missing_results_remain_missing_in_each_language(nasa_fixture, language):
    from astrocare.i18n import Translator
    from astrocare.research_cards import research_cards_html

    frame = research.load_research().observations.query("analyte == 'Albumin'").copy()
    frame["value"] = float("nan")
    view = research.research_chart(frame, language)
    t = Translator(language)
    assert view.scale_max == 1.0 and view.valid_count == 0 and view.sample_count == 2
    assert all(row.value is row.fraction is None for row in _comparison_rows(view))
    html = research_cards_html(view)
    parsed = _CardHTML(html)
    assert not parsed.by_class("ac-fill")
    assert len(parsed.by_class("ac-missing")) == 2
    assert escape(t("missing_result")) in html
    assert escape(t("comparison_available", valid=0, total=2)) in html


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
    header = next(item.value for item in app.markdown if 'data-testid="research-header"' in item.value)
    assert 'data-testid="research-verified"' in header
    assert not app.get("plotly_chart")
    assert any('data-testid="research-comparison"' in item.value for item in app.markdown)
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
