# Basics Requirements
import dash_core_components as dcc
import dash_html_components as html

from app import app

##############################
# General
##############################
# CONTENTS
#  1. Styles
#  2. Description Text
#  3. Image
#  4. Photos

# ------------------------------
# 1. Styles
# ------------------------------

# 1.1 text
STYLE_DESCRIPTION = {
    "position": "absolute",
    "width": "53%",
    "height": "400px",
    "left": "12%",
    "top": "110px",
    #"border": "10px solid #e7eff6",
    #"border-radius": "10px",
    'color': '#061936',
    'fontSize': 16,
    'font-weight': '999',
    'text-align': 'justify'
}

# 1.2 Background
GENERAL_BACKGROUND = {
    "position": "absolute",
    "width": "25%",
    "height": "650px",
    #"right": "1%",
    'left': '80%',
    "top": "170px",
    "background-image": 'url(/assets/img/education2.png)',
    'background-repeat': 'no-repeat'
}

# 1.3 Photo 1
PHOTO_1 = {
    "position": "absolute",
    "left": "8.5%",
    "top": "480px",
    "width": "9.5%"
}
# 1.4 Photo 2
PHOTO_2 = {
    "position": "absolute",
    "left": "21%",
    "top": "480px",
    "width": "8%"
}
# 1.5 Photo 3
PHOTO_3 = {
    "position": "absolute",
    "left": "32%",
    "top": "480px",
    "width": "8%"
}
# 1.6 Photo 4
PHOTO_4 = {
    "position": "absolute",
    "left": "43%",
    "top": "480px",
    "width": "8.5%"
}
# 1.7 Photo 5
PHOTO_5 = {
    "position": "absolute",
    "left": "54%",
    "top": "480px",
    "width": "8%"
}
# 1.8 Photo 6
PHOTO_6 = {
    "position": "absolute",
    "left": "65%",
    "top": "480px",
    "width": "8%"
}
# 1.9 background_ph
BACK_PHOTO = {
    "position": "absolute",
    "left": "0",
    "top": "135px",
    "width": "100%"
}

NAME_1 = {
    "height": "450px",
    'color': '#061936',
    'fontSize': 14,
    'font-weight': '999',
    'text-align': 'center',
    "position": "absolute",
    "left": "7%",
    "top": "588px",
    "width": "13%"
}
NAME_2 = {
    "height": "450px",
    'color': '#061936',
    'fontSize': 14,
    'font-weight': '999',
    'text-align': 'center',
    "position": "absolute",
    "left": "20%",
    "top": "588px",
    "width": "10%"
}
NAME_3 = {
    "height": "450px",
    'color': '#061936',
    'fontSize': 14,
    'font-weight': '999',
    'text-align': 'center',
    "position": "absolute",
    "left": "31%",
    "top": "588px",
    "width": "10%"
}
NAME_4 = {
    "height": "450px",
    'color': '#061936',
    'fontSize': 14,
    'font-weight': '999',
    'text-align': 'center',
    "position": "absolute",
    "left": "42%",
    "top": "588px",
    "width": "10%"
}
NAME_5 = {
    "height": "450px",
    'color': '#061936',
    'fontSize': 14,
    'font-weight': '999',
    'text-align': 'center',
    "position": "absolute",
    "left": "53%",
    "top": "588px",
    "width": "10%"
}
NAME_6 = {
    "height": "450px",
    'color': '#061936',
    'fontSize': 14,
    'font-weight': '999',
    'text-align': 'center',
    "position": "absolute",
    "left": "66%",
    "top": "588px",
    "width": "5%"
}

# ------------------------------
# 2. Description Text
# ------------------------------
text = dcc.Tab(
        label='About',
        value='what-is',
        children=html.Div(className='control-tab', children=[

            html.Br(),
            html.Br(),
           # html.H2(children='Project Description'),
            #html.Br(),
            html.P('Scholar desertion is an important phenomenon that affects boys, girls and teenagers' 
                   '  around the globe. In developing countries,' 
                    ' it affects society at different levels as not attending school' 
                    ' impacts the individual’s possibilities to improve his or her wellbeing.' 
                    ' Scholar desertion at younger ages severely limits job opportunities and '
                    'contributes to the propagation of poverty cycles across generations.'
                   ),
            html.P('Team 67 decided to face this challenge by providing an interactive tool '
                   'for understanding the problem. With the use of this interactive application '
                   'it is our hope that you can understand some of the variables that are most '
                   'related to the school dropout phenomenon in Colombian. In the interest of '
                   'remaining humble, we did our best to not only present our findings, but to '
                   'make the app interactive as possible so that more knowledgeable users can '
                   'conduct their own analyses.'),
            html.P('We sincerely hope that you enjoy it and find it useful!')
        ], style=STYLE_DESCRIPTION)

    )
# ------------------------------
# 3. Images
# ------------------------------
bg = html.Div(style=GENERAL_BACKGROUND)

# ------------------------------
# 4. Photos
# ------------------------------
ph1 = html.Div([
    html.Img(src=app.get_asset_url("img/alejandra_c.png"),style=PHOTO_1)
])
ph2 = html.Div([
    html.Img(src=app.get_asset_url("img/carlos_c.png"),style=PHOTO_2)
])
ph3 = html.Div([
    html.Img(src=app.get_asset_url("img/daniel_j_3.png"),style=PHOTO_3)
])
ph4 = html.Div([
    html.Img(src=app.get_asset_url("img/alberto_l.png"),style=PHOTO_4)
])
ph5 = html.Div([
    html.Img(src=app.get_asset_url("img/diego_m.png"),style=PHOTO_5)
])
ph6 = html.Div([
    html.Img(src=app.get_asset_url("img/luis_p.png"),style=PHOTO_6)
])
bck_ph = html.Div([
    html.Img(src=app.get_asset_url("img/colegio3.jpeg"),style=BACK_PHOTO)
])

name_1 = html.Div([
    html.P('Alejandra Castelblanco  '
           'Biomedical & Mechanical '
           'Eng.')
], style=NAME_1)

name_2 = html.Div([
    html.P('Carlos Coy '
           'Electronic Eng.')
], style=NAME_2)

name_3 = html.Div([
    html.P('Daniel Jimenez  '
           'Statistician '
           )
], style=NAME_3)

name_4 = html.Div([
    html.P('Alberto Lagos  '
           'Industrial Eng.'
           )
], style=NAME_4)

name_5 = html.Div([
    html.P('Diego Mora  '
           'Electronic Eng.'
           )
], style=NAME_5)

name_6 = html.Div([
    html.P('Luis Parra  '
           'Civil Eng.'
           )
], style=NAME_6)


##############################
# General Layout
##############################
general = html.Div(id='general_description', children=[
    bck_ph,
    bg,
    ph1,
    ph2,
    ph3,
    ph4,
    ph5,
    ph6,
    text,
    name_1,
    name_2,
    name_3,
    name_4,
    name_5,
    name_6
])
