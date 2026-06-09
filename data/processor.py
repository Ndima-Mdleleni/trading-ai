import pandas as pd
import numpy as np
import logging

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
