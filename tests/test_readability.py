"""Accessibility targets and chart emphasis must survive presentation changes."""

from pathlib import Path
import tomllib

import pytest

from astrocare.analysis import analyze_daily
from astrocare.charts import METRIC_LABELS, trend_chart
from astrocare.data import generate_demo_data, prepare_daily_data
from astrocare.theme import COLORS


def contrast(first, second):
    def luminance(color):
        channels = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        linear = [c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4 for c in channels]
        return sum(c * weight for c, weight in zip(linear, (.2126, .7152, .0722)))
    high, low = sorted((luminance(first), luminance(second)), reverse=True)
    return (high + .05) / (low + .05)


@pytest.mark.parametrize("foreground", ["text", "secondary", "muted"])
@pytest.mark.parametrize("background", ["background", "surface", "card"])
def test_normal_text_palette_meets_wcag_aa(foreground, background):
    assert contrast(COLORS[foreground], COLORS[background]) >= 4.5


def test_selected_chip_labels_meet_normal_text_aa():
    assert contrast(COLORS["text"], COLORS["chip"]) >= 4.5


def test_interactive_borders_and_focus_meet_nontext_contrast():
    assert contrast(COLORS["control_border"], COLORS["surface"]) >= 3
    assert contrast(COLORS["focus"], COLORS["surface"]) >= 3


def test_native_theme_agrees_with_plot_and_css_tokens():
    config = Path(__file__).resolve().parents[1] / ".streamlit" / "config.toml"
    theme = tomllib.loads(config.read_text(encoding="utf-8"))["theme"]
    assert theme["backgroundColor"] == COLORS["background"]
    assert theme["secondaryBackgroundColor"] == COLORS["surface"]
    assert theme["textColor"] == COLORS["text"]
    assert theme["primaryColor"] == COLORS["focus"]


@pytest.mark.parametrize("metric", METRIC_LABELS)
def test_health_chart_emphasizes_measurements_with_readable_labels(metric):
    daily = analyze_daily(prepare_daily_data(generate_demo_data())[0])
    fig = trend_chart(daily, metric)
    color = METRIC_LABELS[metric][2]
    actual = fig.data[0]
    assert (actual.marker.color if actual.type == "bar" else actual.line.color) == color
    assert contrast(color, fig.layout.plot_bgcolor) >= 4.5
    assert fig.data[1].line.color == COLORS["muted"]
    assert fig.data[1].line.dash == "dash"
    assert fig.layout.xaxis.tickfont.size >= 14
    assert fig.layout.yaxis.tickfont.size >= 14
    assert fig.layout.legend.font.size >= 14
    assert "extra" in actual.hovertemplate
    footnote = fig.layout.annotations[0]
    assert footnote.y == 0 and footnote.yanchor == "top"
    assert fig.layout.margin.b >= abs(footnote.yshift) + 32
