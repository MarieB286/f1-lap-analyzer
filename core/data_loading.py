import fastf1
from pathlib import Path

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

