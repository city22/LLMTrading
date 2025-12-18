from __future__ import annotations

from dataclasses import dataclass
from textwrap import dedent


@dataclass
class MarketSummary:
    """Lightweight market context for the LLM agent."""

    short_ma: float
    long_ma: float
    price: float
    volatility: float
    volume_trend: float


class LLMTradingAgent:
    """A lightweight, deterministic stand-in for an LLM decision maker."""

    def __init__(self, buy_threshold: float = 0.35, sell_threshold: float = -0.35):
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold

    def build_prompt(self, summary: MarketSummary) -> str:
        """Compose a prompt that would be sent to a real LLM."""

        return dedent(
            f"""
            You are an LLM-based crypto trading assistant. Given the latest market
            summary decide whether to BUY, SELL or HOLD. Consider momentum (short
            vs long moving average), volatility, and the recent change in
            on-chain volume. Avoid unnecessary trades when signals conflict.

            - Short MA: {summary.short_ma:.2f}
            - Long MA: {summary.long_ma:.2f}
            - Latest Close: {summary.price:.2f}
            - Volatility: {summary.volatility:.4f}
            - Volume Trend: {summary.volume_trend:.4f}
            """
        ).strip()

    def score_summary(self, summary: MarketSummary) -> float:
        """Score the market state to emulate a small reasoning step."""

        momentum = summary.short_ma - summary.long_ma
        volatility_penalty = -abs(summary.volatility) * 0.1
        volume_bonus = summary.volume_trend * 0.25
        return momentum + volatility_penalty + volume_bonus

    def decide(self, summary: MarketSummary) -> str:
        """Return BUY, SELL or HOLD based on the synthetic score."""

        score = self.score_summary(summary)
        if score >= self.buy_threshold:
            return "BUY"
        if score <= self.sell_threshold:
            return "SELL"
        return "HOLD"
