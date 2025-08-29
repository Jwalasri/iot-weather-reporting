"""FastAPI application to serve IoT weather sensor readings."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd
from fastapi import FastAPI, HTTPException


DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "readings.csv"


app = FastAPI(title="IoT Weather API", version="0.1.0")


def load_latest_reading(path: Path = DATA_FILE) -> Optional[dict]:
    """Load the most recent sensor reading from the CSV file.

    Returns None if the file does not exist or is empty.
    """
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        return None
    if df.empty:
        return None
    # Use last row
    row = df.iloc[-1]
    return {
        "timestamp": row["timestamp"],
        "temperature": float(row["temperature"]),
        "humidity": float(row["humidity"]),
        "rain": int(row["rain"]),
    }


@app.get("/latest")
def latest() -> dict:
    """Return the latest sensor reading as JSON."""
    reading = load_latest_reading()
    if reading is None:
        raise HTTPException(status_code=404, detail="No sensor data available")
    return reading