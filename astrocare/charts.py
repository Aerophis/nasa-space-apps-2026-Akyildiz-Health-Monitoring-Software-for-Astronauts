"""Plotly presentation shared by the UI and chart tests."""

import plotly.graph_objects as go

from astrocare.i18n import Translator
from astrocare.theme import COLORS

METRIC_LABELS = {
    "sleep_minutes": ("Sleep duration", "minutes", COLORS["sleep"]),
    "resting_hr_bpm": ("Resting heart rate", "bpm", COLORS["heart"]),
    "activity_minutes": ("Exercise / activity", "minutes", COLORS["activity"]),
}


def style_chart(fig):
    """Readable, restrained styling shared by exported and embedded figures."""
    fig.update_layout(
        template="plotly_dark", height=470,
        font={"family": "Arial, sans-serif", "size": 15, "color": COLORS["text"]},
        paper_bgcolor=COLORS["surface"], plot_bgcolor=COLORS["surface"],
        title={"font": {"size": 19, "color": COLORS["text"]}, "x": .035, "y": .96},
        margin={"l": 56, "r": 24, "t": 100, "b": 140},
        legend={"orientation": "h", "y": 1.18, "x": 0,
                "font": {"size": 14, "color": COLORS["secondary"]}, "tracegroupgap": 12},
        hoverlabel={"bgcolor": COLORS["card"], "font_size": 15, "font_color": COLORS["text"]},
    )
    axes = {"tickfont": {"size": 14, "color": COLORS["secondary"]},
            "title_font": {"size": 15, "color": COLORS["secondary"]},
            "zeroline": False, "automargin": True}
    fig.update_xaxes(showgrid=False, **axes)
    fig.update_yaxes(gridcolor="rgba(168,184,200,.16)", **axes)
    return fig


def trend_chart(data, metric, language="en"):
    if ("source_type" in data and not data.source_type.isin(["synthetic_demo", "manual_demo"]).all()
            or "is_synthetic" in data and not data.is_synthetic.eq(True).all()):
        raise ValueError("Real research samples cannot be plotted as simulated health telemetry.")
    title, unit, color = METRIC_LABELS[metric]
    t = Translator(language)
    title = t({"sleep_minutes": "sleep", "resting_hr_bpm": "heart", "activity_minutes": "activity"}[metric])
    unit = "bpm" if unit == "bpm" else t("minutes")
    fig = go.Figure()
    hover = f"%{{x|%Y-%m-%d}}<br>%{{y:.1f}} {unit}<extra>%{{fullData.name}}</extra>"
    if metric == "activity_minutes":
        fig.add_trace(go.Bar(x=data.index, y=data[metric], name=t("daily_measurement"),
                             marker_color=color, hovertemplate=hover))
    else:
        fig.add_trace(go.Scatter(
            x=data.index, y=data[metric], name=t("daily_measurement"), mode="lines+markers",
            line={"color": color, "width": 3}, marker={"size": 8}, connectgaps=False,
            fill="tozeroy" if metric == "sleep_minutes" else None,
            fillcolor="rgba(120,168,232,.14)", hovertemplate=hover))
    fig.add_trace(go.Scatter(x=data.index, y=data[f"{metric}_mean7"], name=t("mean7"),
                             mode="lines", line={"color": COLORS["muted"], "dash": "dash", "width": 1.6},
                             connectgaps=False, hovertemplate=hover))
    style_chart(fig)
    fig.update_layout(
        title=title, yaxis_title=unit, xaxis_title=t("chart_date"),
        hovermode="x unified", bargap=.35,
    )
    if metric != "resting_hr_bpm":
        fig.update_yaxes(rangemode="tozero")
    fig.update_xaxes(tickformat="%Y-%m-%d")
    source = data["source_type"].iloc[0] if len(data) and "source_type" in data else "unknown"
    fig.add_annotation(text="DEMO — SIMULATED DATA<br>" + t("chart_source", source=source),
                       x=0, y=0, yshift=-104, xref="paper", yref="paper", showarrow=False,
                       xanchor="left", yanchor="top", font={"size": 13, "color": COLORS["secondary"]})
    return fig
