import pandas as pd

from volatility import build_volatility_summary


def main() -> None:
    # Load CSV file
    try:
        data = pd.read_csv("sample_data.csv")
    except FileNotFoundError:
        print("Error: sample_data.csv was not found.")
        return

    # Check required column
    if "Close" not in data.columns:
        print("Error: CSV file must contain a 'Close' column.")
        return

    # Extract closing prices
    prices = data["Close"]

    # Build summary results
    try:
        summary = build_volatility_summary(
            prices,
            return_method="log",
        )
    except ValueError as error:
        print(f"Error: {error}")
        return

    # Print report header
    print("Volatility Calculator")
    print("-" * 40)

    # Print core results
    print(f"Observation count: {summary['observation_count']}")
    print(f"Return method: {summary['return_method']}")

    # Print return series
    print("\nDaily returns:")
    print(summary["returns"])

    # Print volatility values
    print(
        f"\nDaily volatility: "
        f"{summary['daily_volatility']:.4%}"
    )
    print(
        f"Annualized volatility: "
        f"{summary['annualized_volatility']:.4%}"
    )

    # Print rolling volatility
    print("\n7-day rolling volatility:")
    print(summary["rolling_volatility_7d"])


# Start program
if __name__ == "__main__":
    main()