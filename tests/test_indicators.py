import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import pandas as pd
from app.indicators import calculate_indicators


def test_calculate_indicators_basic():
    dates = pd.date_range("2023-01-01", periods=40, freq="D")
    close = pd.Series(range(1, 41))
    df = pd.DataFrame({"Date": dates, "Close": close, "Open": close, "High": close, "Low": close, "Volume": close})

    result = calculate_indicators(df)

    # On day 30 (index 29) SMA should be mean of 1..30 = 15.5
    sma_day30 = result.loc[29, "sma30"]
    assert abs(sma_day30 - 15.5) < 1e-6
    pos = result.loc[39, "suggested"]
    assert pos in {"long", "short", "cash"}
