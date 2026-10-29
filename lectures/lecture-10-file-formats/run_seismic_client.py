"""
Lecture 10: SeismicClient-ის შემოწმება —
(1) coordinate swap-ის ტესტი (mock), (2) ნამდვილი USGS მოთხოვნა ბოლო 30 დღეზე.
"""
import sys
from datetime import date, timedelta
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.ingestion.logging_config import setup_logging
from src.ingestion.seismic_client import SeismicAPIError, SeismicClient


class FakeResponse:
    def raise_for_status(self) -> None:
        pass

    def json(self) -> dict:
        return {"features": [{
            "id": "ge2026aaaa",
            "properties": {"mag": 2.3, "place": "12km SW of Tbilisi, Georgia", "time": 1787832000000},
            "geometry": {"type": "Point", "coordinates": [44.75, 41.65, 8.2]},
        }]}


def check_no_swap() -> None:
    with mock.patch("src.ingestion.seismic_client.requests.get", return_value=FakeResponse()):
        events = SeismicClient().get_recent_events("2026-08-01", "2026-08-31")
    e = events[0]
    assert e["latitude"] == 41.65 and e["longitude"] == 44.75 and e["depth_km"] == 8.2
    print(f"[OK] coordinate swap არ მოხდა: latitude={e['latitude']}, longitude={e['longitude']}, "
          f"depth={e['depth_km']} km, time={e['event_time']}")


def fetch_real() -> int:
    end = date.today()
    start = end - timedelta(days=30)
    try:
        events = SeismicClient().get_recent_events(start.isoformat(), end.isoformat(), min_magnitude=1.5)
    except SeismicAPIError as exc:
        print(f"[FAIL] {exc}")
        return 1
    print(f"[OK] USGS: {len(events)} მოვლენა ბოლო 30 დღეში (საქართველოს რეგიონი)")
    for e in events[:5]:
        print(f"     M{e['magnitude']}  {e['event_time']:%Y-%m-%d %H:%M} UTC  {e['place']}")
    return 0


def main() -> int:
    setup_logging()
    print("=== 1. Coordinate swap ტესტი (mock) ===")
    check_no_swap()
    print("\n=== 2. ნამდვილი USGS მოთხოვნა ===")
    return fetch_real()


if __name__ == "__main__":
    sys.exit(main())
