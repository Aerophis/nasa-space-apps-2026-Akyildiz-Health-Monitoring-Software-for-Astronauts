"""Plotly presentation shared by the UI and chart tests."""

import plotly.graph_objects as go

METRIC_LABELS = {
    "sleep_minutes": ("Uyku süresi", "dakika", "#61d7ff"),
    "resting_hr_bpm": ("Dinlenme kalp atım hızı", "bpm", "#ffb18b"),
    "activity_minutes": ("Egzersiz / aktivite", "dakika", "#b9a1ff"),
}


def trend_chart(data, metric):
    title, unit, color = METRIC_LABELS[metric]
    fig = go.Figure()
    for column, name, dash in (
        (metric, "Günlük ölçüm", "solid"),
        (f"{metric}_mean7", "7 günlük ortalama", "dash"),
    ):
        fig.add_trace(go.Scatter(
            x=data.index, y=data[column], name=name,
            mode="lines+markers" if column == metric else "lines",
            line={"color": color, "dash": dash, "width": 2},
            connectgaps=False,
            hovertemplate=f"%{{x|%d.%m.%Y}}<br>%{{y:.1f}} {unit}<extra>%{{fullData.name}}</extra>",
        ))
    fig.update_layout(
        title=title, yaxis_title=unit, xaxis_title="Ölçüm tarihi (UTC)",
        template="plotly_dark", height=320, hovermode="x unified",
        margin={"l": 15, "r": 15, "t": 50, "b": 15},
        legend={"orientation": "h", "y": 1.18},
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig
