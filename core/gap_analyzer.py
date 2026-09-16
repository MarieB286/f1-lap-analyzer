import fastf1
from pathlib import Path
from datetime import datetime
import pandas as pd
import numpy as np
from core.data_loading import get_fastest_lap_telemetry, load_session
from core.delta_computer import delta_cumulative

def get_corner_delta (ref_tel, comp_tel, corner_distance,delta_1, delta_time):
    delta_at_entry = np.interp(corner_distance - 60, delta_1, delta_time)
    delta_at_exit = np.interp(corner_distance + 30, delta_1, delta_time)
    corner_delta = delta_at_exit - delta_at_entry
    return corner_delta 