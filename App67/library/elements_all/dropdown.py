import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

# Recall app
from app import app
from library import def_data

df_vars = def_data.runQuery("""select * from public.var_definition;""")
df_mun = def_data.runQuery("""select * from desertion_by_municip;""")

# dropdown = dbc.DropdownMenu(
#     id='drop_down',
#     label="Menu",
#     children=[
#         dbc.DropdownMenuItem(value=list(df['group_id'].unique())),
#         dbc.DropdownMenuItem("Item 2"),
#         dbc.DropdownMenuItem("Item 3"),
#     ],
# )

# dropdown = dcc.Dropdown(
#     id='drop_down',
#     options=[{"label": name, "value": name} for name in names],
#     value=[name for name in names],
#     clearable=True,
#     multi=True,
# ),

dropdown_variables = dcc.Dropdown(id='dropdown_var', options=[
        {'label': i, 'value': i} for i in df_vars['name'].unique()
    ], multi=True, placeholder='Variable...', style={'width':'60%'}),

dropdown_mun = dcc.Dropdown(id='dropdown_mun', options=[
        {'label': i, 'value': i} for i in df_mun['name_dept'].unique()
    ], multi=False, placeholder='Departamento...', style={'width':'60%'}, value='Antioquia'),