import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots

def plot_speed_delta_plotly (d_ref_norm, d_comp_norm, ref_speed, comp_speed, 
                      delta_time, ref_name, comp_name, ref_color, comp_color, circuit_info):
    fig = make_subplots (rows = 2, cols = 1, 
                         shared_xaxes = True, 
                         row_heights = [0.75, 0.25],
                         vertical_spacing = 0.05,
    )
    fig.add_trace(go.Scatter(x = d_ref_norm, y = ref_speed, name = ref_name, line = dict(color = ref_color),
                            ), row = 1, col = 1 )
    fig.add_trace(go.Scatter(x = d_comp_norm, y = comp_speed, name = comp_name, line = dict(color = comp_color),
                                ), row = 1, col = 1 )

    delta_neg = np.where(delta_time < 0, delta_time, None)
    delta_pos = np.where(delta_time >= 0, delta_time, None)

    fig.add_trace(
        go.Scatter(
            x=d_ref_norm,
            y=delta_neg,
            fill='tozeroy',
            fillcolor=ref_color,
            opacity=0.5,
            line=dict(color=ref_color, width=0),
            showlegend=False,
            name=f'{ref_name} gains',
        ),
        row=2, col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=d_ref_norm,
            y=delta_pos,
            fill='tozeroy',
            fillcolor=comp_color,
            opacity=0.5,
            line=dict(color=comp_color, width=0),
            showlegend=False,
            name=f'{comp_name} gains',
        ),
        row=2, col=1,
    )
    fig.add_trace(go.Scatter(x = d_ref_norm, y = delta_time, name = 'Delta', line = dict(color = 'black', width = 1.5),
                                        ), row = 2, col = 1 )

    for _, corner in circuit_info.corners.iterrows():
        txt = f"T{corner['Number']}{corner['Letter']}"
        fig.add_vline(x=corner['Distance'],
                      line = dict(color='gray', width = 0.5, dash = 'dash'), 
                      opacity=0.5, layer = 'above', row = 1, col=1,)
        fig.add_annotation(x = corner['Distance'], 
                           y = 340, 
                           text=txt, textangle=-90, 
                           font = dict(size = 9, color = 'gray'), 
                           row = 1, col = 1,)   
    fig.update_layout(
        title=f'{ref_name} vs {comp_name} - Speed and cumulative delta',
        height=550,
        hovermode='x unified', 
        showlegend=True,
    )
    fig.update_yaxes(title_text='Speed (km/h)', range=[0, 350], row=1, col=1)

    fig.update_xaxes(title_text='Distance (m)', row=2, col=1)
    fig.update_yaxes(title_text=f'Delta (s)\n←{ref_name}  {comp_name}→', row=2, col=1)

    fig.add_hline(y = delta_time[-1],
                  line = dict(color = 'blue', width = 1.5, dash = 'dash'),
                  annotation_text = f'Final Delta : {delta_time[-1]:.3f}s', 
                  annotation_position = 'bottom left',
                  row = 2, col = 1)
    return fig