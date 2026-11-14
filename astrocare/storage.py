"""Local SQLite persistence for fictional manual records only; no new dependencies."""

import os
import sqlite3
from pathlib import Path
from datetime import date

import pandas as pd

from astrocare.data import METRICS, REQUIRED, validate_health_record

COLUMNS = [*REQUIRED, *(f"{m}_unit" for m in METRICS), "rest_state"]


class StorageError(Exception):
    """A readable storage failure that must be displayed instead of crashing."""


def database_path():
    return Path(os.environ.get("ASTROCARE_DB_PATH", Path(__file__).resolve().parents[1] / "local_data" / "astrocare.sqlite3"))


def load_records(path=None):
    path = Path(path) if path is not None else database_path()
    if not path.exists():
        return pd.DataFrame(columns=COLUMNS)
    try:
        with sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True, timeout=5) as connection:
            connection.row_factory = sqlite3.Row
            rows = [dict(row) for row in connection.execute(
                "SELECT " + ", ".join(COLUMNS) + " FROM records ORDER BY measured_at"
            )]
        validated = []
        for row in rows:
            if row["is_synthetic"] != 1:
                raise StorageError("The local database contains unsupported data provenance; the file was not changed.")
            row["is_synthetic"] = True
            result = validate_health_record(row)
            if not result.ok:
                raise StorageError("A local record failed validation; the file was not changed: " + " ".join(result.errors))
            validated.append(result.record)
        return pd.DataFrame(validated, columns=COLUMNS)
    except (sqlite3.Error, OSError, ValueError, TypeError) as exc:
        raise StorageError("The local database could not be read; the file was not changed. Check the path and access permissions.") from exc


def save_record(record, path=None):
    result = validate_health_record(record)
    if not result.ok:
        raise StorageError(" ".join(result.errors))
    path = Path(path) if path is not None else database_path()
    # Refuse to append to an unrecognised or invalid existing database.
    existing = load_records(path)
    candidate = result.record
    dates = [date.fromisoformat(candidate["measured_at"])] + [date.fromisoformat(d) for d in existing.measured_at]
    if (max(dates) - min(dates)).days > 3660:
        raise StorageError("The record date range cannot exceed 3660 days; no record was added.")
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(path, timeout=5) as connection:
            connection.execute("BEGIN IMMEDIATE")
            connection.execute("""CREATE TABLE IF NOT EXISTS records (
                subject_id TEXT NOT NULL CHECK(subject_id='DEMO-MANUAL-001'),
                measured_at TEXT NOT NULL,
                sleep_minutes REAL CHECK(sleep_minutes BETWEEN 0 AND 1440),
                resting_hr_bpm REAL CHECK(resting_hr_bpm > 0),
                activity_minutes REAL CHECK(activity_minutes BETWEEN 0 AND 1440),
                is_synthetic INTEGER NOT NULL CHECK(is_synthetic=1),
                source_type TEXT NOT NULL CHECK(source_type='manual_demo'),
                sleep_minutes_unit TEXT NOT NULL CHECK(sleep_minutes_unit='minute'),
                resting_hr_bpm_unit TEXT NOT NULL CHECK(resting_hr_bpm_unit='bpm'),
                activity_minutes_unit TEXT NOT NULL CHECK(activity_minutes_unit='minute'),
                rest_state TEXT NOT NULL CHECK(rest_state IN ('confirmed','unspecified')),
                PRIMARY KEY(subject_id, measured_at)
            )""")
            # Recheck under the write lock; simultaneous clients cannot bypass
            # the calendar-span bound between validation and insertion.
            bounds = connection.execute("SELECT MIN(measured_at), MAX(measured_at) FROM records").fetchone()
            locked_dates = [date.fromisoformat(candidate["measured_at"])]
            locked_dates.extend(date.fromisoformat(d) for d in bounds if d is not None)
            if (max(locked_dates) - min(locked_dates)).days > 3660:
                raise StorageError("The record date range cannot exceed 3660 days; no record was added.")
            values = [int(candidate[c]) if c == "is_synthetic" else candidate[c] for c in COLUMNS]
            connection.execute("INSERT INTO records (" + ", ".join(COLUMNS) + ") VALUES (" +
                               ", ".join("?" for _ in COLUMNS) + ")", values)
    except sqlite3.IntegrityError as exc:
        raise StorageError("A record already exists for this date; the existing record was not changed.") from exc
    except (sqlite3.Error, OSError) as exc:
        raise StorageError("The record could not be saved; check the database path, write permissions, or lock status.") from exc
    return result
