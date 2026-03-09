import math

import pandas as pd

# Crypto trading calendar
TRADING_PERIODS_PER_YEAR = 365


# Clean input prices
def validate_prices(prices: pd.Series) -> pd.Series:
    cleaned_prices = prices.dropna()

    if len(cleaned_prices) < 2:
        raise ValueError(
            "At least two valid price points are required to calculate "
            "volatility."
        )

    if (cleaned_prices <= 0).any():
        raise ValueError("All price points must be positive numbers.")

    return cleaned_prices


# Compute simple returns
def calculate_simple_returns(prices: pd.Series) -> pd.Series:
    # Validate prices
    validated_prices = validate_prices(prices)
    # Compute returns
    returns = validated_prices.pct_change().dropna()
    return returns


# Compute log returns
def calculate_log_returns(prices: pd.Series) -> pd.Series:
    # Validate prices
    validated_prices = validate_prices(prices)
    # Compute returns
    log_returns = (validated_prices / validated_prices.shift(1)).apply(
        math.log
    ).dropna()
    return log_returns


# Compute daily volatility
def calculate_daily_volatility(returns: pd.Series) -> float:
    # Check input data
    if len(returns) == 0:
        raise ValueError("Return series is empty.")

    return float(returns.std())


# Annualize volatility
def calculate_annualized_volatility(
    daily_volatility: float,
    periods_per_year: int = TRADING_PERIODS_PER_YEAR,
) -> float:
    return daily_volatility * math.sqrt(periods_per_year)


# Compute rolling volatility
def calculate_rolling_volatility(
    returns: pd.Series,
    window: int = 7,
) -> pd.Series:
    # Check window size
    if len(returns) < window:
        raise ValueError(
            "Return series is too short for the rolling window."
        )

    # Compute rolling std
    rolling_volatility = returns.rolling(window=window).std()
    return rolling_volatility.dropna()


# Build summary output
def build_volatility_summary(
    prices: pd.Series,
    return_method: str = "simple",
) -> dict:
    # Validate prices
    validated_prices = validate_prices(prices)

    # Choose return method
    if return_method == "simple":
        returns = calculate_simple_returns(validated_prices)
    elif return_method == "log":
        returns = calculate_log_returns(validated_prices)
    else:
        raise ValueError(
            "return_method must be either 'simple' or 'log'."
        )

    # Calculate volatilities
    daily_volatility = calculate_daily_volatility(returns)
    annualized_volatility = calculate_annualized_volatility(
        daily_volatility
    )
    rolling_volatility_7d = calculate_rolling_volatility(
        returns,
        window=7,
    )

    # Return summary
    return {
        "observation_count": len(validated_prices),
        "return_method": return_method,
        "returns": returns,
        "daily_volatility": daily_volatility,
        "annualized_volatility": annualized_volatility,
        "rolling_volatility_7d": rolling_volatility_7d,
    }