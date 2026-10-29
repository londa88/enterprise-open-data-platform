"""
Lecture 10 (დამატება): pandas-ით ცხრილური ტრანსფორმაცია — CSV-დან
სვეტურ აგრეგაციამდე, რაც stdlib csv-ს მარტივად არ გააჩნია.
"""
import pandas as pd


def compute_daily_currency_stats(csv_path: str) -> pd.DataFrame:
    """თითო ვალუტის საშუალო/მინიმალური/მაქსიმალური კურსი — groupby().agg() ერთ ხაზში."""
    df = pd.read_csv(csv_path, encoding="utf-8-sig")
    stats = (
        df.groupby("currency_code")["rate"]
        .agg(["mean", "min", "max"])
        .round(4)
        .reset_index()
        .rename(columns={"mean": "avg_rate", "min": "min_rate", "max": "max_rate"})
    )
    return stats
