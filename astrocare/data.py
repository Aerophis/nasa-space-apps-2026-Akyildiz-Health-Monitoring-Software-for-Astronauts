"""Reproducible demo data. No real astronaut records are used."""

from random import Random
from datetime import date, datetime
from math import isfinite, isnan
from numbers import Real
from dataclasses import dataclass, field

import pandas as pd

METRICS = ("sleep_minutes", "resting_hr_bpm", "activity_minutes")
REQUIRED = ("subject_id", "measured_at", *METRICS, "is_synthetic", "source_type")


def generate_demo_data(days: int = 21, seed: int = 2026) -> pd.DataFrame:
    """One daily record per fictional subject; dates and seed are fixed."""
    if not 14 <= days <= 365:
        raise ValueError("The demo period must be between 14 and 365 days.")
    rng = Random(seed)
    dates = pd.date_range(end="2026-11-14", periods=days, freq="D")
    return pd.DataFrame([
        {
            "subject_id": "DEMO-001",
            "measured_at": date,
            "sleep_minutes": rng.randint(385, 480),
            "resting_hr_bpm": rng.randint(58, 70),
            "activity_minutes": rng.randint(65, 125),
            "is_synthetic": True,
            "source_type": "synthetic_demo",
        }
        for date in dates
    ])


def prepare_daily_data(raw: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Validate a single synthetic subject, insert missing calendar dates.

    Invalid metric cells become NaN, never zero. Duplicate dates are rejected
    rather than silently combining potentially conflicting measurements.
    Bounds below are data-format constraints, not clinical reference ranges.
    """
    missing = set(REQUIRED) - set(raw.columns)
    if missing:
        raise ValueError("Missing fields: " + ", ".join(sorted(missing)))
    if raw.empty:
        raise ValueError("No data to display.")
    df = raw.copy()
    if df["subject_id"].isna().any() or df["subject_id"].nunique() != 1:
        raise ValueError("Records for a single astronaut are required.")
    if (not df["is_synthetic"].eq(True).all()
            or not df["source_type"].isin(["synthetic_demo", "manual_demo"]).all()
            or df["source_type"].nunique() != 1):
        raise ValueError("This version accepts only explicitly labeled synthetic demo data.")
    notices = []
    df["measured_at"] = pd.to_datetime(df["measured_at"], errors="coerce", utc=True, format="mixed").dt.tz_convert(None).dt.normalize()
    invalid_dates = int(df["measured_at"].isna().sum())
    if invalid_dates:
        notices.append(f"Excluded {invalid_dates} records with invalid dates.")
        df = df.dropna(subset=["measured_at"])
    if df.empty:
        raise ValueError("No records have a valid date.")
    if df["measured_at"].duplicated().any():
        raise ValueError("Multiple records exist for the same day; correct the data source first.")
    if (df["measured_at"].max() - df["measured_at"].min()).days > 3660:
        raise ValueError("The date range is too large for this demo.")
    for metric in METRICS:
        statuses = df[metric].map(lambda value: classify_measurement(value, metric))
        missing_count = int(statuses.eq("missing").sum())
        invalid_count = int(statuses.eq("invalid").sum())
        if missing_count or invalid_count:
            notices.append(f"{metric}: {missing_count} missing and {invalid_count} invalid values were excluded from calculations.")
        df[f"{metric}_status"] = statuses
        df[metric] = pd.to_numeric(df[metric].where(statuses.eq("valid")), errors="coerce").astype(float)
    df = df.set_index("measured_at").sort_index()
    calendar = pd.date_range(df.index.min(), df.index.max(), freq="D", name="measured_at")
    gaps = len(calendar) - len(df)
    subject = df["subject_id"].iloc[0]
    source = df["source_type"].iloc[0]
    if "rest_state" not in df:
        df["rest_state"] = "simulated_rest" if source == "synthetic_demo" else "unspecified"
    df = df.reindex(calendar)
    df["subject_id"] = subject
    df["is_synthetic"] = True
    df["source_type"] = source
    for metric in METRICS:
        df[f"{metric}_status"] = df[f"{metric}_status"].fillna("missing")
    df["rest_state"] = df["rest_state"].fillna("unspecified")
    if gaps:
        notices.append(f"{gaps} missing days were left blank; no values were estimated.")
    return df, notices

def classify_sleep_minutes(value):
    if pd.isna(value):
        return "missing"
    elif value < 0 or value > 1440:
        return "İnvalid"
    else:
        return "Valid"


def _numeric_status(value):
    """Reject booleans, strings and containers before checking missingness."""
    if value is None or value is pd.NA:
        return "missing"
    if isinstance(value, bool) or not isinstance(value, Real):
        return "invalid"
    try:
        if isnan(value):
            return "missing"
        return "valid" if isfinite(value) else "invalid"
    except (OverflowError, TypeError, ValueError):
        return "invalid"


def classify_resting_hr(value):
    """Positive finite bpm only; no clinical upper threshold is invented."""
    status = _numeric_status(value)
    if status != "valid":
        return status
    return "valid" if value > 0 else "invalid"


def classify_activity_minutes(value):
    status = _numeric_status(value)
    if status != "valid":
        return status
    return "valid" if 0 <= value <= 1440 else "invalid"


def classify_measurement(value, metric):
    """Safe adapter preserves the leader's original sleep function unchanged."""
    if metric not in METRICS:
        raise ValueError("Unsupported metric.")
    status = _numeric_status(value)
    if status != "valid":
        return status
    if metric == "sleep_minutes":
        return {"Valid": "valid", "İnvalid": "invalid", "missing": "missing"}[classify_sleep_minutes(value)]
    if metric == "resting_hr_bpm":
        return classify_resting_hr(value)
    if metric == "activity_minutes":
        return classify_activity_minutes(value)
    raise ValueError("Unsupported metric.")


UNITS = {"sleep_minutes": "minute", "resting_hr_bpm": "bpm", "activity_minutes": "minute"}
LABELS = {"sleep_minutes": "Sleep", "resting_hr_bpm": "Resting heart rate", "activity_minutes": "Activity"}
MANUAL_SUBJECT = "DEMO-MANUAL-001"


def parse_record_date(value):
    """Manual records use an unambiguous ISO date or a date/datetime object."""
    if isinstance(value, datetime):
        parsed = pd.to_datetime(value, utc=True).date()
    elif isinstance(value, date):
        parsed = value
    elif isinstance(value, str):
        parsed = date.fromisoformat(value)
        if value != parsed.isoformat():
            raise ValueError("An ISO calendar date is required.")
    else:
        raise ValueError("Unsupported date type.")
    if not 2000 <= parsed.year <= 2100:
        raise ValueError("The demo date must fall within 2000–2100.")
    return parsed.isoformat()


@dataclass
class RecordValidation:
    record: dict | None = None
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    statuses: dict[str, str] = field(default_factory=dict)

    @property
    def ok(self):
        return not self.errors and self.record is not None


def validate_health_record(record, existing_dates=()):
    """Validate a fictional manual record before any persistence.

    Missing metrics may be saved if at least one is valid. Never convert them
    to zero. Daily duplicates are rejected, never overwritten or averaged.
    """
    result = RecordValidation()
    if not isinstance(record, dict):
        result.errors.append("The record must be a dictionary of field names and values.")
        return result
    clean = {}
    try:
        clean["measured_at"] = parse_record_date(record.get("measured_at"))
        if clean["measured_at"] in {parse_record_date(d) for d in existing_dates}:
            result.errors.append("A record already exists for this date; the existing record was not changed.")
    except (ValueError, TypeError, OverflowError):
        result.errors.append("Enter a valid date (YYYY-MM-DD, within 2000–2100).")
    if (not isinstance(record.get("subject_id"), str) or record["subject_id"] != MANUAL_SUBJECT
            or record.get("is_synthetic") is not True
            or not isinstance(record.get("source_type"), str) or record["source_type"] != "manual_demo"):
        result.errors.append("Only fictional manual demo records are accepted; data provenance cannot be changed.")
    for metric in METRICS:
        status = classify_measurement(record.get(metric), metric)
        result.statuses[metric] = status
        unit = record.get(f"{metric}_unit")
        if not isinstance(unit, str) or unit != UNITS[metric]:
            result.errors.append(f"The unit for {LABELS[metric]} must be {UNITS[metric]}.")
        if status == "invalid":
            rule = "a positive finite number" if metric == "resting_hr_bpm" else "a finite number between 0 and 1440"
            result.errors.append(f"{LABELS[metric]}: enter {rule}; text and boolean values are not supported.")
        elif status == "missing":
            result.warnings.append(f"The {LABELS[metric]} measurement is missing; it will not be counted as zero.")
        clean[metric] = float(record[metric]) if status == "valid" else None
        clean[f"{metric}_unit"] = UNITS[metric]
    if not any(status == "valid" for status in result.statuses.values()):
        result.errors.append("Enter at least one valid measurement.")
    rest_state = record.get("rest_state", "unspecified")
    if not isinstance(rest_state, str) or rest_state not in ("confirmed", "unspecified"):
        result.errors.append("Invalid resting-condition label.")
    clean.update(subject_id=MANUAL_SUBJECT, is_synthetic=True, source_type="manual_demo",
                 rest_state=rest_state)
    if not result.errors:
        result.record = clean
    return result


def manual_form_record(measured_at, sleep, resting_hr, activity, resting_confirmed=False):
    """Translate optional text inputs into numeric or intentionally invalid cells."""
    def number(text):
        if isinstance(text, str):
            if not text.strip():
                return None
            try:
                return float(text.strip().replace(",", "."))
            except ValueError:
                return text
        return text

    record = {"measured_at": measured_at, "subject_id": MANUAL_SUBJECT,
              "is_synthetic": True, "source_type": "manual_demo",
              "rest_state": "confirmed" if resting_confirmed else "unspecified"}
    for metric, value in zip(METRICS, (sleep, resting_hr, activity)):
        record[metric] = number(value)
        record[f"{metric}_unit"] = UNITS[metric]
    return record
