# Basics Requirements
import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

# Recall app
from app import app
from library import def_data

# ------------------------------
# CONTENTS
# 1. Sidebar style
# 2. SQL queries
# 3. Accordion
# 4. Area drop down
# 5. Sidebar Layout
# 6. Input and Area arrays
# ------------------------------

# ------------------------------
# 1. SIDEBAR STYLE
# ------------------------------
SIDEBAR_STYLE = {
    "position": "absolute",
    "top": '140px',
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# ------------------------------
# 2. SQL queries
# ------------------------------
# 2.1 Query variables
df_vars = def_data.runQuery("""select * from public.var_definition order by group_id;""")

# ------------------------------
# 3. Accordion
# ------------------------------
var_groups = list(df_vars['group_id'].unique())
cardBody = []
for gr in var_groups:
    tempCardBody = []
    options = []
    for var_id in df_vars[df_vars['group_id'] == gr]['var_id']:
        options.append( {'label': '  ' + list(df_vars[df_vars['var_id']==str(var_id)]['label'])[0], 'value': str(var_id)} )
    tempCardBody.append(
        dbc.CardBody(
            [dcc.RadioItems(
                id=f"stats_checklist_{gr}",
                options=options,
                value="",
                style={"font-size": "small"}),
            html.Div(id=f"stats_checklist_{gr}_output", style={'display':'none'})],
            style={'height': '200px', 'overflowY': 'auto'}
        )
    )
    cardBody.insert(gr, tempCardBody)


def make_item(i):
    # we use this function to make the example items to avoid code duplication
    return dbc.Card(
        [
            dbc.CardHeader(
                html.H6(
                    dbc.Button(
                        list(df_vars[df_vars['group_id']==i]['group'].unique())[0],
                        color="link",
                        id=f"stats_group-{i}-toggle", size="sm" #,block=True
                    )
                ),style={"height":"30px","padding": "0","margin": "0"}
            ),
            dbc.Collapse(
                cardBody[i-1],
                id=f"stats_collapse-{i}",
            ),
        ]
    )

accordion_items = []
for gr in var_groups:
    accordion_items.append(make_item(gr))

accordion = html.Div(
    accordion_items, className="accordion"
)

# ------------------------------
# 3.1 Accordion Callbacks
# ------------------------------
@app.callback(
    [Output(f"stats_collapse-{i}", "is_open") for i in var_groups],
    [Input(f"stats_group-{i}-toggle", "n_clicks") for i in var_groups],
    [State(f"stats_collapse-{i}", "is_open") for i in var_groups],
)
def toggle_accordion(*args):
    ctx = dash.callback_context
    n = args[0:int(len(args)/2)]
    n = list(n)
    is_open = args[int(len(args)/2):]
    for i in range(len(n)):
        if n[i] is None:
            n[i] = 0

    if not ctx.triggered:
        return [False for i in var_groups]
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    toggle = [False for i in range(len(is_open))]
    for i in var_groups:
        if button_id == 'stats_group-' + str(i) + '-toggle': # and n[i]:
            toggle[i-1] = not is_open[i-1]
    return toggle


# ------------------------------
# 5. SIDEBAR LAYOUT
# ------------------------------

dropdown_variables = dcc.Dropdown(
    id='xy-dropdown',
    options=[
        {'label': 'X variable', 'value': 'x_selected'},
        {'label': 'Y variable', 'value': 'y_selected'}
    ],
    value='x_selected'
)

dropdown_years = dcc.Dropdown(
    id='year-dropdown',
    options=[
        {'label': '2011', 'value': 2011},
        {'label': '2012', 'value': 2012},
        {'label': '2013', 'value': 2013},
        {'label': '2014', 'value': 2014},
        {'label': '2015', 'value': 2015},
        {'label': '2016', 'value': 2016},
        {'label': '2017', 'value': 2017},
        {'label': '2018', 'value': 2018},
        {'label': '2019', 'value': 2019},

    ],
    value=2019
)



sidebar = html.Div(
    [
        html.H3('Explore Variables:'),
        html.P('Select Year:'),
        dropdown_years,
        html.P(' '),
        html.P('Select X Variable to Compare:'),
        # dropdown_variables,
        html.Hr(),
        accordion,
    ],
    style=SIDEBAR_STYLE,
)
