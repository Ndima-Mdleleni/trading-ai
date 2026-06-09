# main.py
# Entry point for the full trading AI pipeline
# Run this to execute the complete pipeline end to end

import logging
from data.fetcher import fetch_ohlcv
from data.processor import process
from signals.indicators import add_indicators
from signals.generator import generate_signals
from backtest.engine import run_backtest
from backtest.metrics import calculate_metrics
from report.generator import print_report

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(name)s — %(levelname)s — %(message)s"
)

logger = logging.getLogger(__name__)


def run_pipeline():
    logger.info("starting trading pipeline")

    # 1. fetch data
    df = fetch_ohlcv()

    # 2. process and clean
    df = process(df)

    # 3. add indicators
    df = add_indicators(df)

    # 4. generate signals
    df = generate_signals(df)

    # 5. run backtest
    df, trades = run_backtest(df)

    # 6. calculate metrics
    metrics = calculate_metrics(df, trades)

    # 7. print report
    print_report(metrics, trades)

    logger.info("pipeline complete")
    return df, trades, metrics


if __name__ == "__main__":
    run_pipeline()