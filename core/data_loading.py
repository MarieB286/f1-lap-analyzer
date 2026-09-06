import fastf1
from pathlib import Path
from datetime import datetime
import pandas as pd
import numpy as np


CACHE_DIR = Path(__file__).parent.parent / 'cache'
CACHE_DIR.mkdir(exist_ok=True)
fastf1.Cache.enable_cache(str(CACHE_DIR))


def load_session(year, event, session_type):
    session = fastf1.get_session(year, event, session_type)
    session.load(laps=True, telemetry=True, weather=False)
    return session


def get_fastest_lap_telemetry(session, driver, quali_phase = None):
    lap = session.laps.pick_drivers(driver)
    if quali_phase is not None:
        laps_sorted = add_qualifying_phase(lap)
        lap = laps_sorted[laps_sorted['QualiPhase'] == quali_phase]
    lap = lap.pick_fastest()
    telemetry = lap.get_telemetry()
    return lap, telemetry

def get_available_schedule(year):
    schedule = fastf1.get_event_schedule(year)
    schedule = schedule[schedule['RoundNumber'] > 0 ]
    schedule = schedule[schedule['EventDate'] < datetime.now()]
    return schedule['EventName'].tolist()

def get_drivers_full_infos(year,gp, session_type, quali_phase=None):
    session = load_session(year, gp, session_type)
    results = session.results
    if quali_phase is not None: 
        laps_sorted = add_qualifying_phase(session.laps)
        laps_sorted = laps_sorted[laps_sorted['QualiPhase'] == quali_phase]
        drivers_in_phase = laps_sorted['Driver'].unique()
        results = results[results['Abbreviation'].isin(drivers_in_phase)]
    options = []
    for _, row in results.iterrows():
        options.append({
            'label': f"{row['FullName']} ({row['Abbreviation']})",
            'value': row['Abbreviation']
        })
    return options 

def add_qualifying_phase(laps):
    laps = laps.sort_values('LapStartTime').copy()
    start_times = laps['LapStartTime'].dt.total_seconds().values
    
    gaps = np.diff(start_times)
    top_2_gap_indices = sorted(np.argsort(gaps)[-2:])
    
    phases = np.array(['Q1'] * len(laps), dtype=object)
    phases[top_2_gap_indices[0]+1:top_2_gap_indices[1]+1] = 'Q2'
    phases[top_2_gap_indices[1]+1:] = 'Q3'
    
    laps['QualiPhase'] = phases
    return laps

def get_corner_min_speed(telemetry, corner_distance, window_before = 60, window_after =30): 
    telemetry = telemetry[(telemetry['Distance']> corner_distance - window_before)&(telemetry['Distance']< corner_distance + window_after)]
    vmin = min(telemetry['Speed'])
    return vmin

def classify_corners(vmin):
    if vmin < 120 : 
        cat = 'slow'
    elif vmin >= 120 and vmin < 200 : 
        cat = 'medium'
    elif vmin >= 200 : 
        cat = 'fast'
    return cat