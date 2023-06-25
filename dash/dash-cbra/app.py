import pathlib
import json
from datetime import datetime
import flask
import dash
from dash import dash_table
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import plotly.graph_objs as go
import plotly.express as px
import requests
from io import BytesIO
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input, State
from utils import LOGO, DATASET, LINK_BRASILEIRAO, BALL_ICON
import requests
from bs4 import BeautifulSoup
import urllib

def get_wikipedia_image_link(page_title):
    # Construct the URL of the Wikipedia page
    url = f"{page_title}"

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the infobox image element
    infobox_image = soup.find("table", class_="infobox").find("img")

    # Extract the source attribute (image link) from the image element
    image_link = infobox_image["src"]
    image_link = image_link[2:]
    result = 'https://' + image_link
    return result

df = pd.read_csv(DATASET)
TIMES = df.clube.unique()
time_dict = {string: len(string) for string in TIMES}

time_dict['Fluminense']= 'https://pt.wikipedia.org/wiki/Fluminense_Football_Club'
time_dict['Internacional'] = 'https://pt.wikipedia.org/wiki/Sport_Club_Internacional'
time_dict['Sao Paulo'] = 'https://pt.wikipedia.org/wiki/S%C3%A3o_Paulo_Futebol_Clube'
time_dict['Cruzeiro'] = 'https://pt.wikipedia.org/wiki/Cruzeiro_Esporte_Clube'
time_dict['Palmeiras'] = 'https://pt.wikipedia.org/wiki/Sociedade_Esportiva_Palmeiras'
time_dict['Santos'] = 'https://pt.wikipedia.org/wiki/Santos_Futebol_Clube'
time_dict['Bahia'] = 'https://pt.wikipedia.org/wiki/Esporte_Clube_Bahia'
time_dict['Sport'] = 'https://pt.wikipedia.org/wiki/Sport_Club_do_Recife'
time_dict['Athletico-PR'] = 'https://pt.wikipedia.org/wiki/Club_Athletico_Paranaense'
time_dict['Criciuma'] = 'https://pt.wikipedia.org/wiki/Crici%C3%BAma_Esporte_Clube'
time_dict['Botafogo-RJ'] = 'https://pt.wikipedia.org/wiki/Botafogo_de_Futebol_e_Regatas'
time_dict['Vitoria'] = 'https://pt.wikipedia.org/wiki/Esporte_Clube_Vit%C3%B3ria'
time_dict['Corinthians'] = 'https://pt.wikipedia.org/wiki/Sport_Club_Corinthians_Paulista'
time_dict['Goias'] = 'https://pt.wikipedia.org/wiki/Goi%C3%A1s_Esporte_Clube'
time_dict['Gremio'] = 'https://pt.wikipedia.org/wiki/Gr%C3%AAmio_Foot-Ball_Porto_Alegrense'
time_dict['Atletico-MG'] = 'https://pt.wikipedia.org/wiki/Clube_Atl%C3%A9tico_Mineiro'
time_dict['Chapecoense'] = 'https://pt.wikipedia.org/wiki/Associa%C3%A7%C3%A3o_Chapecoense_de_Futebol'
time_dict['Coritiba'] = 'https://pt.wikipedia.org/wiki/Coritiba_Foot_Ball_Club'
time_dict['Flamengo'] = 'https://pt.wikipedia.org/wiki/Clube_de_Regatas_do_Flamengo'
time_dict['Figueirense'] = 'https://pt.wikipedia.org/wiki/Figueirense_Futebol_Clube'
time_dict['Ponte Preta'] = 'https://pt.wikipedia.org/wiki/Associa%C3%A7%C3%A3o_Atl%C3%A9tica_Ponte_Preta'
time_dict['Avai'] = 'https://pt.wikipedia.org/wiki/Ava%C3%AD_Futebol_Clube'
time_dict['Vasco'] = 'https://pt.wikipedia.org/wiki/Club_de_Regatas_Vasco_da_Gama'
time_dict['Joinville'] = 'https://pt.wikipedia.org/wiki/Joinville_Esporte_Clube'
time_dict['Santa Cruz'] = 'https://pt.wikipedia.org/wiki/Santa_Cruz_Futebol_Clube'
time_dict['America-MG'] = 'https://pt.wikipedia.org/wiki/Am%C3%A9rica_Futebol_Clube_(Belo_Horizonte)'
time_dict['Atletico-GO'] = 'https://pt.wikipedia.org/wiki/Atl%C3%A9tico_Clube_Goianiense'
time_dict['Parana'] = 'https://pt.wikipedia.org/wiki/Paran%C3%A1_Clube'
time_dict['Ceara'] = 'https://pt.wikipedia.org/wiki/Cear%C3%A1_Sporting_Club'
time_dict['Fortaleza'] = 'https://pt.wikipedia.org/wiki/Fortaleza_Esporte_Clube'
time_dict['CSA'] = 'https://pt.wikipedia.org/wiki/Centro_Sportivo_Alagoano'
time_dict['Bragantino'] = 'https://pt.wikipedia.org/wiki/Red_Bull_Bragantino'
time_dict['Cuiaba'] = 'https://pt.wikipedia.org/wiki/Cuiab%C3%A1_Esporte_Clube'
time_dict['Juventude'] = 'https://pt.wikipedia.org/wiki/Esporte_Clube_Juventude'

DATA_PATH = pathlib.Path(__file__).parent.resolve()
EXTERNAL_STYLESHEETS = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

NAVBAR = dbc.Navbar(
    children=[
        html.A(
            dbc.Row(
                [
                    dbc.Col(html.Img(src=LOGO, height="30px")),
                    dbc.Col(
                        dbc.NavbarBrand("Dashboard Brasileirão", className="ml-2")
                    ),
                ],
                align="center",
                no_gutters=True,
            ),
            href=LINK_BRASILEIRAO,
        )
    ],
    color="green",
    dark=True,
    sticky="top",
)

LEFT_COLUMN = dbc.Jumbotron(
    [
        html.H5(children="Selecione as rodadas", className="display-5"),
        html.Hr(className="my-2"),
        dcc.RangeSlider(1, 38, 4, value=[1, 38], id='slider-rodada'),
        html.Div(
            style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'},
            children=[
                html.Img(id='image-escudo', style={'justify-content': 'center', 'align-items': 'center'}),
            ]
        ),
    ]
)

GRAPH_TIPOS_GOLS = [
    dbc.CardHeader([
        dbc.Row([
            html.Img(src=BALL_ICON, height="30px"),
            html.H5("Os tipos de gols marcados por rodada", style={"marginLeft": 10}),
            html.Img(src=BALL_ICON, height="30px", style={"marginLeft": 10}),
    ]),
    ]),
    dbc.CardBody(
        [
            dcc.Graph(id="figura-tipo"),
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]


GRAPH_GOLEADORES = [
    dbc.CardHeader(html.H5("Análise Detalhada dos gols no Brasileirão - Série A")),
    dbc.CardBody(
        [
            dcc.Loading(
                id="loading-bigrams-comps",
                children=[
                    dbc.Row(
                        [
                            dbc.Col(html.P("Escolha o time:"), md=12),
                            dbc.Col(
                                [
                                    dcc.Dropdown(
                                        id="drop-time",
                                        options=TIMES,
                                        value="Sport",
                                    )
                                ],
                                md=6,
                            ),
                            #FIXME: Se você desejar outrar coluna, usar esta estrutura!
                            # dbc.Col(
                            #     [
                            #         dcc.Dropdown(
                            #             id="bigrams-comp_2",
                            #             options=[
                            #                 {"label": i, "value": i}
                            #                 for i in bigram_df.company.unique()
                            #             ],
                            #             value="TRANSUNION INTERMEDIATE HOLDINGS, INC.",
                            #         )
                            #     ],
                            #     md=6,
                            # ),
                        ]
                    ),
                    dcc.Graph(id="figura-gols"),
                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]

BODY = dbc.Container(
    [
        dbc.Row([dbc.Col(dbc.Card(GRAPH_GOLEADORES)),], style={"marginTop": 30}),
        dbc.Row(
            [
                dbc.Col(LEFT_COLUMN, md=4, align="center"),
                dbc.Col(dbc.Card(GRAPH_TIPOS_GOLS), md=8),
            ],
            style={"marginTop": 30},
        ),
    ],
    className="mt-12",
)


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server 

app.layout = html.Div(children=[NAVBAR, BODY])

@app.callback(
    Output("image-escudo", "src"),
    Output("figura-gols", "figure"),
    Output("figura-tipo", "figure"),
    Input("drop-time", "value"),
    Input("slider-rodada", "value"),
)
def update_figura_time(nome_do_time, rodada):
    print(f"Você selecionou o time: {nome_do_time}")
    # Direcionar link do escudo do time
    image_url = get_wikipedia_image_link(time_dict[nome_do_time])
    # Filtrar pelo time
    dfs = df.loc[df['clube'] == nome_do_time]
    # Filtar os tipos de gol pela rodada
    dff = dfs.loc[(dfs['rodata']>= rodada[0]) & (dfs['rodata'] <= rodada[1])]
    # Processo de criar as figuras baseados nos filtos personalizados
    dff_sorted = dfs.value_counts('atleta', ascending=False) 
    fig1 = px.bar(dff_sorted[:7], labels={"value": "Número de Gols Marcados"}, text="value")
    fig2 = px.bar(dff, x="tipo_de_gol")
    return image_url, fig1, fig2



if __name__ == "__main__":
    app.run_server(debug=True)
