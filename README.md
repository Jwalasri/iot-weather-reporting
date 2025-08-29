# IoT Weather Reporting

Simulate a low‑cost IoT weather station using DHT11 and rain sensors. Logs temperature, humidity, and rain data; generates charts; and exposes a FastAPI endpoint for retrieving the latest reading.

## Problem → Approach → Results → Next Steps

- **Problem.** Local weather reporting hardware can be expensive or overkill for simple sensor setups.
- **Approach.** Built a simulator for DHT11 temperature/humidity sensor and a basic rain sensor. The simulator generates minute‑level readings; a FastAPI endpoint (`/latest`) returns the most recent reading; and a plotting script produces line charts of recent data. The code includes a stub to swap in actual Raspberry Pi sensor reads.
- **Results.** Generates stable 120‑minute traces with clear plots. The API responds in milliseconds locally. The project is structured for deployment on a Raspberry Pi with minimal changes.
- **Next steps.** Replace the simulator with real DHT11 and rain sensor code; persist data to SQLite or TimescaleDB; build a Grafana dashboard; and add threshold‑based alerts.

## Installation

```bash
git clone https://github.com/yourname/iot-weather-reporting.git
cd iot-weather-reporting
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Running the Simulator

```bash
python src/simulator.py --duration 120 --interval 60 --output data/readings.csv
```

This command runs the simulator for 120 minutes, producing readings every 60 seconds.

## Plotting Data

```bash
python src/plot.py --input data/readings.csv --output plots/weather.png
```

## Running the API

Start the FastAPI server:

```bash
uvicorn src.api:app --reload
```

Access the latest reading at `http://localhost:8000/latest`.

## Project Structure

```
iot-weather-reporting/
├── src/
│   ├── simulator.py
│   ├── api.py
│   └── plot.py
├── data/
├── plots/
├── tests/
├── requirements.txt
├── .gitignore
├── .github/workflows/python-ci.yml
├── LICENSE
└── README.md
```

## Contributing

Contributions are welcome! Please open an issue for bug reports or feature requests.

## License

This project is licensed under the MIT License.