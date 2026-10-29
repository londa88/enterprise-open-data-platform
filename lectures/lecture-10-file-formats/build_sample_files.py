"""
Lecture 10: sample CSV/XML ფაილების გენერაცია (File Naming Conventions:
<წყარო>_<თარიღი>.<გაფართოება>).
"""
import csv
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SAMPLE_DIR = ROOT / "data" / "sample"

CURRENCY_ROWS = [
    {"currency_code": "USD", "quantity": "1", "rate": "2.6512", "rate_date": "2026-08-27"},
    {"currency_code": "EUR", "quantity": "1", "rate": "2.9284", "rate_date": "2026-08-27"},
]

# მრავალდღიანი ისტორია pandas-ის აგრეგაციისთვის (იგივე მნიშვნელობები, რაც Lab 5-ში)
CURRENCY_HISTORY_ROWS = [
    {"currency_code": "USD", "quantity": "1", "rate": "2.6480", "rate_date": "2026-08-18"},
    {"currency_code": "USD", "quantity": "1", "rate": "2.6502", "rate_date": "2026-08-19"},
    {"currency_code": "USD", "quantity": "1", "rate": "2.6455", "rate_date": "2026-08-20"},
    {"currency_code": "EUR", "quantity": "1", "rate": "2.9150", "rate_date": "2026-08-18"},
    {"currency_code": "EUR", "quantity": "1", "rate": "2.9180", "rate_date": "2026-08-19"},
    {"currency_code": "EUR", "quantity": "1", "rate": "2.9210", "rate_date": "2026-08-20"},
]

WEATHER_ROWS = [
    {"city": "Tbilisi", "forecast_time": "2026-08-27T12:00:00+00", "temperature_c": "28.3"},
    {"city": "Tbilisi", "forecast_time": "2026-08-27T13:00:00+00", "temperature_c": "29.2"},
]


def write_csv(path: Path, rows: list) -> Path:
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return path


def build_weather_xml() -> Path:
    path = SAMPLE_DIR / "weather_forecast_2026-08-27.xml"
    root = ET.Element("forecasts")
    for row in WEATHER_ROWS:
        record = ET.SubElement(root, "forecast")
        for key, value in row.items():
            field = ET.SubElement(record, key)
            field.text = value
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)
    return path


if __name__ == "__main__":
    SAMPLE_DIR.mkdir(parents=True, exist_ok=True)
    paths = [
        write_csv(SAMPLE_DIR / "currency_rates_2026-08-27.csv", CURRENCY_ROWS),
        write_csv(SAMPLE_DIR / "currency_rates_2026-08-18_2026-08-20.csv", CURRENCY_HISTORY_ROWS),
        build_weather_xml(),
    ]
    for p in paths:
        print(f"[OK] {p.relative_to(ROOT)}")
