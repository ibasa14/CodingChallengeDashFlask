from flask import Flask
from dash import Dash
import dash_html_components as html
import dash_core_components as dcc
from funciones_auxiliares import cargar_df, cargar_geojson, display_choropleth,\
                                 create_table, create_histogram_count,\
                                create_pie_chart

# Se cargan datos
df = cargar_df('dataset_motos.geojson', 'distritos.geojson')
geojson = cargar_geojson('dataset_motos.geojson')

# Paths para archivos contenidos en assets
external_stylesheets = [
    {
        "href": "styles.css",
        "rel": "stylesheet",
    },
    {
        "href": "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css",
        'integrity':"sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh",
        "crossorigin":"anonymous",
        "rel": "stylesheet"
    }
]
external_scripts = [
    {
        'src': 'https://code.jquery.com/jquery-3.4.1.slim.min.js',
        'integrity': 'sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n',
        'crossorigin': 'anonymous'
    },
    {
        'src': 'https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js',
        'integrity': 'sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo',
        'crossorigin': 'anonymous'
    },
    {
        'src': 'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js',
        'integrity': 'sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6',
        'crossorigin': 'anonymous'
    },
]


# Configuracion flask + dash
server = Flask(__name__)
app = Dash(
    __name__,
    server=server,
    url_base_pathname='/dash/',
    external_scripts=external_scripts,
    external_stylesheets=external_stylesheets
)

# layout
app.layout = html.Div(
    className = 'row',
    children = [
        html.Div(
            className = 'col-8',
            children = [
                html.Div(
                    className = 'map-container',

                    children = [
                        dcc.Graph(
                            style={'height':'100%'},
                            id='map',
                            figure =  display_choropleth(df, geojson)
                        )
                    ]                
                )
            ]
        ),
        html.Div(
            className = 'col-4',
            style= {'margin-top': '2vh'},
            children = [
                html.Div(
                    className = 'table-container',
                    children = [
                          dcc.Graph(
                              style={'height':'100%'},
                              id='table',
                              figure = create_table(df)
                          )

                    ]
                )   ,      

                html.Div(
                    className = 'graph',
                    children = [
                          dcc.Graph(
                              style={'height':'100%'},
                              id='histogram',
                              figure = create_histogram_count(df)
                          )
                    ]
                )   ,

                html.Div(
                    className = 'graph',
                    children = [
                          dcc.Graph(
                              style={'height':'100%'},
                              id='pie_chart',
                              figure = create_pie_chart(df.loc[~df['nombre'].isna()])
                          ) 
                   ]
                )                                           

            ]
        )        
    ]

)

@server.route("/dash")
def my_dash_app():
    return app.index()

if __name__ == '__main__':
    app.run_server(debug = False, port = 5000)
