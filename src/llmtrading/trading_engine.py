from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence

from .data_loader import PriceBar, slice_bars
from .dex_client import DexClient
from .llm_agent import LLMTradingAgent, MarketSummary


def moving_average(bars: Sequence[PriceBar]) -> float:
    return sum(bar.close for bar in bars) / len(bars)


def volatility(bars: Sequence[PriceBar]) -> float:
    closes = [bar.close for bar in bars]
    mean = sum(closes) / len(closes)
    variance = sum((c - mean) ** 2 for c in closes) / len(closes)
    return variance ** 0.5


def volume_trend(bars: Sequence[PriceBar]) -> float:
    first, last = bars[0], bars[-1]
    return (last.volume - first.volume) / first.volume if first.volume else 0.0


@dataclass
class BacktestResult:
    trades: List[str]
    ending_balance: float
    prompt: str


class TradingEngine:
    """Coordinate price analysis, LLM decision making, and DEX execution."""

    def __init__(self, client: DexClient, agent: LLMTradingAgent, starting_balance: float = 1000.0):
        self.client = client
        self.agent = agent
        self.balance = starting_balance
        self.position = 0.0
        self.trades: List[str] = []

    def _build_summary(self, bars: Iterable[PriceBar], short_window: int, long_window: int) -> MarketSummary:
        bar_list = list(bars)
        short_slice = slice_bars(bar_list, short_window)
        long_slice = slice_bars(bar_list, long_window)

        return MarketSummary(
            short_ma=moving_average(short_slice),
            long_ma=moving_average(long_slice),
            price=bar_list[-1].close,
            volatility=volatility(long_slice),
            volume_trend=volume_trend(long_slice),
        )

    def _execute_trade(self, decision: str, price: float) -> None:
        amount = 1.0  # base units per trade for this prototype
        if decision == "BUY" and self.balance >= amount * price:
            self.client.place_order("BUY", amount, price)
            self.balance -= amount * price
            self.position += amount
            self.trades.append(f"BUY {amount} at {price:.2f}")
        elif decision == "SELL" and self.position >= amount:
            self.client.place_order("SELL", amount, price)
            self.balance += amount * price
            self.position -= amount
            self.trades.append(f"SELL {amount} at {price:.2f}")
        else:
            self.trades.append(f"HOLD at {price:.2f}")

    def run_backtest(
        self, bars: Iterable[PriceBar], short_window: int = 3, long_window: int = 5
    ) -> BacktestResult:
        bar_list = list(bars)
        if len(bar_list) < long_window:
            raise ValueError("Not enough bars to run backtest")

        for idx in range(long_window, len(bar_list) + 1):
            window = bar_list[:idx]
            summary = self._build_summary(window, short_window, long_window)
            prompt = self.agent.build_prompt(summary)
            decision = self.agent.decide(summary)
            self._execute_trade(decision, summary.price)

        ending_balance = self.balance + self.position * bar_list[-1].close
        return BacktestResult(trades=self.trades, ending_balance=ending_balance, prompt=prompt)
