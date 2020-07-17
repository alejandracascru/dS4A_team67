#Basics Requirements
import dash_html_components as html

# Recall app
from app import app
from lib import sidebar

benchmark = html.Div(
    [
        sidebar.sidebar
    ]
)
#benchmark = html.P('Fabio A. Lagos')

