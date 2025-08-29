"""Unit tests for the IoT weather reporting project."""

from pathlib import Path

from src.simulator import simulate, write_csv
from src.api import load_latest_reading


def test_simulation_and_load_latest(tmp_path: Path) -> None:
    # Generate a small number of readings
    readings = simulate(duration_minutes=1, interval_seconds=30, seed=0)
    assert len(readings) == 2  # 1 minute / 30 sec => 2 readings
    # Write to CSV
    csv_path = tmp_path / "readings.csv"
    write_csv(readings, csv_path)
    # Load latest reading via API helper
    latest = load_latest_reading(csv_path)
    assert latest is not None
    assert "timestamp" in latest and "temperature" in latest and "humidity" in latest and "rain" in latest