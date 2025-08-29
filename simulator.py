"""Simulate sensor readings for an IoT weather station.

This script generates synthetic temperature, humidity and rain data
at fixed intervals over a specified duration.  The output is
written to a CSV file with a timestamp column.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict

import numpy as np


def simulate(duration_minutes: int, interval_seconds: int, seed: int | None = None) -> List[Dict[str, any]]:
    """Generate a list of sensor readings.

    Parameters
    ----------
    duration_minutes:
        Total simulation time in minutes.
    interval_seconds:
        Time step between readings in seconds.
    seed:
        Optional random seed.

    Returns
    -------
    list of dict
        Each dict contains timestamp (ISO string), temperature (°C), humidity (%) and rain (0 or 1).
    """
    rng = np.random.default_rng(seed)
    readings = []
    start_time = datetime.utcnow()
    total_steps = int(duration_minutes * 60 / interval_seconds)
    for step in range(total_steps):
        timestamp = start_time + timedelta(seconds=step * interval_seconds)
        # Generate temperature around 20°C with small random fluctuation
        temperature = 20 + rng.normal(0, 2)
        # Generate humidity between 30% and 90%
        humidity = rng.uniform(30, 90)
        # Generate rain event with low probability
        rain = int(rng.random() < 0.1)
        readings.append(
            {
                "timestamp": timestamp.isoformat(timespec="seconds") + "Z",
                "temperature": round(float(temperature), 2),
                "humidity": round(float(humidity), 2),
                "rain": rain,
            }
        )
    return readings


def write_csv(readings: List[Dict[str, any]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "temperature", "humidity", "rain"])
        writer.writeheader()
        writer.writerows(readings)


def main() -> None:
    parser = argparse.ArgumentParser(description="Simulate IoT weather sensor readings.")
    parser.add_argument(
        "--duration",
        type=int,
        default=120,
        help="Duration of simulation in minutes.",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=60,
        help="Interval between readings in seconds.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=str(Path(__file__).resolve().parents[1] / "data" / "readings.csv"),
        help="Path to output CSV file.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducibility.",
    )
    args = parser.parse_args()
    readings = simulate(args.duration, args.interval, seed=args.seed)
    output_path = Path(args.output)
    write_csv(readings, output_path)
    print(f"Generated {len(readings)} readings to {output_path}")


if __name__ == "__main__":
    main()