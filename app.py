"""AstroCare AI Streamlit entry point; presentation is localized independently of data."""

from datetime import date

import pandas as pd
import streamlit as st

from astrocare.analysis import analyze_daily, compare_periods
from astrocare.charts import METRIC_LABELS, trend_chart
from astrocare.data import generate_demo_data, prepare_daily_data, manual_form_record, validate_health_record
from astrocare.storage import load_records, save_record, StorageError
from astrocare.research_ui import render_research_explorer
from astrocare.science import explanation_cards
from astrocare.ui import apply_theme, choice_key, localized_choice
from astrocare.i18n import LANGUAGES, Translator

METRIC_TEXT = {"sleep_minutes": "sleep", "resting_hr_bpm": "heart", "activity_minutes": "activity"}
WORKSPACE_TEXT = {"Health dashboard": "health", "NASA Research Data Explorer": "research"}
DATASET_TEXT = {"Generated demo": "generated", "Manual demo": "manual"}


def display_value(value, metric, t=None):
    t = t or Translator()
    if pd.isna(value):
        return t("no_data")
    if metric == "sleep_minutes":
        minutes = round(value)
        return t("duration", hours=minutes // 60, minutes=minutes % 60)
    unit = "bpm" if metric == "resting_hr_bpm" else t("min")
    return f"{value:.1f} {unit}"


def record_form(manual, t=None):
    t = t or Translator()
    with st.expander(t("add_record")):
        st.caption(t("form_help"))
        with st.form("manual_record", clear_on_submit=False):
            measured = st.date_input(t("measurement_date"), value=date(2026, 11, 15),
                                     min_value=date(2000, 1, 1), max_value=date(2100, 12, 31), key="record_date")
            sleep = st.text_input(t("sleep_input"), key="sleep_input", help=t("duration_help"))
            hr = st.text_input(t("hr_input"), key="hr_input", help=t("hr_help"))
            activity = st.text_input(t("activity_input"), key="activity_input", help=t("duration_help"))
            resting = st.checkbox(t("rest_confirmed"), key="rest_confirmed")
            submitted = st.form_submit_button(t("save"))
        if submitted:
            candidate = manual_form_record(measured, sleep, hr, activity, resting)
            result = validate_health_record(candidate, manual.measured_at)
            if not result.ok:
                for error in result.errors:
                    st.error(t.message(error))
                return
            try:
                saved = save_record(candidate)
            except StorageError as exc:
                st.error(t.message(str(exc)))
                return
            st.session_state["saved_notice"] = saved.warnings
            st.session_state["pending_dataset"] = "Manual demo"
            st.rerun()


def main():
    st.set_page_config(page_title="AstroCare AI | AKYILDIZ", page_icon="✦", layout="wide")
    apply_theme()
    identity, locale = st.columns([3, 1])
    with locale:
        previous = Translator(st.session_state.get("language", "en"))
        language = st.selectbox(previous("language"), list(LANGUAGES), format_func=LANGUAGES.get, key="language")
    t = Translator(language)
    research_workspace = st.session_state.get("_selection_workspace") == "NASA Research Data Explorer"
    with identity:
        if research_workspace:
            st.markdown("**AstroCare AI** · AKYILDIZ")
        else:
            st.caption(t("eyebrow"))
            st.title("AstroCare AI")
            st.write(t("tagline"))
    if not research_workspace:
        st.caption(t("prototype"))
    navigation, safety = st.columns([2, 1], vertical_alignment="center")
    with navigation:
        workspace = localized_choice(st.radio, t("workspace"), list(WORKSPACE_TEXT), horizontal=True,
                                     name="workspace", language=language, initial="Health dashboard",
                                     format_func=lambda value: t(WORKSPACE_TEXT[value]))
    with safety:
        with st.expander(t("safety")):
            if workspace == "NASA Research Data Explorer":
                st.caption(t("research_status"))
                st.write(t("prototype"))
            st.write(t("safety_body"))
            st.write(t("separation"))
    if workspace == "NASA Research Data Explorer":
        render_research_explorer(language)
        return
    st.warning(t("demo_warning"))
    if "pending_dataset" in st.session_state:
        pending = st.session_state.pop("pending_dataset")
        st.session_state[choice_key("dataset", language)] = pending
        st.session_state["_selection_dataset"] = pending
    source_control, entry_control = st.columns([1, 2], vertical_alignment="center")
    with source_control:
        dataset = localized_choice(st.selectbox, t("source"), list(DATASET_TEXT), name="dataset",
                                   language=language, initial="Generated demo",
                                   format_func=lambda value: t(DATASET_TEXT[value]))
        st.caption(t("simulated" if dataset == "Generated demo" else "manual_source"))
    if "saved_notice" in st.session_state:
        st.success(t("saved"))
        for warning in st.session_state.pop("saved_notice"):
            st.warning(t.message(warning))
    try:
        manual = load_records()
    except StorageError as exc:
        st.error(t.message(str(exc)))
        manual = pd.DataFrame(columns=["measured_at"])
    with entry_control:
        record_form(manual, t)
    if dataset == "Manual demo" and manual.empty:
        st.info(t("empty_manual"))
        return
    try:
        daily, notices = prepare_daily_data(generate_demo_data() if dataset == "Generated demo" else manual)
        analyzed = analyze_daily(daily)
    except ValueError as exc:
        st.error(t("prepare_error", detail=t.message(str(exc))))
        st.stop()
    for notice in notices:
        st.warning(t.message(notice))

    with st.sidebar:
        st.header(t("mission"))
        st.subheader("Deniz Yıldız" if dataset == "Generated demo" else t("manual_profile"))
        st.write(t("fictional_astronaut", subject=str(daily.subject_id.iloc[0])))
        st.caption(t("fictional_source", source=daily.source_type.iloc[0]))
        # Date options can change with the source; keep a valid selected day on locale changes.
        dates = list(analyzed.index.date)
        if st.session_state.get("review_date") not in dates:
            st.session_state["review_date"] = dates[-1]
        selected = st.selectbox(t("review_date"), dates, key="review_date")
        window = localized_choice(st.radio, t("chart_range"), [7, 14, 21], name="chart_range",
                                  language=language, initial=21, format_func=lambda n: t("last_days", days=n))
        if dataset == "Generated demo":
            st.caption(t("fixed_demo"))
        else:
            with st.expander(t("storage_policy")):
                st.caption(t("storage_body"))

    endpoint = pd.Timestamp(selected)
    row = analyzed.loc[endpoint]
    shown = analyzed.loc[endpoint - pd.Timedelta(days=window - 1):endpoint]
    st.subheader(t("overview", date=f"{endpoint:%Y-%m-%d}"))
    for column, (metric, (_, unit, _)) in zip(st.columns(3), METRIC_LABELS.items()):
        with column:
            delta = row[f"{metric}_delta"]
            if metric == "resting_hr_bpm" and dataset == "Manual demo":
                previous_date = endpoint - pd.Timedelta(days=1)
                comparable = (row.rest_state == "confirmed" and previous_date in daily.index
                              and daily.loc[previous_date, "rest_state"] == "confirmed")
                if not comparable:
                    delta = float("nan")
            display_unit = "bpm" if unit == "bpm" else t("minutes")
            st.metric(t(METRIC_TEXT[metric]), display_value(row[metric], metric, t),
                      delta=f"{delta:+.1f} {display_unit}" if pd.notna(delta) else None,
                      delta_color="off", help=t("metric_help"))
            count = int(row[f"{metric}_count7"])
            st.caption(t("average", value=display_value(row[f"{metric}_mean7"], metric, t)))
            st.progress(count / 7, text=t("coverage", count=count))
    st.caption(t("coverage_note"))

    trends, records, research = st.tabs([t("trends"), t("records"), t("evidence")])
    with trends:
        visible = localized_choice(st.multiselect, t("show_charts"), list(METRIC_LABELS),
                                   name="visible_metrics", language=language, initial=list(METRIC_LABELS),
                                   format_func=lambda metric: t(METRIC_TEXT[metric]), help=t("chart_help"))
        if not visible:
            st.info(t("no_charts"))
        for metric in METRIC_LABELS:
            if metric not in visible:
                continue
            st.plotly_chart(trend_chart(shown, metric, language), width="stretch", theme=None, key=f"chart_{metric}")
            st.caption(t("chart_quality", valid=int(shown[metric].notna().sum()), total=len(shown),
                         invalid=int(shown[f"{metric}_status"].eq("invalid").sum()),
                         missing=int(shown[f"{metric}_status"].eq("missing").sum())))
        with st.expander(t("compare")):
            st.caption(t("periods", start=f"{endpoint - pd.Timedelta(days=13):%Y-%m-%d}",
                         middle=f"{endpoint - pd.Timedelta(days=7):%Y-%m-%d}",
                         next=f"{endpoint - pd.Timedelta(days=6):%Y-%m-%d}", end=f"{endpoint:%Y-%m-%d}"))
            for comparison in compare_periods(daily, endpoint):
                st.info(t.message(comparison["message"]))
                st.caption(t.message(comparison["coverage"]))
        with st.expander(t("read_charts")):
            st.write(t("mean_method"))
            st.write(t("axis_method"))
            if dataset == "Manual demo":
                st.write(t("manual_hr_method"))
    with records:
        st.write(t("record_caption"))
        st.dataframe(shown[list(daily.columns)].reset_index(), hide_index=True, width="stretch")
        st.caption(t("units_caption"))
    with research:
        st.subheader(t("background"))
        st.caption(t("context_intro"))
        for card in explanation_cards(daily, endpoint, compare_periods(daily, endpoint)):
            with st.expander(t("evidence_limits", metric=t(METRIC_TEXT[card["metric"]]))):
                for label, field in (("observed", "observed"), ("calculated", "calculated"),
                                     ("design_rule", "design_rule"), ("published", "finding")):
                    st.write(f"**{t(label)}:** " + t.message(card[field]))
                st.caption(t.message(card["coverage"]))
                st.markdown(f"[{t('source_link')}: {card['title']}]({card['url']})")
                st.caption(t("limitation") + ": " + t.message(card["limitation"]))
        with st.expander(t("methods")):
            st.markdown("- [NASA Fatigue Countermeasures Laboratory](https://www.nasa.gov/human-systems-integration-division/human-performance/fatigue-countermeasures-laboratory/)\n- [NASA Wearable Tech for Space Station Research](https://www.nasa.gov/humans-in-space/wearable-tech-for-space-station-research/)")
            st.info(t("source_caveat"))
            st.write(t("data_method"))
        st.caption(t("research_available"))
    st.caption(t("footer"))


if __name__ == "__main__":
    main()
