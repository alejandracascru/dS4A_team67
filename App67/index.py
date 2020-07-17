import dash
import dash_html_components as html

# Recall app
from app import app
###########################################################
#
#           APP LAYOUT:
#
###########################################################

# LOAD THE DIFFERENT FILES
from lib import title, tab_bar

# PLACE THE COMPONENTS IN THE LAYOUT

app.layout = html.Div([
    title.title,
    tab_bar.tab_bar
])

if __name__ == '__main__':
    app.run_server(debug=True)
