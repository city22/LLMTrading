from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import csv
from typing import Iterable, List


@dataclass
class PriceBar:
    """Represents an OHLCV bar for a single trading interval."""

    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


def _parse_row(row: dict[str, str]) -> PriceBar:
    return PriceBar(
        timestamp=datetime.fromisoformat(row["timestamp"].replace("Z", "+00:00")),
        open=float(row["open"]),
        high=float(row["high"]),
        low=float(row["low"]),
        close=float(row["close"]),
        volume=float(row["volume"]),
    )


def load_price_bars(path: str | Path) -> List[PriceBar]:
    """Load OHLCV bars from a CSV file.

    Args:
        path: Path to a CSV file with columns timestamp, open, high, low, close, volume.

    Returns:
        List of :class:`PriceBar` objects sorted by timestamp ascending.
    """

    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Price history file not found: {file_path}")

    with file_path.open(newline="") as fh:
        reader = csv.DictReader(fh)
        rows = [_parse_row(row) for row in reader]

    return sorted(rows, key=lambda bar: bar.timestamp)


def slice_bars(bars: Iterable[PriceBar], window: int) -> List[PriceBar]:
    """Return the last *window* bars from an iterable collection."""

    recent = list(bars)[-window:]
    if len(recent) < window:
        raise ValueError(f"Not enough bars to calculate window={window}")
    return recent
