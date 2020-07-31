# Basics Requirements
import dash_html_components as html

# ------------------------------
# 1. Styles
# ------------------------------

# 1.1 text
STYLE_DOC = {
    "position": "absolute",
    "width": "70%",
    "height": "400px",
    "left": "10%",
    "top": "115px",
    #"border": "10px solid #e7eff6",
    #"border-radius": "10px",
    'color': '#072552',
    'fontSize': 16,
    'text-align': 'justify'
}


text = html.Div(className='control-tab', children=[

            html.Br(),
            html.Br(),
            html.H1(children='Documentation'),
            html.Br(),
            html.H3(children='Data Sources & Important Documentation'),
            html.P('For this project, we gather multiple data from different '
                   'open sources. All the data used to build this product '
                   'is available in the links below. If you want to continue or '
                   'use this project for future investigations, we provide the link '
                   'to the git hub repository where you can find all the code:'
                   ),
            html.Br(),
            html.H5(children='Ministry of Education'),
            html.Label(['- Basic Education Statistics: ', html.A('link', href='https://www.datos.gov.co/Educaci-n/ESTADISTICAS-EN-EDUCACION-BASICA-POR-MUNICIPIO/nudc-7mev',target="_blank")]),
            html.Br(),
            html.Label(['- School Enrollment Data: ', html.A('link', href='https://www.datos.gov.co/Educaci-n/MEN_MATRICULA-ESTADISTICA_EPBM/ngw5-c5nw',target="_blank")]),
            html.Br(),
            html.Label(['- School Enrollment Data: ', html.A('link', href='https://www.datos.gov.co/Educaci-n/MEN_MATRICULA-ESTADISTICA_EPBM/ngw5-c5nw',target="_blank")]),
            html.Br(),
            html.Br(),
            html.H5(children='ICFES'),
            html.Label(['- Government official test results: ', html.A('link', href='https://www.datos.gov.co/Educaci-n/Resultados-Saber-11-/t6je-7yrd',target="_blank")]),
            html.Br(),
            html.Br(),
            html.H5(children='DANE'),
            html.Label(['- Formal Education 2019 Survey: ', html.A('link', href='http://microdatos.dane.gov.co/index.php/catalog/669/study-description',target="_blank")]),
            html.Br(),
            html.Label(['- School Enrollment Data: ', html.A('link', href='https://www.datos.gov.co/Educaci-n/MEN_MATRICULA-ESTADISTICA_EPBM/ngw5-c5nw',target="_blank")]),
            html.Br(),
            html.Label(['- Household Survey: ', html.A('link', href='http://microdatos.dane.gov.co/index.php/catalog/116',target="_blank")]),
            html.Br(),
            html.Label(['- Financial Household Survey: ', html.A('link', href='http://microdatos.dane.gov.co/index.php/catalog/626',target="_blank")]),
            html.Br(),
            html.Label(['- School to Work Transition Survey: ', html.A('link', href='http://microdatos.dane.gov.co/index.php/catalog/518/data_dictionary',target="_blank")]),
            html.Br(),
            html.Br(),
            html.H5(children='SISBEN'),
            html.Label(['- SISBEN Open Data: ', html.A('link', href='https://www2.sisben.gov.co/Datos%20del%20sisb%C3%A9n/Paginas/Bases-de-datos-anonimizadas.aspx',target="_blank")]),
            html.Br(),
            html.Br(),
            html.H5(children='POLICE'),
            html.Label(['- National Police Open Data: ', html.A('link', href='https://www.policia.gov.co/grupo-informaci%C3%B3n-criminalidad/estadistica-delictiva',target="_blank")]),
            html.Br(),
            html.Br(),
            html.H5(children='Git Hub Repository'),
            html.Label([html.A('link', href='https://github.com/alejandracascru/dS4A_team67',target="_blank")]),
            html.Br(),
            html.Br()

            #html.Label(['- School Enrollment Data: ', html.A('link', href='')]),

], style=STYLE_DOC)


##############################
# General Layout
##############################
documentation = html.Div(id='documentation', children=[
    text
])
