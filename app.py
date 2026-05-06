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
# State
# =========================
if "lang" not in st.session_state:
    st.session_state.lang = "EN"  # EN / MR

if "recent" not in st.session_state:
    st.session_state.recent = deque(maxlen=5)  # store dict items

# =========================
# Theme + Mobile UI CSS
# =========================
PRIMARY = "#C1121F"
BG = "#F7F7F7"
TEXT = "#111827"
MUTED = "#6B7280"

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
  margin-bottom: 12px;
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

.langbtn {{
  padding: 8px 12px;
  border-radius: 999px;
  border: 1px solid #eee;
  background: #fff;
  color: {TEXT};
  font-weight: 700;
}}

/* Hero card */
.hero {{
  border-radius: 22px;
  overflow: hidden;
  position: relative;
  height: 160px;
  background: linear-gradient(135deg, rgba(193,18,31,0.95), rgba(17,24,39,0.75));
  box-shadow: 0 18px 40px rgba(0,0,0,0.10);
  margin-bottom: 14px;
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
  padding: 18px;
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
  margin-bottom: 14px;
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
  font-weight: 800 !important;
}}

/* Input styling */
.inputHint {{
  color: {MUTED};
  font-size: 0.9rem;
  margin-top: 6px;
}}

/* Chips */
.chiprow {{
  display:flex;
  gap:10px;
  overflow-x:auto;
  padding-bottom: 4px;
}}
.chip {{
  white-space: nowrap;
  padding: 10px 12px;
  border-radius: 999px;
  border: 1px solid #eaeaea;
  background: #fff;
  color: {TEXT};
  font-weight: 800;
  cursor: pointer;
}}
.chip-selected {{
  border: 1px solid {PRIMARY};
  background: {PRIMARY};
  color: white;
}}

/* Travel type cards */
.typegrid {{
  display:grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 10px;
}}
.typecard {{
  border-radius: 18px;
  padding: 12px 10px;
  border: 1px solid #eaeaea;
  background: #fff;
  text-align:center;
  font-weight: 900;
  color: {TEXT};
}}
.type-selected {{
  border: 2px solid {PRIMARY};
  background: rgba(193,18,31,0.07);
}}

/* Predict button */
div.stButton > button {{
  width: 100%;
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
</style>
""",
    unsafe_allow_html=True,
)

# =========================
# Calendar (CSV) loader (Option A)
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
        # don't crash UI
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
# UI helpers
# =========================
DESTINATIONS = ["Pune", "Kolhapur", "Akkalkot", "Pandharpur", "Dharashiv", "Latur", "Mumbai", "Tuljapur", "Sangola", "Barshi", "Swargate"]
WEATHER = [("☀ Clear", "Clear"), ("🌧 Rain", "Rain"), ("⛈ Heavy Rain", "Heavy Rain"), ("🌫 Fog", "Fog")]

def time_slots_24():
    return [f"{h:02d}:00" for h in range(24)]

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
    # More "app-like" actionable wording
    peak = (8 <= hour <= 10) or (18 <= hour <= 20)
    if travel_type == "Student":
        if peak and level != "Low":
            return "🎓 College rush likely. Reach 15 min early for a seat."
        return "🎓 Student mode: Prefer non-peak buses for comfortable travel."
    if travel_type == "Office Worker":
        if peak:
            return "💼 Peak commute detected. Keep 20–30 min buffer time."
        return "💼 Office mode: Smooth commute expected outside peak hours."
    # Tourist
    if level == "High":
        return "🧳 Tourist mode: Avoid this slot for luggage comfort—try mid-day."
    return "🧳 Tourist mode: Good slot for relaxed sightseeing travel."

def simulate_occupancy(dest: str, d: date, hour: int, weather: str, travel_type: str, cal: dict) -> int:
    occ = 35

    # rush hours
    if hour in [8, 9, 10, 18, 19, 20]:
        occ += 30

    # weekend
    if cal["is_weekend"]:
        occ += 14

    # destination load
    if dest == "Mumbai":
        occ += 10

    # weather
    if weather == "Rain":
        occ += 6
    elif weather == "Heavy Rain":
        occ += 10
    elif weather == "Fog":
        occ += 5

    # travel type weights
    if travel_type == "Office Worker":
        occ += 6
    elif travel_type == "Tourist":
        occ += 3

    # festival/holiday from CSV
    if cal["is_festival"]:
        occ += 10
    if cal["is_holiday"]:
        occ += 6

    occ += random.randint(-6, 10)
    return max(5, min(98, int(occ)))

def best_time_engine(dest: str, d: date, hour: int, weather: str, travel_type: str, cal: dict):
    # check +/- 1 hour
    candidates = [max(0, hour - 1), hour, min(23, hour + 1)]
    best_h, best_occ = hour, 999
    for h in candidates:
        occ = simulate_occupancy(dest, d, h, weather, travel_type, cal)
        if occ < best_occ:
            best_occ = occ
            best_h = h
    return f"{best_h:02d}:00", best_occ

# =========================
# MOBILE CONTAINER START
# =========================
st.markdown('<div class="mobile">', unsafe_allow_html=True)

# =========================
# Topbar (sticky)
# =========================
c1, c2 = st.columns([1.6, 0.7])
with c1:
    st.markdown('<div class="topbar"><div class="brand">🚍 MSRTC Crowd Sync</div></div>', unsafe_allow_html=True)

with c2:
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
# Input Card
# =========================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="cardTitle">📦 Trip Details</div>', unsafe_allow_html=True)

# Fixed source
st.text_input("🚏 From (Fixed)", value="Solapur", disabled=True)

# Destination
destination = st.selectbox("🏁 Destination", DESTINATIONS)

# Swap button (UI-only because source fixed)
st.caption("🔄 Swap disabled (Source is fixed as Solapur).")

# Date cards (Today + next 6 days)
st.markdown("📅 Journey Date")
days = [date.today() + timedelta(days=i) for i in range(7)]
labels = []
for d in days:
    if d == date.today():
        labels.append(("TODAY", d))
    elif d == date.today() + timedelta(days=1):
        labels.append(("TOMORROW", d))
    else:
        labels.append((d.strftime("%a").upper(), d))

date_cols = st.columns(7)
if "selected_date" not in st.session_state:
    st.session_state.selected_date = date.today()

for i, (lab, d) in enumerate(labels):
    selected = (d == st.session_state.selected_date)
    btn_text = f"{lab}\n{d.strftime('%d %b')}"
    if date_cols[i].button(btn_text, key=f"date_{i}", use_container_width=True):
        st.session_state.selected_date = d

selected_date = st.session_state.selected_date

# Time chips (24 hour)
st.markdown("⏰ Time Slot (24-hour)")
if "selected_time" not in st.session_state:
    st.session_state.selected_time = "08:00"

time_cols = st.columns(4)
# show as segmented grid, still mobile-friendly
slots = time_slots_24()
# render 24 buttons in 6 rows x 4 cols
for r in range(6):
    cols = st.columns(4)
    for c in range(4):
        idx = r * 4 + c
        ts = slots[idx]
        label = ts
        is_sel = (ts == st.session_state.selected_time)
        if cols[c].button(("✅ " if is_sel else "") + label, key=f"time_{ts}", use_container_width=True):
            st.session_state.selected_time = ts

selected_time = st.session_state.selected_time
hour = int(selected_time.split(":")[0])

# Travel type cards
st.markdown("🧍 Travel Type")
if "travel_type" not in st.session_state:
    st.session_state.travel_type = "Student"

types = [("🎓 Student", "Student"), ("💼 Office Worker", "Office Worker"), ("🧳 Tourist", "Tourist")]
cols = st.columns(3)
for i, (lab, val) in enumerate(types):
    is_sel = (st.session_state.travel_type == val)
    if cols[i].button(("✅ " if is_sel else "") + lab, key=f"type_{val}", use_container_width=True):
        st.session_state.travel_type = val

travel_type = st.session_state.travel_type

# Weather chips
st.markdown("🌦 Weather")
if "weather" not in st.session_state:
    st.session_state.weather = "Clear"

wcols = st.columns(4)
for i, (lab, val) in enumerate(WEATHER):
    is_sel = (st.session_state.weather == val)
    if wcols[i].button(("✅ " if is_sel else "") + lab, key=f"w_{val}", use_container_width=True):
        st.session_state.weather = val

weather = st.session_state.weather

st.markdown("<hr style='border:0;height:1px;background:#eee;margin:12px 0;'/>", unsafe_allow_html=True)
predict = st.button("🚀 Predict Crowd", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# =========================
# Prediction + Result
# =========================
if predict:
    cal = get_calendar_features(selected_date)

    with st.spinner("Predicting occupancy…"):
        t.sleep(0.9)

    occupancy = simulate_occupancy(destination, selected_date, hour, weather, travel_type, cal)
    level = crowd_level_logic(occupancy)
    eng, mr = bilingual_suggestion(level)
    best_time, best_occ = best_time_engine(destination, selected_date, hour, weather, travel_type, cal)

    # Store recent searches
    st.session_state.recent.appendleft({
        "route": f"Solapur → {destination}",
        "time": selected_time,
        "date": selected_date.isoformat(),
        "when": datetime.now().strftime("%H:%M"),
    })

    # Festival card
    fest_payload = cal["festival"]
    holiday_payload = cal["holiday"]
    show_festival = cal["is_festival"] == 1

    # Badge class
    badge_cls = "badge-med"
    badge_icon = "🟡"
    if level == "High":
        badge_cls, badge_icon = "badge-high", "🔴"
    elif level == "Low":
        badge_cls, badge_icon = "badge-low", "🟢"

    # Result card
    st.markdown('<div class="card resultAnim">', unsafe_allow_html=True)
    st.markdown('<div class="cardTitle">📊 Result</div>', unsafe_allow_html=True)

    st.markdown(f'<span class="badge {badge_cls}">{badge_icon} {level} Crowd</span>', unsafe_allow_html=True)
    st.write("")

    # Progress bar
    st.markdown(f"**Occupancy: {occupancy}%**")
    st.progress(occupancy / 100)

    # Bilingual output based on toggle
    st.markdown("### 🌍 Bilingual Output")
    st.write(f"**English:** {eng}")
    st.write(f"**मराठी:** {mr}")

    # Smart travel message
    st.markdown("### 🎯 Smart Travel Message")
    st.info(travel_type_message(travel_type, hour, level))

    # Best time
    st.markdown("### ⏱ Best Time Suggestion")
    st.success(f"Best time to travel: **{best_time}** (≈ **{best_occ}%** crowd)")

    # Festival output
    if show_festival:
        fest_name = fest_payload["en"] if fest_payload else "Festival"
        st.markdown(
            f"""
            <div class="festival resultAnim">
              <div class="festivalTitle">🎉 Festival Alert: {fest_name} Rush Expected</div>
              <div style="color:{MUTED}; font-weight:800; margin-top:6px;">
                Festival days often increase passenger demand. Consider off-peak hours.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Holiday output
    if cal["is_holiday"]:
        hol_name = holiday_payload["en"] if holiday_payload else "Holiday"
        st.warning(f"🏛️ Holiday Active: {hol_name} → crowd may increase.")

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
# Bottom nav (UI-only)
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

# MOBILE CONTAINER END
st.markdown("</div>", unsafe_allow_html=True)
