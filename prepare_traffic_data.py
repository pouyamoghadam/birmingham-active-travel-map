"""
آماده‌سازی دیتای ترافیک بیرمینگهام (DfT AADF) برای نقشه‌ی تعاملی
ورودی: dft_aadf_local_authority_id_141.csv

نحوه‌ی گرفتن ورودی:
1. برو به: https://roadtraffic.dft.gov.uk/local-authorities/E08000025
2. لینک دانلود CSV بیرمینگهام رو پیدا کن و دانلودش کن
   (یا مستقیم: https://storage.googleapis.com/dft-statistics/road-traffic/downloads/aadf/local_authority_id/dft_aadf_local_authority_id_141.csv)
3. فایل رو کنار این اسکریپت به اسم dft_aadf_local_authority_id_141.csv ذخیره کن.

اجرا: python prepare_traffic_data.py
خروجی: traffic_data.json (برای استفاده در نقشه‌ی HTML)
"""

import pandas as pd
import json

INPUT_FILE = "dft_aadf_local_authority_id_141.csv"
OUTPUT_FILE = "traffic_data.json"


def build_points_by_year(df):
    """آماده‌سازی نقاط شمارش هر سال برای رسم روی نقشه"""
    points_by_year = {}
    for year in sorted(df["year"].unique()):
        yr_data = df[df["year"] == year]
        points = []
        for _, row in yr_data.iterrows():
            points.append({
                "lat": round(row["latitude"], 5),
                "lon": round(row["longitude"], 5),
                "road": row["road_name"],
                "type": row["road_type"],
                "total": int(row["all_motor_vehicles"]),
                "hgv": int(row["all_hgvs"]),
                "cars": int(row["cars_and_taxis"]),
                "cycles": int(row["pedal_cycles"]),
            })
        points_by_year[str(int(year))] = points
    return points_by_year


def build_yearly_totals(df):
    """جمع سالانه‌ی کل بیرمینگهام برای نمودار روند"""
    yearly = df.groupby("year").agg(
        all_motor=("all_motor_vehicles", "sum"),
        cars=("cars_and_taxis", "sum"),
        hgv=("all_hgvs", "sum"),
        cycles=("pedal_cycles", "sum"),
    ).reset_index()
    return yearly.to_dict("records")


def main():
    df = pd.read_csv(INPUT_FILE)

    data = {
        "points_by_year": build_points_by_year(df),
        "yearly_totals": build_yearly_totals(df),
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)

    yearly = pd.DataFrame(data["yearly_totals"])
    y2019 = yearly[yearly["year"] == 2019]["all_motor"].values[0]
    y2024 = yearly[yearly["year"] == 2024]["all_motor"].values[0]
    pct_change = (y2024 / y2019 - 1) * 100

    print(f"تعداد نقاط شمارش: {df['count_point_id'].nunique()}")
    print(f"بازه‌ی سال: {df['year'].min()} تا {df['year'].max()}")
    print(f"ترافیک کل ۲۰۲۴: {y2024:,} وسیله نقلیه/روز")
    print(f"تغییر نسبت به ۲۰۱۹: {pct_change:.1f}%")
    print(f"خروجی در {OUTPUT_FILE} ذخیره شد.")


if __name__ == "__main__":
    main()
