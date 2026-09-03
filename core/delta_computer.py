import numpy as np
from scipy.ndimage import uniform_filter1d

def delta_cumulative (tel_ref, tel_comp):
    tel_ref_dt = (tel_ref['Time'] - tel_ref['Time'].iloc[0]).dt.total_seconds().values
    tel_comp_dt = (tel_comp['Time'] - tel_comp['Time'].iloc[0]).dt.total_seconds().values
    d_ref = tel_ref['Distance'].values
    d_comp = tel_comp['Distance'].values
    L = max(d_ref.max(), d_comp.max())
    d_ref_norm = d_ref * L / d_ref.max()
    d_comp_norm = d_comp * L / d_comp.max()

    tel_comp_interp = np.interp(d_ref_norm, d_comp_norm, tel_comp_dt)
    delta_time = tel_ref_dt - tel_comp_interp

    return d_ref_norm, d_comp_norm, delta_time

def compute_local_gain (delta_time):
    delta_smooth = uniform_filter1d(delta_time, size=20)
    delta_diff = np.diff(delta_smooth)
    return delta_diff

