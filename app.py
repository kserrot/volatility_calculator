import pandas as pd
import streamlit as st

from volatility import build_volatility_summary


# Page title
st.title("Crypto Volatility Calculator")

# Short description
st.write(
    "Upload a CSV file with a Close column to calculate "
    "crypto volatility."
)

# Return method selector
return_method = st.selectbox(
    "Select return method",
    ["simple", "log"],
)

# File uploader
uploaded_file = st.file_uploader(
    "Upload your CSV file",
    type=["csv"],
)

if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file)
    except Exception as error:
        st.error(f"Could not read the file: {error}")
    else:
        if "Close" not in data.columns:
            st.error("CSV file must contain a 'Close' column.")
        else:
            prices = data["Close"]

            try:
                summary = build_volatility_summary(
                    prices,
                    return_method=return_method,
                )
            except ValueError as error:
                st.error(f"Error: {error}")
            else:
                st.subheader("Summary")
                st.write(
                    f"Observation count: "
                    f"{summary['observation_count']}"
                )
                st.write(
                    f"Return method: "
                    f"{summary['return_method']}"
                )
                st.write(
                    f"Daily volatility: "
                    f"{summary['daily_volatility']:.4%}"
                )
                st.write(
                    f"Annualized volatility: "
                    f"{summary['annualized_volatility']:.4%}"
                )

                st.subheader("Daily Returns")
                st.dataframe(summary["returns"])

                st.subheader("7-Day Rolling Volatility")
                st.dataframe(summary["rolling_volatility_7d"])