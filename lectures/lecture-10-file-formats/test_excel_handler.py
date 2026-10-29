"""
Lecture 10: excel_handler.py-ის გადამოწმება — round-trip და 2 ჩავარდნის სცენარი.
"""
import sys
import tempfile
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.ingestion.excel_handler import ExcelImportError, read_excel, write_excel

TMP = Path(tempfile.gettempdir())


def test_round_trip() -> None:
    path = TMP / "test_round_trip.xlsx"
    original = pd.DataFrame({"currency_code": ["USD", "EUR"], "rate": [2.6479, 2.9180]})
    write_excel(original, str(path))
    read_back = read_excel(str(path))
    pd.testing.assert_frame_equal(read_back, original, check_dtype=False)
    print("[OK] round-trip სწორია — ჩაწერილი და წაკითხული მონაცემი იდენტურია")


def test_missing_required_column() -> None:
    path = TMP / "test_missing_col.xlsx"
    write_excel(pd.DataFrame({"currency_code": ["USD"], "rate": [2.6479]}), str(path))
    try:
        read_excel(str(path), required_columns={"nonexistent_column"})
        raise AssertionError("უნდა ატყორცნოს ExcelImportError")
    except ExcelImportError as exc:
        print(f"[OK] სწორად დაიჭირა: {exc}")


def test_file_not_found() -> None:
    path = TMP / "does_not_exist.xlsx"
    try:
        read_excel(str(path))
        raise AssertionError("უნდა ატყორცნოს ExcelImportError")
    except ExcelImportError as exc:
        print(f"[OK] სწორად დაიჭირა: {exc}")


if __name__ == "__main__":
    test_round_trip()
    test_missing_required_column()
    test_file_not_found()
