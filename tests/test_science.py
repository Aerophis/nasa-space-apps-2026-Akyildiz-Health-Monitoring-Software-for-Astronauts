import pytest

from astrocare.analysis import compare_periods
from astrocare.data import generate_demo_data, prepare_daily_data
from astrocare.science import SCIENCE_SOURCES, explanation_cards


def test_cards_separate_observation_calculation_rule_and_published_context():
    daily, _ = prepare_daily_data(generate_demo_data())
    cards = explanation_cards(daily, daily.index[-1], compare_periods(daily, daily.index[-1]))
    assert len(cards) == 3
    for card in cards:
        assert card["url"].startswith("https://www.nasa.gov/")
        assert card["title"] and card["finding"] and card["limitation"]
        assert "fictional" in card["observed"]
        assert "prototype design rule" in card["design_rule"]
        assert card["calculated"] and card["coverage"]
        assert card["url"] == SCIENCE_SOURCES[card["metric"]]["url"]


def test_missing_invalid_and_true_zero_have_different_explanations():
    raw = generate_demo_data()
    raw.loc[20, "sleep_minutes"] = float("nan")
    raw.loc[20, "activity_minutes"] = 0
    raw.loc[20, "resting_hr_bpm"] = -1
    daily, _ = prepare_daily_data(raw)
    cards = explanation_cards(daily, daily.index[-1], compare_periods(daily, daily.index[-1]))
    assert "Missing measurement" in cards[0]["observed"]
    assert "Invalid measurement" in cards[1]["observed"]
    assert "0 minutes" in cards[2]["observed"]


def test_explanations_refuse_real_research_provenance():
    daily, _ = prepare_daily_data(generate_demo_data())
    comparisons = compare_periods(daily, daily.index[-1])
    daily["source_type"] = "nasa_research"
    daily["is_synthetic"] = False
    with pytest.raises(ValueError):
        explanation_cards(daily, daily.index[-1], comparisons)
