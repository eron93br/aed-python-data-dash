import dash
from dash import Dash, dcc, html, Input, Output
import dash_core_components as dcc
import dash_html_components as html
from utils import DATASET

# import plotly express!
import plotly.express as px

# Importar pandas!
import pandas as pd

# Create the Dash application
app = dash.Dash(__name__)

# PASSO 1 - IMPORTAR OS DADOS e definir parâmetros do dataset
df = pd.read_csv(DATASET)
TIMES = df.clube.unique()

# FIXME: apagar isso


# PASSO 2 - DEFINIR O LAYOUT DO NOSSO DASHBOARD!
app.layout = html.Div(
    children=[
        html.H1(
            "Gols do Campeonato Brasileiro", style={"text-align": "center"}
        ),
        dcc.Dropdown(
            TIMES,
            value="Sport",
            id="drop-time",
            style={
                "display": "inline-block",
                "margin-left": "100px",
                "width": "200px",
            },
        ),
        dcc.RangeSlider(1, 38, 1, value=[1, 38], id='slider-rodada'),
        dcc.Graph(id="figura-gols"),
        dcc.Graph(id="figura-tipo"),
    ]
)

# Define callback function for the dropdown
@app.callback(
    Output("figura-gols", "figure"),
    Output("figura-tipo", "figure"),
    Input("drop-time", "value"),
    Input("slider-rodada", "value"),
)
def update_figura_time(nome_do_time, rodada):
    #TODO: PRECISO CRIAR A FIGURA AQUI!!!!!!!!!!!1
    print(f"Você selecionou o time: {nome_do_time}")
    print(f"Selecionada rodada: {rodada}")
    # Filtrar pelo time
    dfs = df.loc[df['clube'] == nome_do_time]
    #
    dff = dfs.loc[(dfs['rodata']>= rodada[0]) & (dfs['rodata'] <= rodada[1])]
    fig1 = px.bar(dff, x="atleta")
    #
    fig2 = px.bar(dff, x="tipo_de_gol")
    return fig1, fig2


# Run the application
if __name__ == "__main__":
    app.run_server(debug=True)
