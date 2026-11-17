import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Financial Risk & Volatility Monitor",
    page_icon="📈",
    layout="wide"
)

st.title("Financial Risk & Volatility Monitor")

st.write(
    "An interactive financial risk analytics dashboard "
    "using historical market data and GARCH volatility models."
)

# --------------------------------------------------
# Load data
# --------------------------------------------------

DATA_PATH = Path(__file__).parent / "data"

@st.cache_data
def load_data():

    prices = pd.read_csv(
        DATA_PATH / "stock_prices.csv",
        index_col=0,
        parse_dates=True
    )

    returns = pd.read_csv(
        DATA_PATH / "stock_returns.csv",
        index_col=0,
        parse_dates=True
    )

    risk = pd.read_csv(
        DATA_PATH / "msft_risk_analysis.csv",
        index_col=0,
        parse_dates=True
    )

    return prices, returns, risk


prices, returns, risk = load_data()

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.header("Settings")

ticker = st.sidebar.selectbox(
    "Select Stock",
    prices.columns.tolist()
)

confidence = st.sidebar.selectbox(
    "VaR Confidence Level",
    [95, 99],
    index=1
)

# --------------------------------------------------
# Stock prices
# --------------------------------------------------

st.header("Historical Stock Prices")

fig_price = px.line(
    prices,
    x=prices.index,
    y=ticker,
    title=f"{ticker}: Historical Adjusted Prices"
)

st.plotly_chart(fig_price, use_container_width=True)

# --------------------------------------------------
# Daily returns
# --------------------------------------------------

st.header("Daily Returns")

fig_returns = px.line(
    returns,
    x=returns.index,
    y=ticker,
    title=f"{ticker}: Daily Log Returns (%)"
)

st.plotly_chart(fig_returns, use_container_width=True)

# --------------------------------------------------
# Rolling volatility
# --------------------------------------------------

st.header("Historical Volatility")

rolling_vol = (
    returns[ticker]
    .rolling(22)
    .std()
    * np.sqrt(252)
)

fig_vol = px.line(
    x=rolling_vol.index,
    y=rolling_vol.values,
    title=f"{ticker}: 22-Day Rolling Annualized Volatility"
)

fig_vol.update_layout(
    xaxis_title="Date",
    yaxis_title="Annualized Volatility (%)"
)

st.plotly_chart(fig_vol, use_container_width=True)

# --------------------------------------------------
# Risk analysis
# --------------------------------------------------

st.header("GARCH-Based Risk Analysis")

if ticker == "MSFT":

    var_column = f"VaR_{confidence}"
    es_column = f"ES_{confidence}"
    violation_column = f"Violation_{confidence}"

    col1, col2, col3 = st.columns(3)

    col1.metric(
        f"{confidence}% VaR",
        f"${risk[var_column].iloc[-1]:,.2f}"
    )

    col2.metric(
        f"{confidence}% Expected Shortfall",
        f"${risk[es_column].iloc[-1]:,.2f}"
    )

    col3.metric(
        "VaR Violation Rate",
        f"{risk[violation_column].mean() * 100:.2f}%"
    )

    st.subheader("VaR Backtesting")

    fig_var = px.line(
        risk,
        x=risk.index,
        y=["Actual_Loss_Linear", var_column],
        title=f"Microsoft: {confidence}% VaR Backtesting"
    )

    st.plotly_chart(fig_var, use_container_width=True)

else:

    st.info(
        "GARCH-based risk analysis is currently available "
        "only for MSFT. Additional stocks will be added later."
    )
