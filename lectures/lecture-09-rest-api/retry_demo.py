"""
Lecture 9: Retry მექანიზმის შემოწმება — API-ს დროებითი/მუდმივი შეცდომის სიმულაცია
unittest.mock-ით (ნამდვილი ქსელი არ გამოიყენება).
"""
import sys
import time
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import requests

from src.ingestion.logging_config import setup_logging
from src.ingestion.weather_client import WeatherAPIError, WeatherClient


class FakeResponse:
    def raise_for_status(self) -> None:
        pass

    def json(self) -> dict:
        return {"current": {"temperature_2m": 24.3, "wind_speed_10m": 8.1}}


def make_flaky_get(fail_times: int, message: str):
    calls = {"n": 0}

    def flaky_get(url, params=None, timeout=None):
        calls["n"] += 1
        if calls["n"] <= fail_times:
            raise requests.exceptions.ConnectionError(message)
        return FakeResponse()

    return flaky_get, calls


def run_scenario(title: str, fail_times: int, message: str) -> None:
    print(f"\n=== {title} ===")
    flaky_get, calls = make_flaky_get(fail_times, message)
    start = time.perf_counter()
    with mock.patch("src.ingestion.weather_client.requests.get", side_effect=flaky_get):
        try:
            WeatherClient().get_current_weather()
            print("[OK] საბოლოოდ წარმატებით დასრულდა")
        except WeatherAPIError as exc:
            print(f"[OK] WeatherAPIError სწორად დაიჭირა: {exc}")
    print(f"სულ დრო: {time.perf_counter() - start:.1f}s, სულ ცდა: {calls['n']}")


def main() -> int:
    setup_logging()
    run_scenario("სცენარი 1: დროებითი შეცდომა (2 ჩავარდნა → success)", 2, "simulated glitch")
    run_scenario("სცენარი 2: მუდმივი შეცდომა (ყველა ცდა ამოწურულია)", 99, "permanent glitch")
    return 0


if __name__ == "__main__":
    sys.exit(main())
