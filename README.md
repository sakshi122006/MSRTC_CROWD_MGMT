# 🚍 MSRTC Crowd Sync (MSRTC Smart Crowd Predictor)

A **mobile-first Streamlit app** that predicts **bus crowd/occupancy** for MSRTC routes (Source fixed: **Solapur**) and provides **smart, explainable travel suggestions** with **Marathi + English** output.

> Theme: **MSRTC Red** • Premium UI • Time-slot picker • Festival/Holiday awareness • Best-time recommendation

---

## ✨ Key Features

### ✅ Premium Mobile UI (Streamlit + Custom CSS)
- Mobile container layout (app-like feel)
- Rounded cards, soft shadows, clean spacing
- Sticky header + bottom navigation (UI-only)
- Premium **AM/PM time slot grid** with:
  - glow + tick on selection
  - smart color themes by time (night/morning/afternoon/evening)

### 🎯 Crowd Prediction Output
- **Crowd Level**:
  - 🔴 High
  - 🟡 Medium
  - 🟢 Low
- **Occupancy %** with progress bar
- **Bilingual Suggestions**
  - English + Marathi

### 🧠 Smart Decision Support
- **Best Time Suggestion Engine** (checks nearby time slots and suggests a better time)
- **Travel Type Mode**:
  - 🎓 Student
  - 💼 Office Worker
  - 🧳 Tourist  
  (each gets different, more effective guidance)

### 🎉 Festival & Holiday Awareness (CSV based)
- Automatically detects festivals/holidays using a CSV dataset
- Shows special alert cards for festivals/holidays
- Adjusts occupancy logic (festival/holiday increases crowd)

### 📋 Recent Searches
- Displays last few searches for quick reference

---

## 🧩 Tech Stack
- **Python**
- **Streamlit**
- Custom CSS (for premium UI)
- Optional: model loading from `models/` (if integrated)

---

## 📂 Project Structure (Suggested)

```
.
├── app.py
├── festivals_mh_2026.csv
├── models/
│   └── crowd_rf_model.pkl        # optional (if you have ML model)
├── data/
│   ├── bus_timetable.csv         # optional
│   └── ...                       # optional datasets
└── README.md
```

---

## 🗓️ Festival / Holiday Data (CSV Format)

Create `festivals_mh_2026.csv` in the root folder (or update path inside `app.py`).

**Required columns:**
- `date` (YYYY-MM-DD)
- `name_en`
- `name_mr`
- `type` (festival / holiday)

Example:

```csv
date,name_en,name_mr,type
2026-08-15,Independence Day,स्वातंत्र्य दिन,holiday
2026-09-17,Ganesh Chaturthi,गणेश चतुर्थी,festival
2026-11-08,Diwali,दिवाळी,festival
```

---

## ▶️ How to Run

### 1) Install dependencies
```bash
pip install streamlit
```

### 2) Run the app
```bash
streamlit run app.py
```

If you placed the CSV in `data/`, update the loader path in `app.py`:
```python
load_calendar_events("data/festivals_mh_2026.csv")
```

---

## 🔧 Configuration Notes

### Source & Destination
- Source is **fixed as Solapur**
- Destination options include:
  - Pune, Kolhapur, Akkalkot, Pandharpur, Dharashiv, Latur, Mumbai, Tuljapur, Sangola, Barshi, Swargate

### Time Slots
- Displayed in **12-hour AM/PM** format
- Internally mapped to 0–23 hours for logic

---

## 🧠 Prediction Logic (Current)
This project currently uses a **rule-based simulation** for occupancy:
- Rush hours increase occupancy
- Weekend increases occupancy
- Weather impacts occupancy
- Festival/Holiday increases occupancy
- Travel type slightly adjusts occupancy

✅ You can replace the simulation with your trained ML model anytime.

---

## 🤖 Integrating Your ML Model (Optional)

If you have a trained model (example: `models/crowd_rf_model.pkl`), you can replace the function:

```python
simulate_occupancy(...)
```

with:

- `model.predict(...)` to output occupancy
- (Optional) `model.predict_proba(...)` to show confidence score

---

## 🧪 Demo Tips (For Viva / Presentation)
- Show how festival day changes output and adds an alert card
- Compare Student vs Office Worker vs Tourist messages
- Select a peak hour and show increased crowd
- Use “Recent Searches” to show app-like usability

---

## 👩‍💻 Author
Developed by: **sakshirevaje-sys**

---

## 📜 License
This project is for educational/demo purposes. Add a license if needed.