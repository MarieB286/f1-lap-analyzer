import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from core.delta_computer import compute_local_gain

def rotate(xy, *, angle):
    rot_mat = np.array([[np.cos(angle), np.sin(angle)],
                        [-np.sin(angle), np.cos(angle)]])
    return np.matmul(xy, rot_mat)

def track_map_plot (ref_X, ref_Y, circuit_info, delta_time, ref_name, comp_name, ref_color, comp_color, session):
    x = ref_X.values
    y = ref_Y.values

    track_angle = circuit_info.rotation / 180 * np.pi
    xy = np.array([x, y]).T
    xy_rot = rotate(xy, angle=track_angle)
    x_rot, y_rot = xy_rot[:, 0], xy_rot[:, 1]

    points = np.array([x_rot, y_rot]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    delta_diff = compute_local_gain (delta_time)

    cmap = LinearSegmentedColormap.from_list(
    f' {ref_name}_{comp_name}', [ref_color, '#f5f5f5', comp_color])
    vmax = np.percentile(np.abs(delta_diff), 70)
    norm = plt.Normalize(vmin=-vmax, vmax=vmax)

    fig, ax = plt.subplots(figsize=(12, 12))

    ax.plot(x_rot, y_rot, color='black', linewidth=8, zorder=1)
    ax.plot(x_rot, y_rot, color='#e0e0e0', linewidth=6, zorder=2)

    lc = LineCollection(segments, cmap=cmap, norm=norm, linewidth=5, zorder=3)
    lc.set_array(delta_diff)
    ax.add_collection(lc)

    cbar = plt.colorbar(lc, ax=ax, shrink=0.5, pad=0.02)
    cbar.set_label(f'← {ref_name} gains    |    {comp_name} gains →')

    offset_vector = [500, 0]
    for _, corner in circuit_info.corners.iterrows():
        txt = f"{corner['Number']}{corner['Letter']}"
        offset_angle = corner['Angle'] / 180 * np.pi
        offset_x, offset_y = rotate(offset_vector, angle=offset_angle)
        text_x = corner['X'] + offset_x
        text_y = corner['Y'] + offset_y
        text_x, text_y = rotate([text_x, text_y], angle=track_angle)
        track_x, track_y = rotate([corner['X'], corner['Y']], angle=track_angle)
        ax.scatter(text_x, text_y, color='grey', s=140, zorder=4)
        ax.plot([track_x, text_x], [track_y, text_y], color='grey', zorder=3)
        ax.text(text_x, text_y, txt, va='center_baseline', ha='center',
                size='small', color='white', zorder=5)

    ax.set_title(f"{session.event['Location']} - Where each of them gains time")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')
    ax.autoscale()
    return fig



