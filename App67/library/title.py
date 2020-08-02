# Basics Requirements
import dash_html_components as html

# Recall app
from app import app

####################################################################################
# Add the title
####################################################################################

DS4A_Img = html.Img(src=app.get_asset_url("img/ds4a-img-03.svg"),
                    style={'width': '15%', 'float': 'right', 'padding-right': '3%'})

Project_Title = html.H1(children=["School Desertion in Colombia", DS4A_Img],
                        style={'padding': '20px 0px 0px 0px'})

title = html.Div(className="main-title", children=[Project_Title], id="title")