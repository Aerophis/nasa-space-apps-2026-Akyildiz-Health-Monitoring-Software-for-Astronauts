"""Plotly presentation shared by the UI and chart tests."""

import plotly.graph_objects as go

METRIC_LABELS = {
    "sleep_minutes": ("Sleep duration", "minutes", "#61d7ff"),
    "resting_hr_bpm": ("Resting heart rate", "bpm", "#ffb18b"),
    "activity_minutes": ("Exercise / activity", "minutes", "#b9a1ff"),
}


def trend_chart(data, metric):
    title, unit, color = METRIC_LABELS[metric]
    fig = go.Figure()
    for column, name, dash in (
        (metric, "Daily measurement", "solid"),
        (f"{metric}_mean7", "7-day average", "dash"),
    ):
        fig.add_trace(go.Scatter(
            x=data.index, y=data[column], name=name,
            mode="lines+markers" if column == metric else "lines",
            line={"color": color, "dash": dash, "width": 2},
            connectgaps=False,
            hovertemplate=f"%{{x|%d.%m.%Y}}<br>%{{y:.1f}} {unit}<extra>%{{fullData.name}}</extra>",
        ))
    fig.update_layout(
        title=title, yaxis_title=unit, xaxis_title="Measurement date (UTC)",
        template="plotly_dark", height=360, hovermode="x unified",
        margin={"l": 15, "r": 15, "t": 50, "b": 80},
        legend={"orientation": "h", "y": 1.18},
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    )
    source = data["source_type"].iloc[0] if len(data) and "source_type" in data else "unknown"
    fig.add_annotation(text=f"DEMO — SIMULATED DATA · source: {source}",
                       x=0, y=-0.32, xref="paper", yref="paper", showarrow=False,
                       xanchor="left", font={"size": 11, "color": "#a8bed8"})
    return fig
