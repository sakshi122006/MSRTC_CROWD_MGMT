import streamlit as st
from datetime import date, timedelta, datetime
import time as t
import random
import csv
from collections import deque

# =========================
# Page config
# =========================
st.set_page_config(page_title="MSRTC Crowd Sync", page_icon="🚍", layout="wide")

# =========================
# Session state
# =========================
if "lang" not in st.session_state:
    st.session_state.lang = "EN"  # EN / MR

if "recent" not in st.session_state:
    st.session_state.recent = deque(maxlen=5)

if "selected_date" not in st.session_state:
    st.session_state.selected_date = date.today()

if "selected_time" not in st.session_state:
    st.session_state.selected_time = "08:00 AM"

if "travel_type" not in st.session_state:
    st.session_state.travel_type = "Student"

if "weather" not in st.session_state:
    st.session_state.weather = "Clear"

# =========================
# Theme
# =========================
PRIMARY = "#C1121F"
BG = "#F7F7F7"
TEXT = "#111827"
MUTED = "#6B7280"

# =========================
# Premium CSS (IMPORTANT: CSS must stay inside this block)
# =========================
st.markdown(
    f"""
<style>
/* App background */
.stApp {{
  background: {BG};
}}

#MainMenu {{visibility:hidden;}}
footer {{visibility:hidden;}}
header {{visibility:hidden;}}

/* Mobile container */
.mobile {{
  max-width: 420px;
  margin: auto;
  border-radius: 25px;
  padding-bottom: 84px; /* space for bottom nav */
}}

/* Sticky header */
.topbar {{
  position: sticky;
  top: 0;
  z-index: 99;
  background: white;
  border-bottom: 1px solid #eee;
  padding: 14px 14px;
  border-radius: 20px;
  margin-bottom: 10px; /* reduced */
  box-shadow: 0 8px 22px rgba(0,0,0,0.06);
}}

.brand {{
  font-weight: 900;
  font-size: 1.15rem;
  color: {PRIMARY};
  display:flex;
  align-items:center;
  gap:10px;
}}

/* Hero card */
.hero {{
  border-radius: 22px;
  overflow: hidden;
  position: relative;
  height: 150px;         /* slightly reduced */
  background: linear-gradient(135deg, rgba(193,18,31,0.95), rgba(17,24,39,0.75));
  box-shadow: 0 18px 40px rgba(0,0,0,0.10);
  margin-bottom: 12px;   /* reduced */
}}
.hero::after {{
  content:"";
  position:absolute;
  inset:0;
  background: radial-gradient(500px circle at 20% 20%, rgba(255,255,255,0.22), transparent 55%);
}}
.heroText {{
  position:absolute;
  inset:0;
  padding: 16px;
  display:flex;
  flex-direction:column;
  justify-content:flex-end;
  color:#fff;
}}
.heroTitle {{
  font-size: 1.35rem;
  font-weight: 900;
  margin: 0;
}}
.heroSub {{
  margin-top: 6px;
  font-size: 0.95rem;
  opacity: 0.92;
}}

/* Cards */
.card {{
  background: white;
  border-radius: 20px;
  padding: 14px;
  box-shadow: 0 14px 36px rgba(0,0,0,0.08);
  border: 1px solid #f1f1f1;
  margin-bottom: 12px; /* reduced */
}}
.cardTitle {{
  font-weight: 900;
  color: {TEXT};
  display:flex;
  align-items:center;
  gap:10px;
  margin-bottom: 10px;
}}

/* Labels */
div[data-testid="stWidgetLabel"] > label {{
  color: {TEXT} !important;
  font-weight: 900 !important;
}}

/* Reduce Streamlit default column gaps a bit */
div[data-testid="stHorizontalBlock"] {{
  gap: 0.55rem !important;
}}

/* Result animation */
@keyframes slideUp {{
  from {{ opacity: 0; transform: translateY(14px); }}
  to {{ opacity: 1; transform: translateY(0); }}
}}
.resultAnim {{ animation: slideUp 360ms ease-out; }}

/* Badges */
.badge {{
  display:inline-flex;
  align-items:center;
  gap:8px;
  padding: 8px 12px;
  border-radius: 999px;
  font-weight: 900;
  color: white;
}}
.badge-high {{ background: #ef4444; }}
.badge-med  {{ background: #f59e0b; }}
.badge-low  {{ background: #22c55e; }}

/* Festival alert */
.festival {{
  background: linear-gradient(135deg, rgba(245,158,11,0.16), rgba(249,115,22,0.12));
  border: 1px solid rgba(245,158,11,0.35);
  border-radius: 18px;
  padding: 12px;
  box-shadow: 0 14px 34px rgba(0,0,0,0.08);
}}
.festivalTitle {{
  font-weight: 950;
  color: {TEXT};
}}

/* Tip card */
.tip {{
  background: rgba(59,130,246,0.10);
  border: 1px solid rgba(59,130,246,0.22);
  border-radius: 18px;
  padding: 12px;
  color: {TEXT};
}}

/* Bottom nav */
.bottomnav {{
  position: fixed;
  left: 50%;
  transform: translateX(-50%);
  bottom: 14px;
  width: min(420px, calc(100% - 24px));
  background: white;
  border-radius: 22px;
  padding: 10px 12px;
  box-shadow: 0 18px 45px rgba(0,0,0,0.12);
  border: 1px solid #eee;
  display:flex;
  justify-content:space-around;
  z-index: 999;
}}
.navitem {{
  display:flex;
  flex-direction:column;
  align-items:center;
  gap:4px;
  font-weight: 900;
  font-size: 0.82rem;
  color: {MUTED};
}}
.navactive {{ color: {PRIMARY}; }}

/* ============ PREMIUM TIME SLOT UI (TIGHTER GAPS) ============ */
.ts-wrap{{ margin-top: 6px; }}
.ts-wrap .stButton {{ margin-bottom: 0.20rem !important; }}

.ts-row{{
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 6px;  /* tighter */
}}
@media (max-width: 520px){{
  .ts-row{{ grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 6px; }}
}}

.ts-btn button{{
  width: 100% !important;
  height: 40px !important;        /* slightly smaller */
  border-radius: 999px !important;
  padding: 0 !important;
  border: 1px solid rgba(255,255,255,0.18) !important;
  color: #fff !important;
  font-weight: 900 !important;
  letter-spacing: 0.2px !important;
  box-shadow: 0 8px 16px rgba(0,0,0,0.08) !important;
  transition: transform 120ms ease, box-shadow 120ms ease, filter 120ms ease !important;
}}
.ts-btn button:hover{{
  transform: translateY(-1px) scale(1.005) !important;
  filter: brightness(1.02) !important;
  box-shadow: 0 10px 18px rgba(0,0,0,0.10) !important;
}}
.ts-selected button{{
  outline: 2px solid rgba(255,255,255,0.92) !important;
  box-shadow: 0 0 0 3px rgba(193,18,31,0.22),
              0 12px 22px rgba(193,18,31,0.18) !important;
  transform: scale(1.01) !important;
}}

.ts-night button{{ background: linear-gradient(135deg, #6b0210, #a30f1f) !important; }}
.ts-morning button{{ background: linear-gradient(135deg, #C1121F, #ff3b30) !important; }}
.ts-afternoon button{{ background: linear-gradient(135deg, #e34214, #c1121f) !important; }}
.ts-evening button{{ background: linear-gradient(135deg, #c1121f, #ff6a00) !important; }}
.ts-late button{{ background: linear-gradient(135deg, #4a000a, #8b0d1b) !important; }}

/* Predict button */
div.stButton > button {{
  border-radius: 18px;
  padding: 0.9rem 1rem;
  border: 0;
  background: linear-gradient(135deg, {PRIMARY}, #ff3b30);
  color: white;
  font-weight: 950;
  box-shadow: 0 16px 36px rgba(193,18,31,0.30);
  transition: transform 120ms ease, filter 120ms ease;
}}
div.stButton > button:hover {{
  transform: translateY(-1px) scale(1.01);
  filter: brightness(1.03);
}}
</style>
""",
    unsafe_allow_html=True,
)

# =========================
# CSV calendar loader (Option A)
# CSV columns: date,name_en,name_mr,type (festival/holiday)
# =========================
@st.cache_data
def load_calendar_events(csv_path="festivals_mh_2026.csv"):
    holidays = {}
    festivals = {}
    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                d = datetime.strptime(row["date"], "%Y-%m-%d").date()
                payload = {"en": (row.get("name_en") or "").strip(), "mr": (row.get("name_mr") or "").strip()}
                typ = (row.get("type") or "festival").strip().lower()
                if typ == "holiday":
                    holidays[d] = payload
                else:
                    festivals[d] = payload
    except FileNotFoundError:
        # don't crash app
        holidays, festivals = {}, {}
    return holidays, festivals

HOLIDAYS, FESTIVALS = load_calendar_events("festivals_mh_2026.csv")

def get_calendar_features(d: date):
    holiday = HOLIDAYS.get(d)
    festival = FESTIVALS.get(d)
    return {
        "is_weekend": int(d.weekday() >= 5),
        "is_holiday": int(holiday is not None),
        "is_festival": int(festival is not None),
        "holiday": holiday,
        "festival": festival,
    }

# =========================
# App logic helpers
# =========================
DESTINATIONS = ["Pune", "Kolhapur", "Akkalkot", "Pandharpur", "Dharashiv", "Latur", "Mumbai", "Tuljapur", "Sangola", "Barshi", "Swargate"]
WEATHER = [("☀ Clear", "Clear"), ("🌧 Rain", "Rain"), ("⛈ Heavy Rain", "Heavy Rain"), ("🌫 Fog", "Fog")]

def build_time_slots_12h():
    time_slots = []
    for hour in range(24):
        suffix = "AM" if hour < 12 else "PM"
        display_hour = hour % 12
        if display_hour == 0:
            display_hour = 12
        time_slots.append(f"{display_hour:02d}:00 {suffix}")
    return time_slots

def slot_theme_class(slot_label: str) -> str:
    hh = int(slot_label.split(":")[0])
    suffix = slot_label.split()[-1]
    if suffix == "AM":
        hour24 = 0 if hh == 12 else hh
    else:
        hour24 = 12 if hh == 12 else hh + 12

    if 0 <= hour24 <= 5:
        return "ts-night"
    if 6 <= hour24 <= 11:
        return "ts-morning"
    if 12 <= hour24 <= 16:
        return "ts-afternoon"
    if 17 <= hour24 <= 21:
        return "ts-evening"
    return "ts-late"

def hour_from_slot(slot_label: str) -> int:
    hh = int(slot_label.split(":")[0])
    suffix = slot_label.split()[-1]
    if suffix == "AM":
        return 0 if hh == 12 else hh
    return 12 if hh == 12 else hh + 12

def crowd_level_logic(occupancy: int) -> str:
    if occupancy > 75:
        return "High"
    elif occupancy > 40:
        return "Medium"
    return "Low"

def bilingual_suggestion(level: str):
    marathi_map = {
        "High": "जास्त गर्दी अपेक्षित आहे. पुढील वेळ निवडा.",
        "Medium": "मध्यम गर्दी. थोडे लवकर जा.",
        "Low": "कमी गर्दी. आरामदायक प्रवास."
    }
    if level == "High":
        eng = "High crowd expected. Try next time slot."
    elif level == "Medium":
        eng = "Moderate crowd. Travel a bit early."
    else:
        eng = "Low crowd. Comfortable journey."
    return eng, marathi_map[level]

def travel_type_message(travel_type: str, hour: int, level: str):
    peak = (8 <= hour <= 10) or (18 <= hour <= 20)
    if travel_type == "Student":
        if peak and level != "Low":
            return "🎓 College rush likely. Reach 15 min early for a seat."
        return "🎓 Student mode: Prefer non-peak buses for comfortable travel."
    if travel_type == "Office Worker":
        if peak:
            return "💼 Peak commute detected. Keep 20–30 min buffer time."
        return "💼 Office mode: Smooth commute expected outside peak hours."
    if level == "High":
        return "🧳 Tourist mode: Avoid this slot for luggage comfort—try mid-day."
    return "🧳 Tourist mode: Good slot for relaxed sightseeing travel."

def simulate_occupancy(dest: str, d: date, hour: int, weather: str, travel_type: str, cal: dict) -> int:
    occ = 35
    if hour in [8, 9, 10, 18, 19, 20]:
        occ += 30
    if cal["is_weekend"]:
        occ += 14
    if dest == "Mumbai":
        occ += 10

    if weather == "Rain":
        occ += 6
    elif weather == "Heavy Rain":
        occ += 10
    elif weather == "Fog":
        occ += 5

    if travel_type == "Office Worker":
        occ += 6
    elif travel_type == "Tourist":
        occ += 3

    if cal["is_festival"]:
        occ += 10
    if cal["is_holiday"]:
        occ += 6

    occ += random.randint(-6, 10)
    return max(5, min(98, int(occ)))

def best_time_engine(dest: str, d: date, hour: int, weather: str, travel_type: str, cal: dict):
    candidates = [max(0, hour - 1), hour, min(23, hour + 1)]
    best_h, best_occ = hour, 999
    for h in candidates:
        occ = simulate_occupancy(dest, d, h, weather, travel_type, cal)
        if occ < best_occ:
            best_occ = occ
            best_h = h
    # keep 24h output for best time; you can also show AM/PM if you want
    return f"{best_h:02d}:00", best_occ

# =========================
# MOBILE container start
# =========================
st.markdown('<div class="mobile">', unsafe_allow_html=True)

# =========================
# Topbar
# =========================
top_l, top_r = st.columns([1.6, 0.7])
with top_l:
    st.markdown('<div class="topbar"><div class="brand">🚍 MSRTC Crowd Sync</div></div>', unsafe_allow_html=True)

with top_r:
    toggle_label = "🌐 मराठी" if st.session_state.lang == "EN" else "🌐 English"
    if st.button(toggle_label, use_container_width=True):
        st.session_state.lang = "MR" if st.session_state.lang == "EN" else "EN"

# =========================
# Hero
# =========================
st.markdown(
    """
<div class="hero">
  <div class="heroText">
    <div class="heroTitle">Plan Your Journey</div>
    <div class="heroSub">Real-time occupancy prediction for stress-free travel.</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# =========================
# Input card
# =========================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="cardTitle">📦 Trip Details</div>', unsafe_allow_html=True)

st.text_input("🚏 From (Fixed)", value="Solapur", disabled=True)
destination = st.selectbox("🏁 Destination", DESTINATIONS)

# Date quick cards
st.markdown("📅 Journey Date")
days = [date.today() + timedelta(days=i) for i in range(7)]
date_cols = st.columns(7)
for i, d in enumerate(days):
    if d == date.today():
        label = f"TODAY\n{d.strftime('%d %b')}"
    elif d == date.today() + timedelta(days=1):
        label = f"TMRW\n{d.strftime('%d %b')}"
    else:
        label = f"{d.strftime('%a').upper()}\n{d.strftime('%d %b')}"
    if date_cols[i].button(label, key=f"date_{i}", use_container_width=True):
        st.session_state.selected_date = d

selected_date = st.session_state.selected_date

# Travel type
st.markdown("🧍 Travel Type")
types = [("🎓 Student", "Student"), ("💼 Office Worker", "Office Worker"), ("🧳 Tourist", "Tourist")]
tcols = st.columns(3)
for i, (lab, val) in enumerate(types):
    is_sel = (st.session_state.travel_type == val)
    if tcols[i].button(("✅ " if is_sel else "") + lab, key=f"type_{val}", use_container_width=True):
        st.session_state.travel_type = val
travel_type = st.session_state.travel_type

# Weather
st.markdown("🌦 Weather")
wcols = st.columns(4)
for i, (lab, val) in enumerate(WEATHER):
    is_sel = (st.session_state.weather == val)
    if wcols[i].button(("✅ " if is_sel else "") + lab, key=f"w_{val}", use_container_width=True):
        st.session_state.weather = val
weather = st.session_state.weather

# Premium time slots
st.markdown("⏰ Time Slot Selection (AM/PM)")
st.caption("Tap a time slot. Selected slot gets glow + tick + theme by time.")

time_slots = build_time_slots_12h()
st.markdown('<div class="ts-wrap">', unsafe_allow_html=True)

for r in range(0, len(time_slots), 4):
    row = time_slots[r:r+4]
    st.markdown('<div class="ts-row">', unsafe_allow_html=True)
    cols = st.columns(4)
    for i, slot in enumerate(row):
        is_sel = (slot == st.session_state.selected_time)
        theme = slot_theme_class(slot)
        wrapper_cls = f"ts-btn {theme} " + ("ts-selected" if is_sel else "")
        with cols[i]:
            st.markdown(f'<div class="{wrapper_cls}">', unsafe_allow_html=True)
            btn_label = f"✔ {slot}" if is_sel else slot
            if st.button(btn_label, key=f"ts_{slot}", use_container_width=True):
                st.session_state.selected_time = slot
            st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

selected_time = st.session_state.selected_time
hour = hour_from_slot(selected_time)

st.markdown("<hr style='border:0;height:1px;background:#eee;margin:10px 0;'/>", unsafe_allow_html=True)
predict = st.button("🚀 Predict Crowd", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# =========================
# Prediction + Result
# =========================
if predict:
    cal = get_calendar_features(selected_date)

    with st.spinner("Predicting occupancy…"):
        t.sleep(0.8)

    occupancy = simulate_occupancy(destination, selected_date, hour, weather, travel_type, cal)
    level = crowd_level_logic(occupancy)
    eng, mr = bilingual_suggestion(level)
    best_time, best_occ = best_time_engine(destination, selected_date, hour, weather, travel_type, cal)

    # store recent searches
    st.session_state.recent.appendleft({
        "route": f"Solapur → {destination}",
        "time": selected_time,
        "date": selected_date.isoformat(),
        "when": datetime.now().strftime("%H:%M"),
    })

    # badge style
    badge_cls = "badge-med"
    badge_icon = "🟡"
    if level == "High":
        badge_cls, badge_icon = "badge-high", "🔴"
    elif level == "Low":
        badge_cls, badge_icon = "badge-low", "🟢"

    st.markdown('<div class="card resultAnim">', unsafe_allow_html=True)
    st.markdown('<div class="cardTitle">📊 Result</div>', unsafe_allow_html=True)

    st.markdown(f'<span class="badge {badge_cls}">{badge_icon} {level} Crowd</span>', unsafe_allow_html=True)
    st.write("")

    st.markdown(f"**Occupancy: {occupancy}%**")
    st.progress(occupancy / 100)

    st.markdown("### 🌍 Bilingual Output")
    st.write(f"**English:** {eng}")
    st.write(f"**मराठी:** {mr}")

    st.markdown("### 🎯 Smart Travel Message")
    st.info(travel_type_message(travel_type, hour, level))

    st.markdown("### ⏱ Best Time Suggestion")
    st.success(f"Best time to travel: **{best_time}** (≈ **{best_occ}%** crowd)")

    # festival/holiday output
    if cal["is_festival"]:
        fest = cal["festival"] or {}
        fest_name = fest.get("en", "Festival")
        fest_mr = fest.get("mr", "")
        st.markdown(
            f"""
            <div class="festival resultAnim">
              <div class="festivalTitle">🎉 Festival Alert: {fest_name}{(" / " + fest_mr) if fest_mr else ""}</div>
              <div style="color:{MUTED}; font-weight:800; margin-top:6px;">
                Festival days often increase passenger demand. Prefer off-peak hours.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if cal["is_holiday"]:
        hol = cal["holiday"] or {}
        hol_name = hol.get("en", "Holiday")
        hol_mr = hol.get("mr", "")
        st.warning(f"🏛️ Holiday Active: {hol_name}" + (f" / {hol_mr}" if hol_mr else "") + " → crowd may increase.")

    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# Recent searches
# =========================
if len(st.session_state.recent) > 0:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="cardTitle">📋 Recent Searches</div>', unsafe_allow_html=True)
    for item in list(st.session_state.recent):
        st.markdown(
            f"""
            <div style="border:1px solid #f0f0f0; border-radius:18px; padding:12px; margin-bottom:10px;">
              <div style="font-weight:950; color:{TEXT}; display:flex; justify-content:space-between;">
                <div>{item["route"]}</div>
                <div style="color:{PRIMARY};">➜</div>
              </div>
              <div style="color:{MUTED}; font-weight:800; margin-top:6px;">
                Time: {item["time"]} • Date: {item["date"]} • Last searched: {item["when"]}
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# Smart tip
# =========================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="cardTitle">💡 Smart Tip</div>', unsafe_allow_html=True)
st.markdown(
    """
<div class="tip">
<b>Tip for commuters:</b><br/>
Buses between <b>1 PM – 3 PM</b> usually have lower occupancy. Try mid-day slots for comfort.
</div>
""",
    unsafe_allow_html=True,
)
st.markdown("</div>", unsafe_allow_html=True)

# =========================
# Bottom nav (UI only)
# =========================
st.markdown(
    f"""
<div class="bottomnav">
  <div class="navitem navactive">🏠<div>Home</div></div>
  <div class="navitem">🎫<div>Bookings</div></div>
  <div class="navitem">👤<div>Profile</div></div>
</div>
""",
    unsafe_allow_html=True,
)

# MOBILE container end
st.markdown("</div>", unsafe_allow_html=True)
