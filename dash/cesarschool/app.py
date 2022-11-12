from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd 
from utils import CONVERT_RATE

# Carregadar o dataset
# https://www.kaggle.com/datasets/iamsouravbanerjee/software-professional-salaries-2022?resource=download

# Descobertas a partir do dataset
# (1) carregar o dataset
df = pd.read_csv("data/salaries.csv")
dfs = pd.read_csv("https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/active_cases_2020-07-17_0800.csv")
# (2) achar os cinco empregos mais populares
titulos_top = df['Job Title'].value_counts().sort_values(ascending=False).head(7)
lista_empregos = titulos_top.index


app = Dash(__name__)

# Definir o layout do dashboard aqui!!!!

app.layout = html.Div([
    html.H1("Dashboard CESAR School 12 Novembro 2022", style={"textAlign": "center"},),
    html.H6("Digite o Cargo para análise:"),
    dcc.Dropdown(options= lista_empregos, 
                 value=lista_empregos[0], 
                 id='dropdown_emprego'),
    html.H6("Digite o tipo de gráfico desejado:"),
    dcc.RadioItems(options=['Boxplot', 'Gráfico de Barra'],
                  value='Boxplot',
                  id='tipo-grafico',
                  inline=True),
    html.Hr(),
    dcc.Graph(id='figura1'),
    html.H2("mapa..."),
    dcc.Graph(id='figura2'),
])

# definir a callback que define o titulo do emprego
@app.callback(
    Output('figura1', 'figure'),
    Output('figura2', 'figure'),
    Input('dropdown_emprego', 'value'),
    Input('tipo-grafico', 'value'),
)
def update_output(value_emprego, value_tipo_grafico):
    print(f"Opção selecionada {value_emprego} | {value_tipo_grafico}")
    df1 = df[df['Job Title'] == value_emprego]
    if(value_tipo_grafico == 'Boxplot'):
        fig1 = px.box(df1, y="Salary", x='Location')
    elif(value_tipo_grafico == 'Gráfico de Barra'):
        #TODO: alterar para outro tipo de gŕafico desejado!
        fig1 = px.box(df1, y="Salary", x='Location')

    fig2 = px.choropleth(
        dfs,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='state',
        color='active cases',
        color_continuous_scale='Blues'
    )

    fig2.update_geos(fitbounds="locations", visible=False)

    return fig1, fig2

if __name__ == '__main__':
    app.run_server(debug=True)