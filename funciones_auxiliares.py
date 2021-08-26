import pandas as pd
import geopandas
import os
import plotly.express as px
import json
from plotly.offline import plot
import plotly.figure_factory as ff
from geopandas.tools import sjoin

#cte color letra de los graficos
PLOT_COLOR = '#F0F5FF'


def cargar_geojson(path):
    """Carga un archivo de formato geojson.

    Parametros:
        path: path del archivo
    """

    with open(path, 'r') as file:
        geo_df = json.load(file)
    return geo_df


def cargar_df(path, districts_path):
    """Carga dos archivos geojson como geopandas dataframe.

    El primero es el archivo original de motos y grids, el segundo
    describe los distritos de Madrid.

    Se calculan los centroides de las celdas de la malla del primer geojson,
    posteriormente se hace un spatial join para determinar en que distrito
    está contenida esa celda.

    Parametros:
        path: path del archivo original de motos
        districts_path: path del archivo distritos
    """

    df = geopandas.read_file(path, dtypes= {'id':str})
    df['perc_value'] = df['perc'].str.replace(',', '.').str.replace(' %', '').astype(float)
    # perc_value suma 99.56
    
    df.rename(columns = {'geometry':'polygon_geometry'},
                inplace = True)    

    df['geometry'] = df.apply(lambda a: a['polygon_geometry'].centroid,
                                            axis = 1)

    distritos = geopandas.read_file(districts_path)

    merged = sjoin(df.drop(columns = list(filter(lambda a: 'index_' in a,\
                                                    df.columns))),
                distritos[['coddistrit', 'nombre', 'geometry']],
                op = 'intersects', how = 'left')
    merged['time_stopped_text'] = merged.apply(lambda x: f"{x['time_stopped']:,.1f}",
                                            axis=1)
    merged['vehicle_id_text'] = merged.apply(lambda x: f"{x['vehicle_id']:,.1f}",
                                            axis=1)                
    return merged


def display_choropleth(df, geojson):
    """Devuelve la figura correspondiente al mapa coroplético

    Parametros:
        df: dataframe de las motos
        geojson: json de las motos.
    """    
    fig = px.choropleth_mapbox(
        df,
        geojson=geojson, 
        color = 'count',
        mapbox_style="carto-positron",
        range_color=(df['count'].min(), df['count'].max()),
        locations = 'id',
        zoom=11,
        center = {"lat": 40.4667,
                  "lon": -3.70325},
        hover_data = ['id', 'count', 'perc', 'time_stopped_text', 'vehicle_id_text'],
        labels = {'count':'#motos disponibles',
                'time_stopped_text': 'Media tiempo parada',
                'vehicle_id_text': 'Media vehicle id'
                },
        opacity=0.5,
                
        )

    fig.update_layout(
                     margin={"r":30,"t":30,"l":30,"b":30},
                    autosize = True,
                    coloraxis_colorbar_x=-0.15,
                    paper_bgcolor='#3F5892',
                    font_color=PLOT_COLOR,
                    )

    return fig

def create_table(df):
    """Devuelve la figura correspondiente a la tabla.

    Parametros:
        df: dataframe de las motos
    """      

    motos_disponibles = f"{df['count'].sum():,.0f}"
    max_tiempo_parada = f"{df.sort_values('time_stopped', ascending = False).head(1)['time_stopped'].values[0]:,.2f}"
    grid_id_max_tiempo_parada = df.sort_values('time_stopped', ascending = False).head(1)['id'].values[0]
    #media ponderada por el numero de motos disponibles en cada grid (count)
    media_total_tiempo_parada = f"{((df['count'] * df['time_stopped']) / df['count'].sum()).sum():,.2f}"

    table = pd.DataFrame(
                        {'Dato': ['Cantidad total de motos disponibles',
                                'Máximo tiempo parada de un grid',
                                'Grid id con máximo tiempo de parada',
                                'Media total de tiempo de parada'],
                        'Valor': [motos_disponibles,
                                max_tiempo_parada,
                                grid_id_max_tiempo_parada,
                                media_total_tiempo_parada]
                        }
                    )

    fig = ff.create_table(table)
    fig.update_layout(margin={"r":30,"t":30,"l":30,"b":30},
                        autosize = True,
                        font_color=PLOT_COLOR,
                        paper_bgcolor='#3F5892'
                    )
    return fig

def create_histogram_count(df):
    """Devuelve la figura correspondiente al histograma.

    Parametros:
        df: dataframe de las motos
    """       
    fig = px.histogram(df, 
                       x="count",
                       labels = {'count': '# Motos Disponibles'})
    fig.update_layout(bargap=0.2,
                        margin={"r":30,"t":30,"l":30,"b":75},
                        autosize = True,
                        paper_bgcolor='#3F5892', 
                       font_color=PLOT_COLOR
                    )
    return fig
    
def create_pie_chart(df):
    """Devuelve la figura correspondiente al pie chart.

    Parametros:
        df: dataframe de las motos
    """      
    fig = px.pie(df,
             values='coddistrit',
             names='nombre',
             labels = {'coddistrit': '# motos disp.',
                       'nombre': 'distrito'},
            hole=0.2)
    fig.update_layout( margin={"r":50,"t":30,"l":0,"b":45},
                        autosize = True,
                        paper_bgcolor='#3F5892',
                        font_color=PLOT_COLOR
                    )
    return fig