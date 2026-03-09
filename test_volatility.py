import math

import pandas as pd
import pytest

from volatility import (
    build_volatility_summary,
    calculate_annualized_volatility,
    calculate_daily_volatility,
    calculate_log_returns,
    calculate_rolling_volatility,
    calculate_simple_returns,
    validate_prices,
)


# Test price validation
def test_validate_prices_removes_missing_values() -> None:
    prices = pd.Series([100, None, 105, 110])
    result = validate_prices(prices)
    assert len(result) == 3


# Test minimum observations
def test_validate_prices_requires_two_values() -> None:
    prices = pd.Series([100])
    with pytest.raises(ValueError):
        validate_prices(prices)


# Test positive prices
def test_validate_prices_rejects_non_positive_values() -> None:
    prices = pd.Series([100, 0, 105])
    with pytest.raises(ValueError):
        validate_prices(prices)


# Test simple returns
def test_calculate_simple_returns() -> None:
    prices = pd.Series([100, 110, 121])
    returns = calculate_simple_returns(prices)

    assert pytest.approx(returns.iloc[0]) == 0.10
    assert pytest.approx(returns.iloc[1]) == 0.10


# Test log returns
def test_calculate_log_returns() -> None:
    prices = pd.Series([100, 110])
    returns = calculate_log_returns(prices)

    expected = math.log(110 / 100)
    assert pytest.approx(returns.iloc[0]) == expected


# Test daily volatility
def test_calculate_daily_volatility() -> None:
    returns = pd.Series([0.01, 0.02, 0.03])
    result = calculate_daily_volatility(returns)

    assert isinstance(result, float)


# Test annualized volatility
def test_calculate_annualized_volatility() -> None:
    daily_volatility = 0.02
    result = calculate_annualized_volatility(daily_volatility)

    assert pytest.approx(result) == daily_volatility * math.sqrt(365)


# Test rolling volatility
def test_calculate_rolling_volatility() -> None:
    returns = pd.Series([0.01, 0.02, 0.03, 0.02, 0.01, 0.04, 0.03, 0.02])
    result = calculate_rolling_volatility(returns, window=7)

    assert len(result) == 2


# Test summary output
def test_build_volatility_summary() -> None:
    prices = pd.Series([100, 110, 105, 115, 120, 118, 122, 125])

    summary = build_volatility_summary(
        prices,
        return_method="simple",
    )

    assert "observation_count" in summary
    assert "returns" in summary
    assert "daily_volatility" in summary
    assert "annualized_volatility" in summary
    assert "rolling_volatility_7d" in summary