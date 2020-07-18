#Basics Requirements
import dash_html_components as html

# Recall app
from app import app
from library.elements_all import sidebar

clustering = html.Div(
    [
        sidebar.sidebar
    ]
)
#benchmark = html.P('Fabio A. Lagos')

