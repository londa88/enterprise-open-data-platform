"""SCD2-ის 3 სცენარის ტესტი: პირველი ჩანაწერი, ცვლილების გარეშე, რეალური ცვლილება."""
from scd2 import scd2_upsert

KEY = "city"
TRACKED = ["latitude", "longitude", "population_category"]
base = {"city": "Tbilisi", "latitude": 41.7151, "longitude": 44.8271,
        "population_category": "large"}

# Test 1: პირველი ვერსია
rows = scd2_upsert([], base, KEY, TRACKED, "2026-01-01")
assert len(rows) == 1 and rows[0]["is_current"] is True
print("Test 1:", rows[0])

# Test 2: იგივე მონაცემი — არაფერი უნდა შეიცვალოს
rows2 = scd2_upsert(rows, dict(base), KEY, TRACKED, "2026-06-01")
assert rows2 == rows
print(f"Test 2: row-ების რაოდენობა უცვლელია ({len(rows2)}) — ცვლილება არ დაფიქსირდა")

# Test 3: რეალური ცვლილება — ძველი იხურება, ახალი ემატება
changed = {**base, "population_category": "mega"}
rows3 = scd2_upsert(rows2, changed, KEY, TRACKED, "2026-09-01")
old, new = rows3
assert len(rows3) == 2
assert old["is_current"] is False and old["valid_to"] == "2026-09-01"
assert new["is_current"] is True and new["valid_from"] == "2026-09-01"
print("Test 3:")
print("  ", old)
print("  ", new)

print("\n[OK] ყველა 3 სცენარი (პირველი ჩანაწერი, ცვლილების გარეშე, რეალური ცვლილება) სწორად მუშაობს")
