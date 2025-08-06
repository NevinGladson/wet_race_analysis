# 🏎️ F1 Wet Weather and Pit Stop Strategy Analysis (2022–2024)

This project investigates the effect of **wet weather conditions** and **pit stop strategies** (undercuts) on F1 race results between 2022 and 2024. It uses official timing data via the FastF1 API and focuses on identifying patterns in driver performance, team reliability, and strategic race decisions.

---

## 🔍 Objectives

- 📉 Identify races held in **wet** vs **dry** conditions using rainfall data
- 🧮 Compare team and driver performance under different conditions
- ⚠️ Analyze **DNF (Did Not Finish)** patterns in wet races
- 🏆 Score drivers in wet conditions using an adjusted points system
- ⛽ Evaluate **undercut effectiveness** from lap-by-lap data


---
```
├── scripts/
│ └── data_collection.py # Code to fetch & save data using FastF1
│
├── notebooks/
|└── wet_race.ipynb # Visualizations, scoring, and insights
│
├── data/
│ └── f1_ground_effect_results.csv

```
---

## 📊 Key Findings

- Wet races lead to **higher DNF rates** for some teams and drivers
- Certain drivers (e.g., VER, LEC) consistently perform better in the wet
- Undercuts are **more effective at Miami** than Monaco based on lap position change
- Top drivers can gain multiple places by well-timed pit stops, even in wet races

---

## 🧰 Technologies Used

- Python 3.9+
- FastF1
- pandas
- matplotlib

## Future Works
- 📊 Compare races like **Monaco** and **Miami** to see where pit stop timing matters most
- seaborn

---
