"""Plot sensor readings from the IoT weather station simulator.

Given a CSV file produced by ``simulator.py``, this script generates
line plots for temperature, humidity and rain over time and saves
them as a PNG file.
"""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

import matplotlib
matplotlib.use('Agg')  # Use non‑interactive backend
import matplotlib.pyplot as plt
import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot IoT weather sensor readings.")
    parser.add_argument("--input", type=str, required=True, help="Path to the CSV readings file.")
    parser.add_argument(
        "--output",
        type=str,
        default=str(Path(__file__).resolve().parents[1] / "plots" / "weather.png"),
        help="Path to save the output plot.",
    )
    args = parser.parse_args()
    df = pd.read_csv(args.input)
    # Convert timestamp strings to datetime objects for plotting
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    # Create figure with multiple axes
    fig, ax1 = plt.subplots(figsize=(8, 6))
    ax1.set_title("IoT Weather Sensor Readings")
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Temperature (°C)", color="tab:red")
    ax1.plot(df["timestamp"], df["temperature"], color="tab:red", label="Temperature")
    ax1.tick_params(axis='y', labelcolor="tab:red")
    # Create second y axis for humidity
    ax2 = ax1.twinx()
    ax2.set_ylabel("Humidity (%)", color="tab:blue")
    ax2.plot(df["timestamp"], df["humidity"], color="tab:blue", label="Humidity")
    ax2.tick_params(axis='y', labelcolor="tab:blue")
    # Plot rain as bar chart on secondary axis but scaled to 0-1
    ax3 = ax1.twinx()
    # Offset the right spine
    ax3.spines.right.set_position(("axes", 1.1))
    ax3.set_ylabel("Rain", color="tab:green")
    ax3.plot(df["timestamp"], df["rain"], color="tab:green", linestyle="--", label="Rain")
    ax3.tick_params(axis='y', labelcolor="tab:green")
    # Rotate x labels for readability
    fig.autofmt_xdate()
    # Create legend
    lines, labels = [], []
    for ax in [ax1, ax2, ax3]:
        line, label = ax.get_legend_handles_labels()
        lines += line
        labels += label
    fig.legend(lines, labels, loc="upper right")
    # Save figure
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, bbox_inches="tight")
    print(f"Plot saved to {output_path}")


if __name__ == "__main__":
    main()