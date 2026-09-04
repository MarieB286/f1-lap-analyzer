import numpy as np
from core.delta_computer import compute_local_gain
import plotly.graph_objects as go

def rotate(xy, *, angle):
    rot_mat = np.array([[np.cos(angle), np.sin(angle)],
                        [-np.sin(angle), np.cos(angle)]])
    return np.matmul(xy, rot_mat)

def plot_track_map_plotly (ref_X, ref_Y, circuit_info, delta_time, ref_name, comp_name, ref_color, comp_color, session):
    x = ref_X
    y = ref_Y

    track_angle = circuit_info.rotation / 180 * np.pi
    xy = np.array([x, y]).T
    xy_rot = rotate(xy, angle=track_angle)
    x_rot, y_rot = xy_rot[:, 0], xy_rot[:, 1]

    points = np.array([x_rot, y_rot]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    delta_diff = compute_local_gain (delta_time)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_rot, y=y_rot,
        mode='lines',
        line=dict(color='black', width=15),
        showlegend=False,
        hoverinfo='skip',
    ))
    fig.add_trace(go.Scatter(
        x = x_rot,
        y = y_rot,
        mode = 'lines',
        line = dict(color = 'lightgray', width = 10),
        showlegend=False,
        hoverinfo = 'skip',
    ))

    fig.update_layout(
        title=f'{circuit_info.corners.iloc[0].name}',
        showlegend = False,
        width = 1100, 
        margin=dict(l=20, r=100, t=60, b=20),
    )

    fig.update_xaxes(showticklabels= False, showgrid = False, zeroline = False)
    fig.update_yaxes(showticklabels= False, showgrid = False, zeroline = False, scaleanchor = 'x')

    vmax = np.percentile(np.abs(delta_diff), 70)
    fig.add_trace(go.Scatter(
        x = x_rot[:-1],
        y = y_rot[:-1],
        mode = 'markers',
        marker = dict(
            color = delta_diff,
            colorscale = [[0, ref_color], [0.5, '#f5f5f5'], [1, comp_color]], 
            cmin = -vmax, 
            cmax = vmax, 
            size = 8, 
            symbol = 'square',
            showscale = True, 
            colorbar = dict(
                title = dict(text = f'← {ref_name} gains    |    {comp_name} gains →', side = 'right', font = dict(size=11)),
                thickness = 12,
                len = 0.5,
                nticks= 11,
                x = 1.02,
                y = 0.5, 
                tickformat= '.3f',
            ),
        ),
        showlegend= False,
        hoverinfo='skip',
    ))

    offset_vector = np .array([500,0])
    for _, corner in circuit_info.corners.iterrows():
        txt = f"{corner['Number']}{corner['Letter']}"
        offset_angle = corner['Angle'] / 180 * np.pi
        offset_x, offset_y = rotate(offset_vector, angle=offset_angle)
        text_x = corner['X'] + offset_x
        text_y = corner['Y'] + offset_y
        text_x, text_y = rotate(np.array([text_x, text_y]), angle=track_angle)
        track_x, track_y = rotate(np.array([corner['X'], corner['Y']]), angle=track_angle)

        fig.add_trace(go.Scatter(
            x=[track_x, text_x],
            y=[track_y, text_y],
            mode='lines',
            line=dict(color='gray', width=1),
            showlegend=False,
            hoverinfo='skip',
        ))

        fig.add_trace(go.Scatter(
            x=[text_x],
            y=[text_y],
            mode='markers+text',
            marker=dict(color='gray', size=20),
            text=[txt],
            textfont=dict(color='white', size=10),
            textposition='middle center',
            showlegend=False,
            hoverinfo='skip',
        ))

    fig.update_layout(
        title=f'{ref_name} vs {comp_name} - Where each of them gains time',
        showlegend=False,
        width=900,
        plot_bgcolor='white',
        margin=dict(l=20, r=20, t=60, b=20),
    )
    fig.update_xaxes(showticklabels=False, showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showticklabels=False, showgrid=False, zeroline=False,
                    visible=False, scaleanchor='x')
    return fig
