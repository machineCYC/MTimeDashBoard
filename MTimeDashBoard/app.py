import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from plotly import tools
from plotly.subplots import make_subplots

# TODO: 要畫的欄位
# TODO: 要畫的圖

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Data"
)
dataset_names = [f for f in os.listdir(DATA_DIR) if not f.endswith(".gitkeep")]


def generate_plot_data(id_index):
    id_name = available_ids[id_index]
    sub_data = df_bar[df_bar["stock_id"] == id_name]
    # return {'x':sub_data["date"].index, 'y':sub_data["close"], 'type':'scatter','name':id_name}
    return go.Scatter(x=sub_data["date"], y=sub_data["close"], mode="lines")
    # return px.line(sub_data, x="date", y="close")


def get_subplots_fig(show_columns, show_figures):
    quotient = int(show_figures // show_columns)
    remainder = int(show_figures % show_columns)
    show_rows = quotient + 1 if remainder else quotient
    print(f"show_rows:{show_rows}, show_columns:{show_columns}")

    fig = make_subplots(
        rows=show_rows,
        cols=show_columns,
        shared_xaxes=False,
        shared_yaxes=False,
        print_grid=False,
        subplot_titles=available_ids[
            :show_figures
        ],  # TODO: if data need filter. maybe it will wrong
    )
    plot_position = [
        (row, col) for row in range(show_rows) for col in range(show_columns)
    ]
    for id_index, (row, col) in enumerate(plot_position):
        print(f"id_index:{id_index}, NBR_KEY:{NBR_KEY}")
        if id_index >= min(NBR_KEY, show_figures):
            continue
        else:
            print(f"id_index:{id_index}, ({row}, {col})")
            fig.append_trace(generate_plot_data(id_index), row + 1, col + 1)
    fig["layout"]["margin"] = {"b": 0, "r": 0, "l": 0, "t": 50}

    # fig["layout"]["height"] = 200
    # fig["layout"]["width"] = 250
    # fig["layout"].update(
    #     paper_bgcolor="#18252E", plot_bgcolor="#18252E"
    # )
    return fig


app.layout = html.Div(
    [
        html.Div(
            [
                "dataset:",
                dcc.Dropdown(
                    id="data_name_input",
                    options=[{"label": i, "value": i} for i in dataset_names],
                    value=dataset_names[0],
                ),
            ],
            style={"width": "48%"},
        ),
        html.Div(
            [
                "show_figures: ",
                dcc.Input(id="show_figures", value=min(20, 5), type="text"),
            ],
            style={"width": "24%", "display": "inline-block"},
        ),
        html.Div(
            [
                "show_columns: ",
                dcc.Input(id="show_columns", value=2, type="text"),
            ],
            style={"width": "24%", "display": "inline-block"},
        ),
        dcc.Graph(id="indicator-graphic"),
    ],
)


@app.callback(
    Output("indicator-graphic", "figure"),
    Input(component_id="show_figures", component_property="value"),
    Input(component_id="show_columns", component_property="value"),
    Input(component_id="data_name_input", component_property="value"),
)
def update_fig(show_figures, show_columns, data_name_input):
    if data_name_input:
        path = os.path.join(DATA_DIR, data_name_input)
        print(f"path:{path}")
        global df_bar
        global available_ids
        global NBR_KEY
        df_bar = pd.read_csv(path)
        df_bar["stock_id"] = df_bar["stock_id"].astype(str)
        df_bar["date"] = pd.to_datetime(df_bar["date"])
        df_bar["close"] = df_bar["close"].astype(int)
        print(df_bar.info())
        available_ids = df_bar["stock_id"].astype(str).unique()
        NBR_KEY = len(available_ids)

    print(
        f"update fig, show_figures:{show_figures} show_columns:{show_columns}"
    )
    fig = get_subplots_fig(int(show_columns), int(show_figures))
    return fig


# @app.callback(
#     Output('indicator-graphic', 'figure'),
#     Input(component_id='data_name_input', component_property='value'),
# )
# def update_datasets(data_name_input):
#     path = os.path.join(DATA_DIR, data_name_input)
#     print(f"path:{path}")
#     global df_bar
#     global available_ids
#     global NBR_KEY
#     df_bar = pd.read_csv(path)
#     df_bar["date"] = pd.to_datetime(df_bar["date"])
#     df_bar["close"] = df_bar["close"].astype(int)
#     print(df_bar.info())
#     available_ids = df_bar["stock_id"].astype(str).unique()
#     NBR_KEY = len(available_ids)


if __name__ == "__main__":
    app.run_server(debug=True)
