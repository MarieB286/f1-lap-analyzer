import fastf1
from pathlib import Path
from datetime import datetime
import pandas as pd
import numpy as np

# Cache à la racine du projet, quel que soit d'où on appelle le code
CACHE_DIR = Path(__file__).parent.parent / 'cache'
CACHE_DIR.mkdir(exist_ok=True)
fastf1.Cache.enable_cache(str(CACHE_DIR))


def load_session(year, event, session_type):
    session = fastf1.get_session(year, event, session_type)
    session.load(laps=True, telemetry=True, weather=False)
    return session


def get_fastest_lap_telemetry(session, driver):
    lap = session.laps.pick_drivers(driver).pick_fastest()
    telemetry = lap.get_telemetry()
    return lap, telemetry

def get_available_schedule(year):
    schedule = fastf1.get_event_schedule(year)
    schedule = schedule[schedule['RoundNumber'] > 0 ]
    schedule = schedule[schedule['EventDate'] < datetime.now()]
    return schedule['EventName'].tolist()

def get_drivers_full_infos(year,gp, session_type):
    session = load_session(year, gp, session_type)
    results = session.results
    options = []
    for _, row in results.iterrows():
        options.append({
            'label': f"{row['FullName']} ({row['Abbreviation']})",
            'value': row['Abbreviation']
        })
    return options 

def add_qualifying_phase(laps):
    """Ajoute une colonne 'QualiPhase' (Q1/Q2/Q3) aux laps d'une session de qualif.
    Détection par les 2 plus gros gaps temporels (pauses entre phases).
    """
    laps = laps.sort_values('LapStartTime').copy()
    start_times = laps['LapStartTime'].dt.total_seconds().values
    
    # Trouver les 2 plus gros écarts
    gaps = np.diff(start_times)
    top_2_gap_indices = sorted(np.argsort(gaps)[-2:])
    
    # Assigner les phases
    phases = np.array(['Q1'] * len(laps), dtype=object)
    phases[top_2_gap_indices[0]+1:top_2_gap_indices[1]+1] = 'Q2'
    phases[top_2_gap_indices[1]+1:] = 'Q3'
    
    laps['QualiPhase'] = phases
    return laps

