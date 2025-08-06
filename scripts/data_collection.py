import fastf1
from fastf1 import get_event_schedule
import pandas as pd
import time
import os
from fastf1.req import RateLimitExceededError

fastf1.Cache.enable_cache('cache')  # Create a local cache folder



years = [2022, 2023, 2024]  # Update to include 2025 later
races_by_year = {}

for year in years:
    schedule = get_event_schedule(year)
    race_names = schedule.loc[schedule['EventFormat'] != 'Sprint Shootout', 'EventName'].tolist()
    races_by_year[year] = race_names

print(races_by_year)


# Enable caching
fastf1.Cache.enable_cache('cache')

# Define years to process
years = [2022, 2023, 2024]

# Define file paths
results_file = "f1_ground_effect_results.csv"
progress_file = "progress_tracker.csv"

# Load completed sessions from progress tracker
if os.path.exists(progress_file):
    try:
        progress_df = pd.read_csv(progress_file)
        completed_sessions = set(zip(progress_df['Year'], progress_df['Race']))
    except Exception as e:
        print(f"⚠️ Failed to read progress file: {e}. Starting from scratch.")
        completed_sessions = set()
else:
    completed_sessions = set()

# Load existing results or create new list
if os.path.exists(results_file):
    results_data = pd.read_csv(results_file).to_dict(orient='records')
else:
    results_data = []

# Get list of races per year
races_by_year = {}
for year in years:
    schedule = get_event_schedule(year)
    races = schedule.loc[schedule['EventFormat'] != 'Sprint Shootout', 'EventName'].tolist()
    races_by_year[year] = races

# Begin loading sessions
for year, race_names in races_by_year.items():
    for race_name in race_names:
        if (year, race_name) in completed_sessions:
            print(f"⏩ Skipping already processed: {year} - {race_name}")
            continue

        try:
            print(f"🔄 Attempting to load: {year} - {race_name}")
            session = fastf1.get_session(year, race_name, 'R')
            session.load(telemetry=False)

            # Determine if it's a wet race
            weather = session.weather_data
            is_wet_race = weather['Rainfall'].mean() > 0.05 if not weather.empty else False

            # Collect results
            for _, row in session.results.iterrows():
                results_data.append({
                    'Year': year,
                    'Race': race_name,
                    'Driver': row['Abbreviation'],
                    'Team': row['TeamName'],
                    'GridPosition': row['GridPosition'],
                    'RacePosition': row['Position'],
                    'Status': row['Status'],
                    'IsWetRace': is_wet_race
                })

            # Save results after each session
            pd.DataFrame(results_data).to_csv(results_file, index=False)

            # Update progress tracker with header-safe method
            progress_entry = pd.DataFrame([[year, race_name]], columns=["Year", "Race"])
            header = not os.path.exists(progress_file)
            progress_entry.to_csv(progress_file, mode='a', header=header, index=False)

            print(f"✅ Loaded: {year} - {race_name}")

        except RateLimitExceededError:
            print("🛑 Rate limit reached. Exiting. Rerun script later to resume.")
            raise  # Exit script by raising the error

        except Exception as e:
            print(f"❌ Failed: {year} - {race_name} | Error: {e}")

        # Respect FastF1 rate limits
        time.sleep(10)
