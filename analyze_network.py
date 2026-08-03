"""
تحلیل شبکه‌ی دوچرخه‌سواری/پیاده‌روی بیرمینگهام
ورودی: export.geojson (خروجی Overpass Turbo)
خروجی: آمار دسته‌بندی، طول هر نوع زیرساخت، و نقاط گسست شبکه

نحوه‌ی گرفتن ورودی:
1. برو به overpass-turbo.eu
2. این کوئری رو اجرا کن:
   [out:json][timeout:90];
   (
     way["highway"="cycleway"](52.4650,-1.9450,52.4950,-1.8850);
     way["cycleway"](52.4650,-1.9450,52.4950,-1.8850);
     way["highway"="path"]["bicycle"](52.4650,-1.9450,52.4950,-1.8850);
     way["highway"="footway"]["foot"="designated"](52.4650,-1.9450,52.4950,-1.8850);
   );
   out geom;
3. Export > GeoJSON رو دانلود کن و به‌عنوان export.geojson کنار این اسکریپت بذار.

اجرا: python analyze_network.py
"""

import json
import math

INPUT_FILE = "export.geojson"
OUTPUT_STATS_FILE = "network_stats.json"
GAP_DISTANCE_THRESHOLD_M = 40   # فاصله‌ای که بیشترش نقطه‌ی گسست محسوب می‌شه
EDGE_BUFFER_DEG = 0.0015        # برای حذف نقاط نزدیک لبه‌ی bbox (حدود 150-170 متر)
BBOX = (52.4650, -1.9450, 52.4950, -1.8850)  # south, west, north, east


def haversine(a, b):
    """فاصله‌ی دو نقطه‌ی جغرافیایی به متر (a و b به‌صورت [lon, lat])"""
    R = 6371000
    phi1, phi2 = math.radians(a[1]), math.radians(b[1])
    dphi = math.radians(b[1] - a[1])
    dlambda = math.radians(b[0] - a[0])
    x = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.asin(math.sqrt(x))


def way_length(coords):
    """طول کل یک LineString بر حسب متر"""
    return sum(haversine(coords[i], coords[i + 1]) for i in range(len(coords) - 1))


def categorize(props):
    """دسته‌بندی یک فیچر بر اساس تگ‌های OSM"""
    if props.get("highway") == "cycleway":
        return "segregated"
    if props.get("cycleway") and props.get("cycleway") != "no":
        return "roadside"
    if props.get("highway") == "path" and props.get("bicycle"):
        return "shared"
    if props.get("highway") == "footway" and props.get("foot") == "designated":
        return "footway"
    return "other"


def near_edge(pt):
    lon, lat = pt[0], pt[1]
    return (
        abs(lat - BBOX[0]) < EDGE_BUFFER_DEG or abs(lat - BBOX[2]) < EDGE_BUFFER_DEG or
        abs(lon - BBOX[1]) < EDGE_BUFFER_DEG or abs(lon - BBOX[3]) < EDGE_BUFFER_DEG
    )


def find_gap_points(features, threshold=GAP_DISTANCE_THRESHOLD_M):
    """نقاط ابتدا/انتهای هر way که بیش از threshold متر از نزدیک‌ترین نقطه‌ی دیگر فاصله دارن"""
    endpoints = []
    for i, f in enumerate(features):
        if f["geometry"]["type"] != "LineString":
            continue
        coords = f["geometry"]["coordinates"]
        endpoints.append((coords[0], i))
        endpoints.append((coords[-1], i))

    gap_points = []
    for pt, way_i in endpoints:
        if near_edge(pt):
            continue
        min_dist = min(
            (haversine(pt, pt2) for pt2, way_j in endpoints if way_j != way_i),
            default=float("inf"),
        )
        if min_dist > threshold:
            gap_points.append({"coord": pt, "way_index": way_i, "nearest_dist": round(min_dist, 1)})
    return gap_points


def main():
    with open(INPUT_FILE, encoding="utf-8") as f:
        data = json.load(f)

    features = data["features"]
    cat_lengths = {}
    for f in features:
        cat = categorize(f["properties"])
        length = way_length(f["geometry"]["coordinates"])
        cat_lengths[cat] = cat_lengths.get(cat, 0) + length

    gap_points = find_gap_points(features)
    significant_gaps = [g for g in gap_points if g["nearest_dist"] > 40]

    stats = {
        "total_features": len(features),
        "category_lengths_km": {k: round(v / 1000, 2) for k, v in cat_lengths.items()},
        "total_km": round(sum(cat_lengths.values()) / 1000, 2),
        "gap_points_count": len(significant_gaps),
        "gap_points": significant_gaps,
    }

    with open(OUTPUT_STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    print(f"مجموع طول شبکه: {stats['total_km']} km")
    for cat, km in stats["category_lengths_km"].items():
        print(f"  {cat}: {km} km")
    print(f"نقاط گسست شناسایی‌شده: {stats['gap_points_count']}")
    print(f"نتایج در {OUTPUT_STATS_FILE} ذخیره شد.")


if __name__ == "__main__":
    main()
