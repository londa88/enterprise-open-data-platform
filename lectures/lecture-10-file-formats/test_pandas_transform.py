"""
Lecture 10: pandas_transform.py-ის გადამოწმება — pandas-ის შედეგს ვადარებთ
stdlib csv-ით ხელით გამოთვლილს.
"""
import csv
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.ingestion.pandas_transform import compute_daily_currency_stats

CSV_PATH = ROOT / "data" / "sample" / "currency_rates_2026-08-18_2026-08-20.csv"


def manual_stats_with_stdlib(path: Path) -> dict:
    groups = defaultdict(list)
    with open(path, encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            groups[row["currency_code"]].append(float(row["rate"]))
    return {code: (round(sum(r) / len(r), 4), min(r), max(r)) for code, r in groups.items()}


def test_compute_daily_currency_stats() -> None:
    stats = compute_daily_currency_stats(str(CSV_PATH))
    assert set(stats.columns) == {"currency_code", "avg_rate", "min_rate", "max_rate"}
    assert len(stats) == 2

    manual = manual_stats_with_stdlib(CSV_PATH)
    for _, row in stats.iterrows():
        expected = manual[row["currency_code"]]
        actual = (row["avg_rate"], row["min_rate"], row["max_rate"])
        assert all(abs(a - e) < 1e-9 for a, e in zip(actual, expected)), (actual, expected)

    print(stats.to_string(index=False))
    print("[OK] pandas groupby().agg() ზუსტად იგივე შედეგს იძლევა, რაც stdlib csv-ით ხელნაწერი გამოთვლა")


if __name__ == "__main__":
    test_compute_daily_currency_stats()
