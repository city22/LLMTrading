from __future__ import annotations

import argparse
from pathlib import Path

from .data_loader import load_price_bars
from .dex_client import DexClient
from .llm_agent import LLMTradingAgent
from .trading_engine import TradingEngine


def main() -> None:
    parser = argparse.ArgumentParser(description="Simulate an LLM-driven DEX trading loop")
    parser.add_argument("--data", type=Path, default=Path("data/price_history.csv"), help="Path to OHLCV CSV file")
    parser.add_argument("--base", default="ETH", help="Base asset symbol")
    parser.add_argument("--quote", default="USDC", help="Quote asset symbol")
    parser.add_argument("--starting-balance", type=float, default=1000.0, help="Starting quote balance")
    parser.add_argument("--short-window", type=int, default=3, help="Short moving average window")
    parser.add_argument("--long-window", type=int, default=5, help="Long moving average window")
    args = parser.parse_args()

    bars = load_price_bars(args.data)
    agent = LLMTradingAgent()
    client = DexClient(base_symbol=args.base, quote_symbol=args.quote)
    engine = TradingEngine(client=client, agent=agent, starting_balance=args.starting_balance)

    result = engine.run_backtest(bars, short_window=args.short_window, long_window=args.long_window)

    print(f"Executed {len(result.trades)} decisions on {len(bars)} bars")
    for trade in result.trades:
        print(f"- {trade}")
    print(f"\nPrompt sent to LLM:\n{result.prompt}\n")
    print(f"Ending balance (mark-to-market): {result.ending_balance:.2f} {args.quote}")


if __name__ == "__main__":
    main()
