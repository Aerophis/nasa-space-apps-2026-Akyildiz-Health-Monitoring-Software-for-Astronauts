"""AstroCare AI Streamlit entry point."""

import pandas as pd
import streamlit as st
from datetime import date
from textwrap import dedent

from astrocare.analysis import analyze_daily, compare_periods
from astrocare.charts import METRIC_LABELS, trend_chart
from astrocare.data import generate_demo_data, prepare_daily_data, manual_form_record, validate_health_record
from astrocare.storage import load_records, save_record, StorageError
from astrocare.research_ui import render_research_explorer
from astrocare.science import explanation_cards


def display_value(value, metric):
    if pd.isna(value):
        return "No data"
    if metric == "sleep_minutes":
        minutes = round(value)
        return f"{minutes // 60} h {minutes % 60:02d} min"
    unit = "bpm" if metric == "resting_hr_bpm" else "min"
    return f"{value:.1f} {unit}"


def record_form(manual):
    with st.expander("Add a fictional manual health record"):
        st.caption("Enter invented measurements for DEMO-MANUAL-001 only. Do not enter real health or identifying information. A blank field is missing data; 0 is an explicit zero measurement.")
        with st.form("manual_record", clear_on_submit=False):
            measured = st.date_input("Measurement date (UTC day)", value=date(2026, 11, 15),
                                     min_value=date(2000, 1, 1), max_value=date(2100, 12, 31), key="record_date")
            sleep = st.text_input("Sleep duration (minutes)", key="sleep_input", help="0–1440; may be left blank.")
            hr = st.text_input("Resting heart rate (bpm)", key="hr_input", help="A positive finite number; this is not a check against a clinical reference range.")
            activity = st.text_input("Activity duration (minutes)", key="activity_input", help="0–1440; a blank field is not converted to zero.")
            resting = st.checkbox("This fictional heart rate record represents resting conditions", key="rest_confirmed")
            submitted = st.form_submit_button("Save demo record")
        if submitted:
            candidate = manual_form_record(measured, sleep, hr, activity, resting)
            result = validate_health_record(candidate, manual.measured_at)
            if not result.ok:
                for error in result.errors:
                    st.error(error)
                return
            try:
                saved = save_record(candidate)
            except StorageError as exc:
                st.error(str(exc))
                return
            st.session_state["saved_notice"] = saved.warnings
            st.session_state["pending_dataset"] = "Manual demo"
            st.rerun()


def main():
    st.set_page_config(page_title="AstroCare AI | AKYILDIZ", page_icon="✦", layout="wide")
    st.markdown("""<style>
    .stApp {background: radial-gradient(ellipse at top left, #152844, #080f1e 65%); color: #eef4ff;}
    [data-testid="stSidebar"] {background: #101c30;}
    [data-testid="stMetric"] {background: #14243b; border: 1px solid #344b68;
        border-radius: 12px; padding: 18px;}
    </style>""", unsafe_allow_html=True)
    st.caption("AKYILDIZ  /  MISSION HEALTH MONITORING RESEARCH PROTOTYPE  /  SPRINT 3")
    st.title("✦ AstroCare AI")
    st.write("Explore daily measurements and track changes over time.")
    st.caption("This prototype does not provide diagnoses, medical risk scores, or medication advice. It is not NASA-approved. This version does not run an AI model.")
    workspace = st.radio("Workspace", ["Health dashboard", "NASA Research Data Explorer"], horizontal=True, key="workspace")
    if workspace == "NASA Research Data Explorer":
        render_research_explorer()
        return
    st.warning("DEMO — SIMULATED DATA · All measurements in the health dashboard are fictional; they are not real NASA or astronaut health data.")
    if "pending_dataset" in st.session_state:
        st.session_state["dataset"] = st.session_state.pop("pending_dataset")
    dataset = st.selectbox("Data source", ["Generated demo", "Manual demo"], key="dataset")
    st.caption("SIMULATED HEALTH TELEMETRY" if dataset == "Generated demo" else "MANUALLY ENTERED DEMO DATA")
    if "saved_notice" in st.session_state:
        st.success("The fictional record was saved to the local SQLite database; Manual demo is now selected.")
        for warning in st.session_state.pop("saved_notice"):
            st.warning(warning)
    try:
        manual = load_records()
    except StorageError as exc:
        st.error(str(exc))
        manual = pd.DataFrame(columns=["measured_at"])
    record_form(manual)
    if dataset == "Manual demo" and manual.empty:
        st.info("No manual demo records are available, or the database could not be read. Add a fictional record using the form. The generated 21-day demo remains separate.")
        return
    try:
        daily, notices = prepare_daily_data(generate_demo_data() if dataset == "Generated demo" else manual)
        analyzed = analyze_daily(daily)
    except ValueError as exc:
        st.error(f"Could not prepare the data: {exc}")
        st.stop()
    for notice in notices:
        st.warning(notice)

    with st.sidebar:
        st.header("Demo crew profile")
        st.subheader("Deniz Yıldız" if dataset == "Generated demo" else "Manual demo profile")
        st.write("Fictional astronaut · " + str(daily.subject_id.iloc[0]))
        st.caption(f"Source: {daily.source_type.iloc[0]}\n\nAll data are synthetic/fictional. Generated and manual records are not combined.")
        selected = st.selectbox("Review date", list(analyzed.index.date), index=len(analyzed) - 1)
        window = st.radio("Chart range", [7, 14, 21], index=2, format_func=lambda n: f"Last {n} days")
        if dataset == "Generated demo":
            st.caption("Fixed demo period: 25 October – 14 November 2026. Measurements do not change when the page is refreshed.")
        else:
            st.caption("Manual records persist in a local SQLite database. A second record for the same date is rejected; editing and deletion are not supported.")

    endpoint = pd.Timestamp(selected)
    row = analyzed.loc[endpoint]
    shown = analyzed.loc[endpoint - pd.Timedelta(days=window - 1):endpoint]
    st.subheader(f"Daily overview · {endpoint:%d.%m.%Y}")
    for column, (metric, (label, unit, _)) in zip(st.columns(3), METRIC_LABELS.items()):
        with column:
            delta = row[f"{metric}_delta"]
            if metric == "resting_hr_bpm" and dataset == "Manual demo":
                previous_date = endpoint - pd.Timedelta(days=1)
                comparable = (row.rest_state == "confirmed" and previous_date in daily.index
                              and daily.loc[previous_date, "rest_state"] == "confirmed")
                if not comparable:
                    delta = float("nan")
            st.metric(label, display_value(row[metric], metric),
                      delta=f"{delta:+.1f} {unit}" if pd.notna(delta) else None,
                      delta_color="off")
            st.caption("Change from the previous calendar day" if pd.notna(delta) else "Insufficient data for a previous-day comparison.")
            count = int(row[f"{metric}_count7"])
            st.write("7-day average: " + display_value(row[f"{metric}_mean7"], metric))
            st.caption(f"{count}/7 valid numeric measurements in the last 7 calendar days; not sensor validation")

    trends, records, research = st.tabs(["Daily trends", "Daily records", "Scientific context and methodology"])
    with trends:
        st.caption(f"DEMO — SIMULATED DATA · Source: {daily.source_type.iloc[0]} · UTC days · missing values are not imputed.")
        st.caption("Dashed line: the average of available measurements over the last 7 calendar days, including the selected day. Missing values are not imputed; the average may include days before the displayed chart range.")
        for metric in METRIC_LABELS:
            st.plotly_chart(trend_chart(shown, metric), width="stretch", key=f"chart_{metric}")
            valid = int(shown[metric].notna().sum())
            invalid = int(shown[f"{metric}_status"].eq("invalid").sum())
            missing = int(shown[f"{metric}_status"].eq("missing").sum())
            st.caption(f"{METRIC_LABELS[metric][0]} · {valid}/{len(shown)} valid; {missing} missing; {invalid} invalid. Missing and invalid values are excluded from the average.")
        st.subheader("Personal demo comparison across separate periods")
        st.caption(f"Baseline: {endpoint - pd.Timedelta(days=13):%d.%m.%Y} – {endpoint - pd.Timedelta(days=7):%d.%m.%Y}; comparison: {endpoint - pd.Timedelta(days=6):%d.%m.%Y} – {endpoint:%d.%m.%Y}. Requiring at least 5 records per period is a demo design choice, not a clinical threshold.")
        for comparison in compare_periods(daily, endpoint):
            st.info(comparison["message"])
            st.caption(comparison["coverage"])
        if dataset == "Manual demo":
            st.caption("The daily heart rate chart shows the entered values. Records without confirmed resting conditions are excluded from period comparisons. Sensor accuracy has not been assessed.")
    with records:
        st.write("Daily measurements for the period displayed in the charts")
        st.dataframe(shown[list(daily.columns)].reset_index(), hide_index=True, width="stretch")
        st.caption("Sleep and activity are in minutes; resting heart rate is in bpm. Dates are processed as UTC calendar days.")
    with research:
        st.subheader("SCIENTIFIC BACKGROUND INFORMATION")
        st.caption("These are source-backed context cards, not clinical assessments. Observations, calculated trends, and prototype rules are explicitly separated.")
        for card in explanation_cards(daily, endpoint, compare_periods(daily, endpoint)):
            with st.expander(METRIC_LABELS[card["metric"]][0] + " — evidence and limits"):
                st.write("**Observed demo data:** " + card["observed"])
                st.write("**Calculated trend:** " + card["calculated"])
                st.caption(card["coverage"])
                st.write("**Prototype design rule:** " + card["design_rule"])
                st.write("**Published research context:** " + card["finding"])
                st.markdown(f"[Source: {card['title']}]({card['url']})")
                st.caption("Limitation: " + card["limitation"])
        st.subheader("Research starting points")
        st.markdown("""
        - [NASA Fatigue Countermeasures Laboratory](https://www.nasa.gov/human-systems-integration-division/human-performance/fatigue-countermeasures-laboratory/): research on sleep and circadian rhythms.
        - [NASA Wearable Tech for Space Station Research](https://www.nasa.gov/humans-in-space/wearable-tech-for-space-station-research/): examples of wearable technology used to study sleep, exercise, and heart health.
        """)
        st.info("These sources provide scientific context. Demo values were not taken from these studies; no clinical thresholds or personalized recommendations were derived. Detailed literature verification remains a team task.")
        st.markdown(dedent("""\
        **Method:** A fixed seed (2026) generates 21 days of synthetic data.
        Daily changes are calculated against the previous calendar day. The 7-day average uses available
        values; missing values are not counted as zero. During the first days, the average
        uses a partial window, and the cards show the observation count.

        **Data quality:** Non-numeric/infinite values and negative durations are excluded.
        Daily durations must be 0–1440 minutes; heart rate must be a positive finite number.
        These are data-format checks, not boundaries between healthy and unhealthy measurements.
        Duplicate dates are rejected. Chart lines have gaps where daily measurements are missing.
        """))
        st.caption("Scientific status: CORRECTIONS REQUIRED. Authentic OSD-575 serum research is available in its separate explorer after local preparation; it is not sleep/heart-rate/activity telemetry. The health dashboard remains entirely fictional. Scientific acceptance and official Resources eligibility remain unresolved.")
    st.caption("AKYILDIZ · AstroCare AI · Descriptive analysis with synthetic data")


if __name__ == "__main__":
    main()
