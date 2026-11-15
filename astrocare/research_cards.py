"""Compact, accessible HTML presentation of a validated research comparison."""

from html import escape
from string import Template

from astrocare.i18n import Translator
from astrocare.theme import COLORS


def research_cards_html(comparison):
    """Escape source text; draw quantitative lengths on the model's shared scale."""
    t = Translator(comparison.language)
    styles = Template("""<style>
    .ac-research {background:$background; border:1px solid $border; border-radius:16px;
        padding:20px; color:$text; margin:4px 0 8px;}
    .ac-research .ac-header {display:flex; justify-content:space-between; gap:16px;
        align-items:center; margin-bottom:20px;}
    .ac-research .ac-meta {font-size:14px; color:$secondary; margin-bottom:6px;}
    .ac-research .ac-analyte {font-size:24px; font-weight:650; line-height:1.25; margin:0;}
    .ac-research .ac-unit {font-size:16px; color:$secondary; text-align:right;}
    .ac-research .ac-count {font-size:14px; margin-top:6px; color:$secondary;}
    .ac-research .ac-phases {display:grid; grid-template-columns:minmax(0,1fr) minmax(0,1fr); gap:18px;}
    .ac-research .ac-phase {background:$card; border:1px solid $border; border-radius:12px;
        padding:20px 18px; min-width:0;}
    .ac-research .ac-phase-heading {font-size:18px; font-weight:650; display:flex;
        align-items:center; gap:10px; margin:0 0 24px; line-height:1.4;}
    .ac-research .ac-dot {display:inline-block; width:11px; height:11px; border-radius:50%; flex:none;}
    .ac-research .ac-row {margin-bottom:24px;}
    .ac-research .ac-row:last-child {margin-bottom:0;}
    .ac-research .ac-row-labels {display:flex; align-items:baseline; justify-content:space-between;
        gap:12px; margin-bottom:10px; line-height:1.35;}
    .ac-research .ac-sample {font-size:15px; color:$secondary; flex:none;}
    .ac-research .ac-value {font-size:18px; font-weight:650; text-align:right;
        color:$text; font-variant-numeric:tabular-nums; overflow-wrap:anywhere;}
    .ac-research .ac-track {height:10px; border-radius:6px; background:$border; overflow:hidden;}
    .ac-research .ac-fill {height:100%; border-radius:inherit;}
    .ac-research .ac-missing .ac-track {height:10px; box-sizing:border-box;
        background:transparent; border:1px dashed $control_border;}
    .ac-research .ac-missing .ac-value {font-size:15px; font-weight:500; color:$secondary;}
    .ac-research .ac-footer {font-size:14px; line-height:1.5; color:$secondary; margin-top:16px;}
    .ac-research .ac-empty {font-size:15px; color:$secondary; line-height:1.5;}
    @media (max-width:760px) {
        .ac-research {padding:16px;}
        .ac-research .ac-phases {grid-template-columns:minmax(0,1fr); gap:14px;}
        .ac-research .ac-phase {padding:18px 16px;}
        .ac-research .ac-analyte {font-size:22px;}
    }
    </style>""").substitute(COLORS)
    panels = []
    for phase in comparison.phases:
        rows = []
        for row in phase.measurements:
            detail = t("comparison_row_info", subject=comparison.subject_id, analyte=comparison.analyte,
                       value=row.value_label, unit=comparison.unit, point=row.label, phase=phase.title,
                       context=row.context, dataset=comparison.dataset_id)
            missing = row.value is None
            fill = "" if missing else (
                f'<div class="ac-fill" style="width:{row.fraction * 100:.12g}%;background:{phase.color}"></div>'
            )
            value_attribute = "" if missing else str(row.value)
            rows.append(
                f'<div class="ac-row{" ac-missing" if missing else ""}" role="group" '
                f'data-sample="{escape(row.label, quote=True)}" data-value="{escape(value_attribute, quote=True)}" '
                f'data-missing="{str(missing).lower()}" title="{escape(detail, quote=True)}" '
                f'aria-label="{escape(detail, quote=True)}">'
                f'<div class="ac-row-labels"><span class="ac-sample">{escape(row.label)}</span>'
                f'<span class="ac-value">{escape(row.value_label)}</span></div>'
                f'<div class="ac-track" aria-hidden="true">{fill}</div></div>'
            )
        if not rows:
            rows.append(f'<div class="ac-empty">{escape(t("no_phase_samples"))}</div>')
        panels.append(
            f'<section class="ac-phase" data-phase="{escape(phase.phase, quote=True)}" '
            f'data-scale-max="{comparison.scale_max}" aria-label="{escape(phase.title, quote=True)}">'
            f'<div class="ac-phase-heading" role="heading" aria-level="4"><span class="ac-dot" aria-hidden="true" '
            f'style="background:{phase.color}"></span>{escape(phase.title)}</div>{"".join(rows)}</section>'
        )
    footer = t("shared_research_scale", maximum=comparison.scale_label, unit=comparison.unit)
    count = t("comparison_available", valid=comparison.valid_count, total=comparison.sample_count)
    return styles + (
        f'<section class="ac-research" data-testid="research-comparison" '
        f'data-scale-max="{comparison.scale_max}" aria-label="{escape(t("research"), quote=True)}">'
        f'<div class="ac-header"><div><div class="ac-meta">{escape(comparison.dataset_id)} · '
        f'{escape(comparison.subject_id)}</div><div class="ac-analyte" role="heading" aria-level="3">{escape(comparison.analyte)}</div></div>'
        f'<div><div class="ac-unit">{escape(comparison.unit)}</div>'
        f'<div class="ac-count">{escape(count)}</div></div></div>'
        f'<div class="ac-phases">{"".join(panels)}</div><div class="ac-footer">{escape(footer)}</div></section>'
    )
