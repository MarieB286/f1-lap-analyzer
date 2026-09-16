import fastf1
from pathlib import Path
from datetime import datetime
import pandas as pd
import numpy as np
from core.gap_analyzer import get_corner_delta
from core.delta_computer import delta_cumulative

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

def build_corners_table(ref_tel, comp_tel, circuit_info):
    rows = []
    delta_1, delta_2, delta_time = delta_cumulative(ref_tel, comp_tel)
    for _, corner in circuit_info.corners.iterrows():
        ref_vmin = get_corner_min_speed(ref_tel, corner['Distance'], 60,30,)
        comp_vmin = get_corner_min_speed(comp_tel, corner['Distance'], 60,30)
        vmin = (ref_vmin + comp_vmin)/2
        corner_type = classify_corners(vmin)
        corner_delta = get_corner_delta(ref_tel, comp_tel, corner['Distance'], delta_1, delta_time)
        rows.append({
            'Corner': f"T{corner['Number']}",
            'Type': corner_type,
            'Vmin ref': f"{ref_vmin:.0f} km/h",
            'Vmin comp': f"{comp_vmin:.0f} km/h",
            'Delta_Corner' : f"{corner_delta:+.3f} s"
        })
    return rows