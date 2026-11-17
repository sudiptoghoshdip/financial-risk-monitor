# Financial Risk and Volatility Monitor

An interactive financial risk analytics dashboard built with
Python and Streamlit.

## Overview

This project applies financial econometric methods to analyze
equity market volatility and evaluate market risk.

## Features

- Historical stock price visualization
- Daily log return analysis
- Annualized rolling volatility
- GARCH-based Value at Risk (VaR)
- Expected Shortfall (ES)
- VaR backtesting and violation analysis

## Methodology

Daily equity returns are calculated using adjusted closing prices.

A GARCH(1,1) model is used to estimate conditional volatility
and generate one-day-ahead variance forecasts.

These forecasts are used to calculate 95% and 99% VaR and
Expected Shortfall under a Gaussian innovation assumption.

VaR performance is evaluated using historical violations.

## Technologies

Python, pandas, NumPy, Plotly, Streamlit, arch.

## Limitations

- GARCH-based risk estimates are currently available for MSFT.
- The dashboard uses saved data rather than live market updates.
- Gaussian VaR may underestimate extreme market losses.
- Risk estimates are illustrative and not investment advice.