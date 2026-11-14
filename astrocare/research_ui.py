"""Separate Streamlit view for real research data, with an honest missing-data state."""

import streamlit as st

from astrocare.research import ResearchError, load_research, read_manifest, research_chart


def render_research_explorer():
    st.header("NASA Research Data Explorer")
    try:
        manifest = read_manifest()
    except ResearchError as exc:
        st.error(str(exc))
        return
    st.subheader(manifest["title"])
    st.markdown(f"**Dataset:** {manifest['dataset_id']} · **Study version:** {manifest['study_version']} · **DOI:** {manifest['doi']}")
    st.markdown(f"[Official NASA OSDR source]({manifest['source_url']}) · [License: {manifest['license']}]({manifest['license_url']})")
    st.write(manifest["origin"])
    st.write(manifest["context"])
    st.warning(manifest["limitations"])
    st.caption("Scientific status: CORRECTIONS REQUIRED. NASA hosting is not NASA endorsement. No diagnoses, clinical reference-range classifications, or causal conclusions are provided.")
    try:
        bundle = load_research()
    except ResearchError as exc:
        st.error(str(exc))
        st.info("SCIENTIFIC BACKGROUND INFORMATION — numerical research integration is unavailable in this local installation. Links alone do not establish dataset integration.")
        st.code(r".\.venv\Scripts\python.exe -m astrocare.acquire_research", language="powershell")
        return
    st.success("AUTHENTIC NASA RESEARCH DATA — NASA-hosted OSD-575 samples loaded and checksum-verified locally. Not synthetic or daily health telemetry.")
    st.caption(f"Acquisition recorded (UTC): {bundle.receipt['retrieved_at_utc']} · CSV SHA-256: {manifest['sha256']}")
    st.caption(f"Original file: {manifest['file_name']} · {manifest['expected_rows']} biospecimen rows × {len(manifest['expected_columns'])} columns. Four selected analytes are displayed; reference-range columns are not interpreted.")
    st.caption("The explorer reads prepared local files without network access. Nothing is merged with the generated or manual demo records.")
    frame = bundle.observations
    subject = st.selectbox("Research participant (published pseudonym)", sorted(frame.subject_id.unique()), key="research_subject")
    analyte = st.selectbox("Serum analyte", [a["label"] for a in manifest["analytes"]], key="research_analyte")
    selected = frame.loc[frame.subject_id.eq(subject) & frame.analyte.eq(analyte)]
    st.caption(f"Valid values: {int(selected.value.notna().sum())}/{len(selected)} scheduled samples. Missing assay results remain missing. Marker positions are scheduled samples, not a continuous daily time axis.")
    st.plotly_chart(research_chart(selected), width="stretch", key="nasa_research_chart")
    st.dataframe(selected[["sample_name", "phase", "sampling_context", "anchor", "analyte", "value", "unit", "dataset_id", "source_type", "is_synthetic"]],
                 hide_index=True, width="stretch")
    with st.expander("Source and reproducibility details"):
        st.write(manifest["license_evidence"])
        st.markdown(f"[Original CSV download]({manifest['download_url']}) · [Official file listing]({manifest['files_api']}) · [Study metadata]({manifest['metadata_api']})")
        st.caption(f"Metadata snapshot SHA-256: {manifest['metadata_sha256']}")
        st.write("The study summary describes a shorter post-flight schedule than the CSV/sample table. R+194 is retained because it is explicitly present in both actual CSV and sample metadata; it is not inferred or interpolated.")
        st.write("Only published pseudonyms and measurements are shown. No attempt is made to identify participants or associate these records with the fictional profiles.")
