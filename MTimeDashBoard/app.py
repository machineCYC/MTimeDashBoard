import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
from plotly import tools
import plotly.graph_objects as go
from plotly.subplots import make_subplots
#TODO: 要畫的欄位
#TODO: 要畫的圖


# NBR_FIGURE = 4
# NBR_COLUMNS_FIGURE = 2
# NBR_ROWS_FIGURE = 2
# NBR_ROWS_FIGURE = int((NBR_FIGURE // NBR_COLUMNS_FIGURE) + (NBR_FIGURE % NBR_COLUMNS_FIGURE) )

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df_bar = pd.DataFrame(
    {
        "id": [
            "Apples",
            "Apples",
            "Apples",
            "Apples",
            "Oranges",
            "Oranges",
            "Oranges",
            "Oranges",
            "Oranges",
            "Oranges",
            "Bananas",
            "Bananas",
            "Bananas",
            "Bananas",
            "Bananas",
            "Bananas",
            "Bananas",
            "Bananas",
            "pig",
            "pig",
            "pig",
        ],
        "time":[i for i in range(21)],
        "Amount": [4, 1, 2, 2, 4, 5, 1, 4, 7, 5, 7, 8, 7, 5, 8, 8, 2, 9, 0, 1, 9],
    }
)

available_ids = df_bar["id"].unique()
NBR_KEY = len(available_ids)

def generate_plot_data(id_index):
    id_name = available_ids[id_index]
    sub_data = df_bar[df_bar["id"]==id_name]
    return {'x':sub_data["time"], 'y':sub_data["Amount"], 'type':'scatter','name':id_name}


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
        print_grid=False
    )
    plot_position = [(row, col)  for row in range(show_rows) for col in range(show_columns)]
    for id_index, (row, col) in enumerate(plot_position):
        if id_index >= min(NBR_KEY, show_figures):
            continue
        else:
            print(id_index, (row, col))
            fig.append_trace(generate_plot_data(id_index), row+1, col+1)
    fig["layout"]["margin"] = {"b": 0, "r": 0, "l": 0, "t": 0}

    # fig["layout"]["height"] = 200
    # fig["layout"]["width"] = 250
    # fig["layout"].update(
    #     paper_bgcolor="#18252E", plot_bgcolor="#18252E"
    # )
    return fig


app.layout = html.Div(
    [
        html.Div(
            ["show_figures: ", dcc.Input(id='show_figures', value=min(20, NBR_KEY), type='text')],
        ),

        html.Div(
            ["show_columns: ", dcc.Input(id='show_columns', value=2, type='text')],
        ),

        dcc.Graph(id='indicator-graphic')
    ],
)


@app.callback(
    Output('indicator-graphic', 'figure'),
    Input(component_id='show_figures', component_property='value'),
    Input(component_id='show_columns', component_property='value'),
)
def update_fig(show_figures, show_columns):
    print(f"update fig, show_figures:{show_figures} show_columns:{show_columns}")
    fig = get_subplots_fig(int(show_columns), int(show_figures))
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
