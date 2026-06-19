# report/generator.py
# Generates a clean performance report
# Single responsibility: format and display results

import pandas as pd
import logging

logger = logging.getLogger(__name__)


def print_report(metrics: dict, trades: pd.DataFrame) -> None:
    """
    Print a clean formatted performance report.
    """
    width = 50

    print("\n" + "=" * width)
    print(" TRADING STRATEGY PERFORMANCE REPORT")
    print("=" * width)

    print("\n📊 RETURNS")
    print(f"  Final Portfolio Value : {metrics['final_value']}")
    print(f"  Total Return          : {metrics['total_return']}")
    print(f"  Annualised Return     : {metrics['annual_return']}")

    print("\n📉 RISK")
    print(f"  Sharpe Ratio          : {metrics['sharpe_ratio']}")
    print(f"   Sortino Ratio        : {metrics['sortino_ratio']}")
    print(f"  Calmar Ratio          : {metrics['calmar_ratio']}")
    print(f"  Max Drawdown          : {metrics['max_drawdown']}")

    print("\n🎯 TRADE QUALITY")
    print(f"  Total Trades          : {metrics['total_trades']}")
    print(f"  Win Rate              : {metrics['win_rate']}")
    print(f"  Profit Factor         : {metrics['profit_factor']}")

    print("\n📋 TRADE LOG")
    print(trades.to_string(index=False))

    print("\n" + "=" * width)

    # simple assessment
    sharpe = float(metrics['sharpe_ratio'])
    if sharpe >= 1.5:
        verdict = "✅ STRONG — deploy with caution"
    elif sharpe >= 1.0:
        verdict = "⚠️  MODERATE — needs improvement"
    else:
        verdict = "❌ WEAK — do not deploy"

    print(f" VERDICT: {verdict}")
    print("=" * width + "\n")