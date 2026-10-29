"""
Lecture 9: custom retry.py-ის ეკვივალენტი tenacity ბიბლიოთეკით —
იგივე ქცევა (3 ცდა, exponential backoff 1s → 2s → 4s).
"""
import logging
import sys
import time
from unittest import mock

import requests
from tenacity import (before_sleep_log, retry, retry_if_exception_type,
                      stop_after_attempt, wait_exponential)

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger("tenacity_demo")

BASE_URL = "https://api.open-meteo.com/v1/forecast"


@retry(
    retry=retry_if_exception_type(requests.exceptions.RequestException),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=8),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    reraise=True,
)
def get_with_tenacity(params: dict) -> requests.Response:
    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()
    return response


def main() -> int:
    calls = {"n": 0}

    class FakeResponse:
        def raise_for_status(self) -> None:
            pass

    def flaky_get(url, params=None, timeout=None):
        calls["n"] += 1
        if calls["n"] <= 2:
            raise requests.exceptions.ConnectionError("simulated glitch")
        return FakeResponse()

    print("=== tenacity: 2 ჩავარდნა → success ===")
    start = time.perf_counter()
    with mock.patch("requests.get", side_effect=flaky_get):
        get_with_tenacity({})
    print(f"[OK] სულ დრო: {time.perf_counter() - start:.1f}s, სულ ცდა: {calls['n']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
