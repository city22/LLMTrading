# LLMTrading

A lightweight prototype that simulates an LLM-guided trading loop on a decentralized exchange. The project includes a simple CLI, deterministic "LLM" agent, and a backtest harness using sample OHLCV data.

## Getting started

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Run the backtest with the included sample data:

```bash
PYTHONPATH=src python -m llmtrading.cli --data data/price_history.csv --base ETH --quote USDC
```

## Project layout

- `data/price_history.csv`: Sample OHLCV data used for quick simulations.
- `src/llmtrading`: Package code for the CLI, LLM agent stub, DEX client, and trading engine.
- `tests/`: Pytest suite covering indicator math and the backtest loop.

## Notes

The LLM agent is deterministic and does not call external APIs. It uses moving-average momentum, volume trend, and volatility to decide BUY/SELL/HOLD actions, producing the prompt that would otherwise be sent to a real LLM.
