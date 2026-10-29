"""
Lecture 10: xml_validator.py-ის გადამოწმება — სწორი და არასრული XML.
"""
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.ingestion.xml_validator import XMLSchemaValidationError, validate_against_schema

XSD = ROOT / "data" / "schemas" / "weather_forecast.xsd"
VALID_XML = ROOT / "data" / "sample" / "weather_forecast_2026-08-27.xml"

# temperature_c აკლია — სქემის მიხედვით სავალდებულოა
INCOMPLETE_XML = """<?xml version='1.0' encoding='utf-8'?>
<forecasts>
  <forecast>
    <city>Tbilisi</city>
    <forecast_time>2026-08-27T12:00:00+00</forecast_time>
  </forecast>
</forecasts>
"""


def test_valid() -> None:
    validate_against_schema(str(VALID_XML), str(XSD))
    print("[OK] სწორი XML გავიდა ვალიდაციას")


def test_incomplete() -> None:
    path = Path(tempfile.gettempdir()) / "weather_incomplete.xml"
    path.write_text(INCOMPLETE_XML, encoding="utf-8")
    try:
        validate_against_schema(str(path), str(XSD))
        raise AssertionError("არასრული XML ვალიდაციას არ უნდა გასულიყო")
    except XMLSchemaValidationError as exc:
        print(f"[OK] სწორად დაიჭირა არასრული XML: {exc}")


if __name__ == "__main__":
    test_valid()
    test_incomplete()
