# Basics Requirements
import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

# Recall app
from app import app
from lib import def_data

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": '140px',
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

df = def_data.runQuery("""select * from public.var_definition;""")

cardBody = []
for gr in list(df['group_id'].unique()):
    tempCardBody = []
    for var in df[df['group_id'] == gr]['label']:
        tempCardBody.append(dbc.CardBody(var))
    cardBody.insert(gr, tempCardBody)

def make_item(i):
    # we use this function to make the example items to avoid code duplication
    return dbc.Card(
        [
            dbc.CardHeader(
                html.H2(
                    dbc.Button(
                        list(df[df['group_id']==i]['group'].unique())[0],
                        color="link",
                        id=f"group-{i}-toggle",
                    )
                )
            ),
            dbc.Collapse(
                cardBody[i-1],
                id=f"collapse-{i}",
            ),
        ]
    )


accordion = html.Div(
    [make_item(1), make_item(2), make_item(3)], className="accordion"
)


@app.callback(
    [Output(f"collapse-{i}", "is_open") for i in range(1, 4)],
    [Input(f"group-{i}-toggle", "n_clicks") for i in range(1, 4)],
    [State(f"collapse-{i}", "is_open") for i in range(1, 4)],
)
def toggle_accordion(n1, n2, n3, is_open1, is_open2, is_open3):
    ctx = dash.callback_context

    if not ctx.triggered:
        return False, False, False
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "group-1-toggle" and n1:
        return not is_open1, False, False
    elif button_id == "group-2-toggle" and n2:
        return False, not is_open2, False
    elif button_id == "group-3-toggle" and n3:
        return False, False, not is_open3
    return False, False, False


sidebar = html.Div(
    [
        html.H6("Variables", className="display-4"),
        html.Hr(),
        accordion,
    ],
    style=SIDEBAR_STYLE,
)