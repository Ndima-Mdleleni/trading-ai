import yfinance as yf
import pandas as pd
from config import config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_ohlcv(
        ticker: str = None,
        start: str = None,
        end: str = None,
        interval: str = None
) -> pd.DataFrame:
    """
    Fetch Open High Low Close Volume data from Yahoo Finance.
    Falls back to config values if parameters not provided.
    """
    ticker = ticker  or config.data.ticker
    start = start    or config.data.start_date
    end = end        or config.data.end_date
    interval = interval or config.data.interval

    logger.info(f"fetching {ticker} from {start} to {end}")

    raw = yf.download(
        tickers=ticker,
        start=start,
        end=end,
        interval=interval,
        auto_adjust=True,
        progress=False
    )

    if raw.empty:
        raise ValueError(f"no data returned for {ticker}")
    
    if isinstance(raw.columns, pd.MultiIndex):
        raw.columns = raw.columns.get_level_values(0)
        
    raw.index = pd.to_datetime(raw.index)    
    raw.sort_index(inplace=True)

    logger.info(f"fetched {len(raw)} rows")
    return raw

if __name__ == "__main__":
    df = fetch_ohlcv()
    print(df.tail())
    print(f"\nshape: {df.shape}")
    print(f"columns: {list(df.columns)}")

