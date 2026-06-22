import sqlite3
import pandas as pd
from datetime import datetime

def get_connection():
    return sqlite3.connect("trading_results.db")


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS backtest_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_date TEXT,
            ticker TEXT,
            start_date TEXT,
            end_date TEXT,
            total_return TEXT,
            annual_return TEXT,
            sharpe_ratio TEXT,
            sortino_ratio TEXT,
            calmar_ratio TEXT,
            max_drawdown TEXT,
            win_rate TEXT,
            profit_factor TEXT,
            total_trades INTEGER,
            final_value TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER,
            date TEXT,
            action TEXT,
            price REAL,
            shares REAL,
            cash REAL,
            FOREIGN KEY (run_id) REFERENCES backtest_runs(id)
        )
    """)

    conn.commit()
    conn.close()
    print("table created successfully")

def save_results(metrics: dict, trades: pd.DataFrame, ticker: str, start: str, end: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO backtest_runs (
            run_date, ticker, start_date, end_date,
            total_return, annual_return, sharpe_ratio, sortino_ratio,
            calmar_ratio, max_drawdown, win_rate, profit_factor,
            total_trades, final_value
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        ticker,
        start,
        end,
        metrics["total_return"],
        metrics["annual_return"],
        metrics["sharpe_ratio"],
        metrics["sortino_ratio"],
        metrics["calmar_ratio"],
        metrics["max_drawdown"],
        metrics["win_rate"],
        metrics["profit_factor"],
        metrics["total_trades"],
        metrics["final_value"]
    ))

    run_id = cursor.lastrowid

    for _, trade in trades.iterrows():
        cursor.execute("""
            INSERT INTO trades (run_id, date, action, price, shares, cash)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            run_id,
            str(trade["date"]),
            trade["action"],
            float(trade["price"]),
            float(trade["shares"]),
            float(trade["cash"])
        ))

    conn.commit()
    conn.close()
    print(f"saved run {run_id} with {len(trades)} trades")
    return run_id

def query_runs():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM backtest_runs", conn)
    conn.close()
    return df

if __name__ == "__main__":
    create_tables()
    print("database ready")   

def query_trades_for_run(run_id: int):
    conn = get_connection()
    df = pd.read_sql_query(
        "SELECT * FROM trades WHERE run_id = ?",
        conn,
        params=(run_id,)
    )
    conn.close()
    return df

def query_trades_with_metrics():
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT 
            backtest_runs.ticker,
            backtest_runs.sharpe_ratio,
            backtest_runs.total_return,
            trades.date,
            trades.action,
            trades.price
        FROM trades
        JOIN backtest_runs ON trades.run_id = backtest_runs.id
    """, conn)
    conn.close()
    return df

def query_summary():
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT
            COUNT(*) as total_runs,
            AVG(CAST(total_trades AS FLOAT)) as avg_trades_per_run
        FROM backtest_runs
    """, conn)
    conn.close()
    return df

if __name__ == "__main__":
    create_tables()
    print("database ready")

    runs = query_runs()
    print("\n--- all backtest runs---")
    print(runs[["id", "run_date", "ticker", "sharpe_ratio", "total_return"]])

    trades = query_trades_for_run(1)
    print("\n-- trades for run 1 ---")
    print(trades)
 
    joined = query_trades_with_metrics()
    print("\n--- joined trades + metrics ---")
    print(joined)

    summary = query_summary()
    print("\n--- summary stats ---")
    print(summary)