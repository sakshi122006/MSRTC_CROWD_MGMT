import streamlit as st
import pandas as pd
import joblib
import os
from datetime import datetime

from calendar_utils import get_calendar_features
from timetable_utils import load_timetable, get_next_bus

# ── Load Model ─────────────────────────────
MODEL_PATH = os.path.join("models", "crowd_rf_model.pkl")

if not os.path.exists(MODEL_PATH):
    st.error("❌ Model not found. Run train_model.py first.")
    st.stop()

model = joblib.load(MODEL_PATH)

# ── Load Timetable ─────────────────────────
timetable_df = load_timetable()

# ── Route Info ─────────────────────────────
ROUTE_INFO = {
    "Solapur-Pune": {"distance_km": 260, "num_stops": 10},
    "Solapur-Kolhapur": {"distance_km": 230, "num_stops": 9},
    "Solapur-Akkalkot": {"distance_km": 40, "num_stops": 5},
}

# ── UI ─────────────────────────────────────
st.set_page_config(page_title="MSRTC Crowd Predictor", layout="centered")

st.title("🚌 MSRTC Smart Crowd Predictor")
st.write("Predict crowd and get next bus suggestion")

st.write(f"🕒 Current Time: {datetime.now().strftime('%H:%M')}")

route = st.selectbox("Select Route", list(ROUTE_INFO.keys()))
date = st.date_input("Select Date")

# ✅ 24-hour time input
selected_time = st.time_input("Select Time", value=datetime.now().time())
hour = selected_time.hour
minute = selected_time.minute

weather = st.selectbox("Weather", ["Clear", "Cloudy", "Rain"])

# ── Calendar Features ──────────────────────
calendar = get_calendar_features(date)

# ── Show Calendar Info ─────────────────────
st.markdown("### 📅 Day Information")

if calendar["is_weekend"]:
    st.info("🛑 Weekend (Saturday/Sunday)")

if calendar["is_holiday"]:
    st.warning(f"🎉 Holiday: {calendar['holiday_name']}")

if calendar["is_festival"]:
    st.success(f"🪔 Festival: {calendar['festival_name']}")

if not (calendar["is_weekend"] or calendar["is_holiday"] or calendar["is_festival"]):
    st.write("📌 Normal Working Day")

# ── Route Features ─────────────────────────
distance_km = ROUTE_INFO[route]["distance_km"]
num_stops = ROUTE_INFO[route]["num_stops"]

# ── Crowd Reason Function ──────────────────
def get_crowd_reason(prediction, hour, calendar, weather):
    reasons = []

    if hour in [7, 8, 9, 17, 18, 19]:
        reasons.append("Peak travel hours")

    if calendar["is_weekend"]:
        reasons.append("Weekend rush")

    if calendar["is_holiday"]:
        reasons.append(f"Public holiday ({calendar['holiday_name']})")

    if calendar["is_festival"]:
        reasons.append(f"Festival ({calendar['festival_name']})")

    if weather == "Rain":
        reasons.append("Rain increases public transport usage")

    if prediction == "Low":
        if hour in [12, 13, 14]:
            reasons.append("Afternoon non-peak hours")
        if not reasons:
            reasons.append("Normal working conditions")

    return reasons

# ── Predict Button ─────────────────────────
if st.button("🔍 Predict Crowd"):

    input_df = pd.DataFrame([{
        "route": route,
        "day_of_week": date.weekday(),
        "hour": hour,
        "is_weekend": calendar["is_weekend"],
        "is_holiday": calendar["is_holiday"],
        "is_festival": calendar["is_festival"],
        "distance_km": distance_km,
        "num_stops": num_stops,
        "weather": weather,
    }])

    prediction = model.predict(input_df)[0]

    # Reasons
    reasons = get_crowd_reason(prediction, hour, calendar, weather)

    # Next bus (FULL TIME)
    selected_time_str = selected_time.strftime("%H:%M")
    next_bus = get_next_bus(route, selected_time_str, timetable_df)

    # ── Output ─────────────────────────────
    st.subheader(f"🚦 Crowd Level: {prediction}")

    # 🔥 Festival/Holiday Impact in OUTPUT
    st.markdown("### 🎯 Special Day Impact")

    if calendar["is_festival"]:
        st.success(f"🪔 Festival Impact: {calendar['festival_name']}")

    if calendar["is_holiday"]:
        st.warning(f"🎉 Holiday Impact: {calendar['holiday_name']}")

    if calendar["is_weekend"]:
        st.info("🛑 Weekend Impact (Higher travel expected)")

    # Crowd Message
    if prediction == "High":
        if next_bus:
            st.warning(f"⚠️ High crowd! Take next bus at {next_bus}")
        else:
            st.warning("⚠️ High crowd and no more buses today.")

    elif prediction == "Medium":
        st.info("ℹ️ Moderate crowd. Reach early.")

    else:
        st.success("✅ Low crowd. Comfortable travel.")

    # ── Reasons ───────────────────────────
    st.markdown("### 📊 Why this prediction?")
    for r in reasons:
        st.write(f"• {r}")

    # ── Next Bus Info ─────────────────────
    if next_bus:
        st.success(f"🚌 Next Available Bus: {next_bus}")
    else:
        st.error("❌ No more buses available today.")