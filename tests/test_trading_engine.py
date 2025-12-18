from llmtrading.data_loader import load_price_bars
from llmtrading.dex_client import DexClient
from llmtrading.llm_agent import LLMTradingAgent
from llmtrading.trading_engine import TradingEngine, moving_average, volatility, volume_trend


def test_indicators_compute_expected_values():
    bars = load_price_bars("data/price_history.csv")[:5]
    assert round(moving_average(bars), 2) == 109.80
    assert round(volatility(bars), 4) == 4.1183
    assert round(volume_trend(bars), 4) == 0.4167


def test_backtest_runs_and_generates_trades():
    bars = load_price_bars("data/price_history.csv")
    agent = LLMTradingAgent()
    client = DexClient(base_symbol="ETH", quote_symbol="USDC")
    engine = TradingEngine(client=client, agent=agent, starting_balance=1000.0)

    result = engine.run_backtest(bars, short_window=3, long_window=5)

    assert len(result.trades) == len(bars) - 4
    # Deterministic outcome given the synthetic scoring.
    assert result.trades[0].startswith("BUY")
    assert result.ending_balance > 0
