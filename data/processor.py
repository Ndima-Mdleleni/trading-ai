import pandas as pd
import numpy as np
import logging
from scipy import stats

logger = logging.getLogger(__name__)

def process(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and prepare raw OHLCV data.
    - removes nulls
    - adds returns and log returns
    - adds rolling volatility
    - validates data quality
    """
    df = df.copy()

    before = len(df)
    df.dropna(inplace=True)
    after = len(df)
    if before != after:
        logger.warning(f"dropped {before - after} rows with nulls")

    required = ["Open", "High", "Low", "Close", "Volume"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"missing required columns: {missing}")
    
    df["returns"]         = df["Close"].pct_change()

    df["log_returns"]     = np.log(df["Close"] / df["Close"].shift(1))

    df["volatility"]      = df["returns"].rolling(20).std() * np.sqrt(252)

    df.dropna(inplace=True)

    logger.info(f"processed {len(df)} rows")
    return df

if __name__ == "__main__":
    from data.fetcher import fetch_ohlcv
    raw        = fetch_ohlcv()
    processed  = process(raw)
    print(processed[["Close", "returns", "log_returns", "volatility"]].tail())
    print("lag 1:", processed["returns"].autocorr(lag=1))
    print("lag 2:", processed["returns"].autocorr(lag=2))
    print("lag 3:", processed["returns"].autocorr(lag=3))
    print("lag 5:", processed["returns"].autocorr(lag=5))
    processed["day_of_week"] = processed.index.day_name()
    print(processed.groupby("day_of_week")["returns"].mean())
    monday_returns = processed[processed["day_of_week"] == "Monday"]["returns"]
    t_stat, p_value = stats.ttest_1samp(monday_returns, 0)
    print(f"t-stat: {t_stat:.3f}, p-value: {p_value:.3f}")