from datetime import date, datetime
import csv

def is_weekend(d: date) -> int:
    return 1 if d.weekday() >= 5 else 0

def load_calendar_events(csv_path="festivals_mh_2026.csv"):
    """
    CSV columns:
    date,name_en,name_mr,type (festival/holiday)
    """
    holidays = {}
    festivals = {}
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            d = datetime.strptime(row["date"], "%Y-%m-%d").date()
            name_en = row.get("name_en", "").strip()
            name_mr = row.get("name_mr", "").strip()
            typ = row.get("type", "festival").strip().lower()

            payload = {"en": name_en, "mr": name_mr}

            if typ == "holiday":
                holidays[d] = payload
            else:
                festivals[d] = payload

    return holidays, festivals

# Load once (fast)
HOLIDAYS, FESTIVALS = load_calendar_events("festivals_mh_2026.csv")

def get_calendar_features(selected_date: date):
    holiday = HOLIDAYS.get(selected_date)
    festival = FESTIVALS.get(selected_date)

    return {
        "is_weekend": is_weekend(selected_date),
        "is_holiday": 1 if holiday else 0,
        "is_festival": 1 if festival else 0,
        "holiday_name": holiday["en"] if holiday else None,
        "holiday_name_mr": holiday["mr"] if holiday else None,
        "festival_name": festival["en"] if festival else None,
        "festival_name_mr": festival["mr"] if festival else None,
    }