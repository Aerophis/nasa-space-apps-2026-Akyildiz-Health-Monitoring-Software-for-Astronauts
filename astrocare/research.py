"""Read-only, offline OSD-575 CMP explorer. Never produces health telemetry."""

import csv
import hashlib
import io
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go

MANIFEST_PATH = Path(__file__).resolve().parents[1] / "data" / "osd575_manifest.json"
ANALYTES = {
    "albumin_value_gram_per_deciliter": ("Albumin", "g/dL"),
    "glucose_value_milligram_per_deciliter": ("Glucose", "mg/dL"),
    "sodium_value_millimol_per_liter": ("Sodium", "mmol/L"),
    "creatinine_value_milligram_per_deciliter": ("Creatinine", "mg/dL"),
}


class ResearchError(Exception):
    """Actionable dataset error; no simulated replacement is permitted."""


def research_directory():
    return Path(os.environ.get("ASTROCARE_RESEARCH_DIR", Path(__file__).resolve().parents[1] / "research_data" / "OSD-575"))


def read_manifest():
    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        required = {"dataset_id", "title", "license", "file_name", "sha256", "metadata_sha256",
                    "expected_columns", "expected_rows", "analytes", "source_url", "study_version",
                    "doi", "license_url", "origin", "context", "limitations", "download_url",
                    "files_api", "metadata_api", "license_evidence"}
        if not isinstance(manifest, dict) or not required.issubset(manifest) or manifest["dataset_id"] != "OSD-575":
            raise ValueError("Invalid manifest")
        if (manifest["license"] != "CC0-1.0"
                or not isinstance(manifest["expected_rows"], int) or not 1 <= manifest["expected_rows"] <= 1000
                or not isinstance(manifest["expected_columns"], list)
                or not all(isinstance(c, str) for c in manifest["expected_columns"])
                or not all(isinstance(manifest[k], str) and re.fullmatch(r"[0-9a-f]{64}", manifest[k])
                           for k in ("sha256", "metadata_sha256"))):
            raise ValueError("Invalid manifest schema or license")
        _validate_analytes(manifest)
        return manifest
    except (OSError, ValueError, TypeError, KeyError) as exc:
        raise ResearchError("The research manifest is missing or invalid. Restore data/osd575_manifest.json.") from exc


def _validate_analytes(manifest):
    if ({a["column"]: (a["label"], a["unit"]) for a in manifest["analytes"]} != ANALYTES
            or len(manifest["analytes"]) != len(ANALYTES)):
        raise ValueError("Unreviewed analytes or units")


def parse_cmp(payload, metadata, manifest):
    """Keep original sample identifiers, units and distinct launch/return anchors.

    Only four explicitly mapped analytes are selected. Reference ranges and
    demographic/race-based derived fields are not interpreted or displayed.
    """
    try:
        _validate_analytes(manifest)
        text = payload.decode("utf-8-sig")
        header = next(csv.reader(io.StringIO(text)))
        if len(header) != len(set(header)) or header != manifest["expected_columns"]:
            raise ValueError("Unexpected CSV schema")
        frame = pd.read_csv(io.StringIO(text))
        if len(frame) != manifest["expected_rows"] or frame["Sample Name"].isna().any() or frame["Sample Name"].duplicated().any():
            raise ValueError("Invalid sample rows")
        study = metadata["study"]["OSD-575"]
        if study["version"] != manifest["study_version"]:
            raise ValueError("Study version mismatch")
        samples = study["additionalInformation"]["samples"]["s_OSD-575-txt"]
        fields = {h["title"]: h["field"] for h in samples["header"]}
        sample_map = {}
        for row in samples["raw"]:
            sample = row[fields["Sample Name"]]
            if sample in sample_map:
                raise ValueError("Duplicate sample metadata")
            sample_map[sample] = row
        if set(frame["Sample Name"]) != set(sample_map):
            raise ValueError("CSV/metadata sample mismatch")
        records = []
        for _, row in frame.iterrows():
            sample = row["Sample Name"]
            info = sample_map[sample]
            subject = info[fields["Source Name"]]
            phase = info[fields["Factor Value: Spaceflight"]]
            time = info[fields["Factor Value: Time"]]
            match = re.fullmatch(r"(Launch minus|Return plus) (\d+)", time)
            if (not match or subject not in {"C001", "C002", "C003", "C004"}
                    or info[fields["Characteristics: Organism"]] != "Homo sapiens"
                    or info[fields["Characteristics: Material Type"]] != "Serum"
                    or info["a100012unit"] != "day"):
                raise ValueError("Unsupported biospecimen context")
            before = match[1] == "Launch minus"
            day = int(match[2])
            point = ("L-" if before else "R+") + str(day)
            if phase != ("Pre-flight" if before else "Post-flight") or sample != f"{subject}_serum_{point}":
                raise ValueError("Sample context mismatch")
            for analyte in manifest["analytes"]:
                value = row[analyte["column"]]
                if pd.isna(value):
                    value = float("nan")
                else:
                    value = float(value)
                    if not float("-inf") < value < float("inf"):
                        raise ValueError("Non-finite measurement")
                records.append({"sample_name": sample, "subject_id": subject,
                                "phase": phase, "timepoint": point, "sampling_context": time + " days",
                                "relative_day": -day if before else day,
                                "anchor": "Launch" if before else "Return",
                                "analyte": analyte["label"], "original_column": analyte["column"],
                                "value": value, "unit": analyte["unit"],
                                "dataset_id": "OSD-575", "source_type": "nasa_research", "is_synthetic": False})
        return pd.DataFrame(records).sort_values(["subject_id", "analyte", "relative_day"]).reset_index(drop=True)
    except (ValueError, TypeError, KeyError, StopIteration, UnicodeError, pd.errors.ParserError) as exc:
        raise ResearchError("OSD-575 could not be parsed: schema, units, sample context, or numeric values differ from the reviewed format. No replacement data were generated.") from exc


@dataclass
class ResearchBundle:
    observations: pd.DataFrame
    manifest: dict
    receipt: dict


def load_research(directory=None):
    """No network calls, file creation, or merging with synthetic health records."""
    root = Path(directory) if directory is not None else research_directory()
    manifest = read_manifest()
    try:
        payload = (root / manifest["file_name"]).read_bytes()
        metadata_bytes = (root / "study_metadata.json").read_bytes()
        if (hashlib.sha256(payload).hexdigest() != manifest["sha256"]
                or hashlib.sha256(metadata_bytes).hexdigest() != manifest["metadata_sha256"]):
            raise ResearchError("Research file checksum mismatch. The local files are not the reviewed snapshots; no data are displayed.")
        metadata = json.loads(metadata_bytes)
        observations = parse_cmp(payload, metadata, manifest)
        receipt = json.loads((root / "receipt.json").read_text(encoding="utf-8"))
        if not isinstance(receipt, dict):
            raise ValueError("Invalid receipt")
        if (receipt.get("sha256") != manifest["sha256"]
                or receipt.get("metadata_sha256") != manifest["metadata_sha256"]
                or receipt.get("download_url") != manifest["download_url"]
                or receipt.get("dataset_id") != "OSD-575" or receipt.get("license") != manifest["license"]
                or receipt.get("study_version") != manifest["study_version"] or receipt.get("restricted") is not False
                or not receipt.get("retrieved_at_utc")):
            raise ResearchError("The research acquisition receipt is incomplete or inconsistent.")
        return ResearchBundle(observations, manifest, receipt)
    except FileNotFoundError as exc:
        raise ResearchError("The local OSD-575 dataset or receipt is missing. Prepare it with: .\\.venv\\Scripts\\python.exe -m astrocare.acquire_research. No numerical integration is available until preparation succeeds.") from exc
    except (OSError, ValueError, TypeError) as exc:
        raise ResearchError("The local research files cannot be read. Check the acquisition receipt and permissions; original files were not changed.") from exc


def research_chart(observations):
    """Sample markers, not an interpolated daily timeline or clinical threshold."""
    if (observations.empty or not observations.source_type.eq("nasa_research").all()
            or not observations.is_synthetic.eq(False).all()
            or observations.subject_id.nunique() != 1 or observations.analyte.nunique() != 1
            or observations.unit.nunique() != 1):
        raise ResearchError("Select one authentic research subject and analyte; incompatible records cannot be plotted together.")
    data = observations.sort_values("relative_day")
    if (not data.dataset_id.eq("OSD-575").all()
            or (data.analyte.iloc[0], data.unit.iloc[0]) not in ANALYTES.values()):
        raise ResearchError("The analyte/unit mapping is not a reviewed OSD-575 measurement.")
    fig = go.Figure(go.Scatter(x=data.timepoint, y=data.value, mode="markers",
                              marker={"size": 10, "color": "#61d7ff"}, connectgaps=False,
                              hovertemplate="%{x}<br>%{y}<extra>Research sample</extra>"))
    fig.update_layout(title=f"{data.analyte.iloc[0]} · {data.subject_id.iloc[0]} · OSD-575",
                      xaxis={"title": "Scheduled sample (L: launch; R: return)", "type": "category"},
                      yaxis_title=data.unit.iloc[0], template="plotly_dark", height=380,
                      margin={"l": 20, "r": 20, "t": 60, "b": 90})
    fig.add_annotation(text="AUTHENTIC NASA-HOSTED RESEARCH DATA · Serum samples · Not daily telemetry",
                       x=0, y=-0.3, xref="paper", yref="paper", showarrow=False, xanchor="left")
    return fig
