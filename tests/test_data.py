from astrocare.data import classify_sleep_minutes

def test_missing_sleep():
    result = classify_sleep_minutes(None)
    assert result == "missing"

def test_invalid_sleep():
    result = classify_sleep_minutes(-10)
    assert result == "İnvalid"

def test_zero_sleep():
    result = classify_sleep_minutes(0)
    assert result == "Valid"

def test_max_sleep():
    result = classify_sleep_minutes(1440)
    assert result == "Valid"

def test_over_max_sleep():
    result = classify_sleep_minutes(1441)
    assert result == "İnvalid"

def test_nan_sleep():
    result = classify_sleep_minutes(float("nan"))
    assert result == "missing"