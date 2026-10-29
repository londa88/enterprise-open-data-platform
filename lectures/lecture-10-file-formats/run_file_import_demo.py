"""
Lecture 10 lab: File Import Engine-ის დემონსტრაცია —
CSV/XML/JSON წაკითხვა და ვალიდაციის ჩავარდნა.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.ingestion.file_import import FileImportError, read_csv, read_json, read_xml
from src.ingestion.logging_config import setup_logging

SAMPLE_DIR = ROOT / "data" / "sample"
CSV_PATH = SAMPLE_DIR / "currency_rates_2026-08-27.csv"


def main() -> int:
    setup_logging()

    print("=== წარმატებული წაკითხვა ===")
    try:
        csv_rows = read_csv(CSV_PATH, required_columns=["currency_code", "rate", "rate_date"])
        print(f"[OK] CSV: {len(csv_rows)} row, პირველი: {csv_rows[0]}")

        xml_rows = read_xml(SAMPLE_DIR / "weather_forecast_2026-08-27.xml")
        print(f"[OK] XML: {len(xml_rows)} ჩანაწერი, პირველი: {xml_rows[0]}")

        geo_data = read_json(SAMPLE_DIR / "earthquakes_sample.geojson")
        print(f"[OK] GeoJSON: {len(geo_data['features'])} feature")
    except FileImportError as exc:
        print(f"[FAIL] {exc}")
        return 1

    print("\n=== ვალიდაციის ჩავარდნა (არარსებული სვეტი) ===")
    try:
        read_csv(CSV_PATH, required_columns=["currency_code", "nonexistent_column"])
        print("[FAIL] ვალიდაცია უნდა ჩავარდნილიყო!")
        return 1
    except FileImportError as exc:
        print(f"[OK] ვალიდაცია სწორად ჩავარდა: {exc}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
