"""Separate, localized view of authentic research; no synthetic fallback."""

from html import escape
from string import Template

import streamlit as st

from astrocare.i18n import Translator
from astrocare.research import ResearchError, load_research, read_manifest, research_chart
from astrocare.research_cards import research_cards_html
from astrocare.theme import COLORS


def research_header(t, *, verified=False):
    """A verified indicator describes local integrity, never scientific approval."""
    styles = Template("""<style>
    .ac-research-heading {margin:4px 0 8px; color:$text;}
    .ac-research-heading .ac-heading-top {display:flex; align-items:center;
        justify-content:space-between; flex-wrap:wrap; gap:12px 20px;}
    .ac-research-heading .ac-heading-title {font-size:28px; font-weight:650;
        line-height:1.25; letter-spacing:-.02em;}
    .ac-research-heading .ac-heading-subtitle {font-size:16px; color:$secondary; margin-top:6px;}
    .ac-research-heading .ac-verified {display:inline-flex; align-items:center; gap:8px;
        color:$activity; border:1px solid $control_border; border-radius:20px;
        padding:6px 11px; font-size:14px; line-height:1.4; background:$surface;}
    .ac-research-heading .ac-heading-notes {display:flex; flex-wrap:wrap;
        align-items:center; gap:8px 16px; margin-top:14px;}
    .ac-research-heading .ac-research-only {color:$heart; font-size:14px; font-weight:600;}
    .ac-research-heading .ac-separation {font-size:14px; color:$secondary; line-height:1.5;}
    @media(max-width:760px) {
        .ac-research-heading .ac-heading-title {font-size:24px;}
        .ac-research-heading .ac-heading-top {align-items:flex-start;}
    }
    </style>""").substitute(COLORS)
    indicator = (
        f'<span class="ac-verified" role="status" data-testid="research-verified" '
        f'title="{escape(t("verified_scope"), quote=True)}">'
        f'<span aria-hidden="true">✓</span>{escape(t("verified_data"))}</span>'
    ) if verified else ""
    st.markdown(styles + (
        '<section class="ac-research-heading" data-testid="research-header">'
        '<div class="ac-heading-top"><div>'
        f'<div class="ac-heading-title" role="heading" aria-level="1">{escape(t("research"))}</div>'
        f'<div class="ac-heading-subtitle">{escape(t("research_subtitle"))}</div>'
        f'</div>{indicator}</div><div class="ac-heading-notes">'
        f'<span class="ac-research-only">{escape(t("research_only"))}</span>'
        f'<span class="ac-separation">{escape(t("research_separation"))}</span>'
        '</div></section>'
    ), unsafe_allow_html=True)


def research_details(manifest, t, receipt=None):
    with st.expander(t("study_context")):
        st.write(manifest["title"])
        st.write(t("research_origin"))
        st.write(t("research_context"))
        st.caption(t("serum_timeline"))
        st.caption(t("timeline_key"))
        st.write(t("research_limits"))
        st.caption(t("eligibility"))
        st.write(t("schedule_caveat"))
        st.write(t("pseudonyms"))
        st.caption(t("counts_note"))
    with st.expander(t("provenance")):
        st.markdown(f"**{manifest['dataset_id']} · v{manifest['study_version']}** · [{t('nasa_source')}]({manifest['source_url']}) · [{t('license')}: {manifest['license']}]({manifest['license_url']})")
        st.write(f"DOI: {manifest['doi']}")
        st.caption(t("offline"))
        st.caption(t("verified_scope"))
        st.write(t("marker_method"))
        st.write(t("original_file", file=manifest["file_name"]))
        st.caption(t("original_shape", rows=manifest["expected_rows"], columns=len(manifest["expected_columns"])))
        if receipt is not None:
            st.caption(t("acquired", time=receipt["retrieved_at_utc"]))
        st.write("CSV SHA-256")
        st.code(manifest["sha256"], language=None)
        st.caption(t("original_metadata"))
        st.write(manifest["license_evidence"])
        st.markdown(f"[{t('csv_download')}]({manifest['download_url']}) · [{t('file_listing')}]({manifest['files_api']}) · [{t('study_metadata')}]({manifest['metadata_api']})")
        st.caption(t("metadata_hash", hash=manifest["metadata_sha256"]))


def render_research_explorer(language="en"):
    t = Translator(language)
    try:
        manifest = read_manifest()
    except ResearchError as exc:
        research_header(t)
        st.error(t.message(str(exc)))
        return
    try:
        bundle = load_research()
    except ResearchError as exc:
        research_header(t)
        st.error(t.message(str(exc)))
        st.info(t("unavailable"))
        st.code(r".\.venv\Scripts\python.exe -m astrocare.acquire_research", language="powershell")
        research_details(manifest, t)
        return
    research_header(t, verified=True)
    frame = bundle.observations
    for column, key, value in zip(st.columns(3), ["participants", "samples", "analytes"],
                                  [frame.subject_id.nunique(), frame.sample_name.nunique(), frame.analyte.nunique()]):
        column.metric(t(key), str(value))
    left, right = st.columns(2)
    with left:
        subject = st.selectbox(t("participant"), sorted(frame.subject_id.unique()), key="research_subject")
    with right:
        analyte = st.selectbox(t("analyte"), [a["label"] for a in manifest["analytes"]], key="research_analyte")
    selected = frame.loc[frame.subject_id.eq(subject) & frame.analyte.eq(analyte)]
    try:
        comparison = research_chart(selected, language)
    except ResearchError as exc:
        st.error(t.message(str(exc)))
        return
    st.markdown(research_cards_html(comparison), unsafe_allow_html=True)
    with st.expander(t("view_samples")):
        st.dataframe(selected[["timepoint", "value", "unit", "phase", "sampling_context", "anchor", "subject_id", "analyte", "sample_name", "dataset_id", "source_type", "is_synthetic"]],
                     hide_index=True, width="stretch")
        st.caption(t("original_fields"))
    research_details(manifest, t, bundle.receipt)
