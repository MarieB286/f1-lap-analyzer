from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import time
from core.data_loading import load_session, get_fastest_lap_telemetry, get_available_schedule, get_drivers_full_infos
from visualization.speed_delta_plotly import plot_speed_delta_plotly
from visualization.track_map_plotly import plot_track_map_plotly
from core.delta_computer import delta_cumulative
from dash.exceptions import PreventUpdate
from dash import dash_table

app = Dash(__name__)

app.layout = html.Div([
    html.H1("F1 Lap Analyzer"),
    html.Div([
        html.Div(
            dcc.Dropdown(id = 'year-dropdown', options = [2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]),
            style = {'flex' : '1', 'minWidth':'0'}
        ),
        html.Div(
            dcc.Dropdown(id = 'gp-dropdown'),
            style = {'flex' : '1', 'minWidth':'0'}
        ),
        html.Div(
            dcc.Dropdown(
                    id = 'session-dropdown',
                    options = ['Q', 'R'],
                ),
            style = {'flex' : '1', 'minWidth':'0'}
        ),
        html.Div(
            dcc.Dropdown(id = 'quali_options', options = ['Q1', 'Q2', 'Q3']),
            style = {'flex' : '1', 'minWidth':'0'}
        ),
    ], style = {'display': 'flex', 'gap':'20px'}),
    dcc.Loading(
        id = 'loading-drivers',
        children = html.Div([
            html.Div(
                dcc.Dropdown(id = 'driver1-dropdown'),
                style = {'flex' : '1', 'minWidth':'0'}
            ),
            html.Div(
                dcc.Dropdown(id = 'driver2-dropdown'),
                style = {'flex' : '1', 'minWidth':'0'}
            ),
        ], style = {'display': 'flex', 'gap':'20px'})
    ),
    dcc.Loading(
        id = 'loading-graphs',
        children=html.Div([
            html.Div(
                dcc.Graph(id='speed-delta-graph'),
                style = {'flex' : '7', 'minWidth':'0'}
            ), 
            html.Div(
                dcc.Graph(id='track-map-delta'),
                style = {'flex' : '3', 'minWidth':'0'}
            ),
        ], style = {'display': 'flex', 'gap':'20px'})
    ),
    dcc.Loading(
        id = 'loading_corners_class',
        children = html.Div([
            dash_table.DataTable(
                id = 'corners-table',
                columns=[
                    {'name' : 'Corner', 'id' : 'Corner'},
                    {'name' : 'Type', 'id' : 'Type'},
                    {'name' : 'Vmin Driver 1', 'id' : 'Vmin ref'},
                    {'name' : 'Vmin Driver 2', 'id' : 'Vmin comp'},
                ],
                data = [],
                style_cell = {'textAlign': 'center', 'padding': '5px', 'fontSize': '12px'},
                style_header={'fontWeight': 'bold', 'backgroundColor': '#f0f0f0'},
            )
        ])
    )
])

@app.callback(
        Output('gp-dropdown', 'options'),
        Input('year-dropdown', 'value')
)

def update_gp(year): 
    if not all([year]):
        raise PreventUpdate
    events  = get_available_schedule(year)
    return events


@app.callback(
    [Output('driver1-dropdown', 'options'),
     Output('driver2-dropdown', 'options'),
     Output('driver1-dropdown', 'value'),
     Output('driver2-dropdown', 'value')],
    [Input('year-dropdown', 'value'),
     Input('gp-dropdown', 'value'),
     Input('session-dropdown', 'value'),
     Input('quali_options', 'value')]
)

def update_driver_options(year, gp, session_type, quali_options):
    if not all([year, gp, session_type, quali_options]):
        raise PreventUpdate
    drivers = get_drivers_full_infos(year, gp, session_type, quali_options)
    return drivers, drivers, None, None

@app.callback(
    [Output('speed-delta-graph', 'figure'),
     Output('track-map-delta', 'figure')],
    [Input('year-dropdown', 'value'),
     Input('gp-dropdown', 'value'),
     Input('session-dropdown', 'value'),
     Input('quali_options', 'value'),
     Input('driver1-dropdown', 'value'),
     Input('driver2-dropdown', 'value')]
)

def update_graphs (year, gp, session_type, quali_options, driver1, driver2) : 
    if not all([year, gp, session_type, quali_options, driver1, driver2]):
        raise PreventUpdate
    session = load_session(year, gp, session_type)
    circuit_info = session.get_circuit_info()

    ref_lap, ref_tel = get_fastest_lap_telemetry(session, driver1, quali_options)
    comp_lap, comp_tel = get_fastest_lap_telemetry(session, driver2, quali_options)

    d_ref_norm, d_comp_norm, delta_time = delta_cumulative(ref_tel, comp_tel)

    fig = plot_speed_delta_plotly (
        d_ref_norm  = d_ref_norm,
        d_comp_norm = d_comp_norm,
        ref_speed = ref_tel['Speed'],
        comp_speed = comp_tel['Speed'],
        delta_time = delta_time,
        ref_name = driver1,
        comp_name = driver2,
        ref_color = '#27F4D2',
        comp_color = '#DC0000',
        circuit_info = circuit_info,
    )

    fig_map = plot_track_map_plotly(
        ref_X=ref_tel['X'].values,
        ref_Y=ref_tel['Y'].values,
        circuit_info = circuit_info,
        delta_time=delta_time,
        ref_name=driver1,
        comp_name=driver2,
        ref_color = '#27F4D2',
        comp_color = '#DC0000',
        session = session,
    )
    return fig, fig_map

if __name__ == '__main__':
    app.run(debug=True)