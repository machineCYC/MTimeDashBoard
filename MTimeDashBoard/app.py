import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

NBR_FIGURE = 10
NBR_COLUMNS_FIGURE = 2
NBR_ROWS_FIGURE = int((NBR_FIGURE // NBR_COLUMNS_FIGURE) + 1)

FIGRURE_WIDTH = 400

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df_bar = pd.DataFrame(
    {
        "Fruit": [
            "Apples",
            "Oranges",
            "Bananas",
            "Apples",
            "Oranges",
            "Bananas",
        ],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"],
    }
)
fig = px.bar(df_bar, x="Fruit", y="Amount", color="City", barmode="group", title="test_title")

app.layout = html.Div(
    children=[
        # All elements from the top of the page
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id=f"graph_{row}_{col}", figure=fig),
                    ],
                    className="six columns",
                    style={'width': FIGRURE_WIDTH}
                )
                for col in range(NBR_COLUMNS_FIGURE)
            ],
            className="row",
        )
        for row in range(NBR_ROWS_FIGURE)
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
