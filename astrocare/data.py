"""Reproducible demo data. No real astronaut records are used."""

from random import Random

import pandas as pd

METRICS = ("sleep_minutes", "resting_hr_bpm", "activity_minutes")
REQUIRED = ("subject_id", "measured_at", *METRICS, "is_synthetic", "source_type")


def generate_demo_data(days: int = 21, seed: int = 2026) -> pd.DataFrame:
    """One daily record per fictional subject; dates and seed are fixed."""
    if not 14 <= days <= 365:
        raise ValueError("Demo süresi 14 ile 365 gün arasında olmalı.")
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
        raise ValueError("Eksik alanlar: " + ", ".join(sorted(missing)))
    if raw.empty:
        raise ValueError("Gösterilecek veri yok.")
    df = raw.copy()
    if df["subject_id"].isna().any() or df["subject_id"].nunique() != 1:
        raise ValueError("Tek bir astronota ait kayıtlar bekleniyor.")
    if not df["is_synthetic"].eq(True).all() or not df["source_type"].eq("synthetic_demo").all():
        raise ValueError("Bu sürüm yalnızca işaretlenmiş sentetik demo verisini kabul eder.")
    notices = []
    df["measured_at"] = pd.to_datetime(df["measured_at"], errors="coerce", utc=True, format="mixed").dt.tz_convert(None).dt.normalize()
    invalid_dates = int(df["measured_at"].isna().sum())
    if invalid_dates:
        notices.append(f"Geçersiz tarihli {invalid_dates} kayıt dışlandı.")
        df = df.dropna(subset=["measured_at"])
    if df.empty:
        raise ValueError("Geçerli tarihli kayıt yok.")
    if df["measured_at"].duplicated().any():
        raise ValueError("Aynı güne ait birden fazla kayıt var; önce veri kaynağını düzeltin.")
    if (df["measured_at"].max() - df["measured_at"].min()).days > 3660:
        raise ValueError("Tarih aralığı demo için çok geniş.")
    for metric in METRICS:
        values = pd.to_numeric(df[metric], errors="coerce").astype(float)
        valid = values.notna() & values.ne(float("inf")) & values.ne(-float("inf"))
        valid &= values.ge(0) if metric != "resting_hr_bpm" else values.gt(0)
        if metric != "resting_hr_bpm":
            valid &= values.le(1440)
        count = int((~valid).sum())
        if count:
            notices.append(f"{metric}: {count} eksik/geçersiz değer hesaplamaya alınmadı.")
        df[metric] = values.where(valid)
    df = df.set_index("measured_at").sort_index()
    calendar = pd.date_range(df.index.min(), df.index.max(), freq="D", name="measured_at")
    gaps = len(calendar) - len(df)
    subject = df["subject_id"].iloc[0]
    df = df.reindex(calendar)
    df["subject_id"] = subject
    df["is_synthetic"] = True
    df["source_type"] = "synthetic_demo"
    if gaps:
        notices.append(f"{gaps} eksik gün boş bırakıldı; değer tahmin edilmedi.")
    return df, notices
