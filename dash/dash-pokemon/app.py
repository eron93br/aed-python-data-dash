from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

DATASET_PATH = "assets/pokemon.csv"

# Carregadar o dataset
# (1) carregar o dataset
df = pd.read_csv(DATASET_PATH)

# (2) Operações necessárias
list_generations = df.Generation.unique()
list_type = df["Type 1"].unique()

app = Dash(__name__)

# Definir o layout do dashboard aqui!!!!

app.layout = html.Div(
    [
        html.H1(
            "Dashboard Pokemon",
            style={"textAlign": "center"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Dropdown(
                            options=list_generations,
                            value=list_generations[0],
                            id="drop-gen",
                        )
                    ],
                    style={
                        "display": "inline-block",
                        "margin-left": "300px",
                        "width": "15%",
                    },
                ),
                html.Div(
                    [
                        dcc.Dropdown(
                            options=list_type, value=list_type[0], id="drop-type"
                        )
                    ],
                    style={
                        "display": "inline-block",
                        "margin-left": "300px",
                        "width": "15%",
                    },
                ),
                # core componenet do dropdown da geração
                # core componenet do dropdown do tipo de pokemon
            ],
            style={"display": "flex"},
        ),
        html.H2("Tipos por Geração de Pokemon"),
        dcc.Graph(id="figura1"),
        html.H2("Boxplot do Attack por Tipo"),
        dcc.Graph(id="figura2"),
    ]
)

# definir a callback
@app.callback(
    Output("figura1", "figure"),
    Output("figura2", "figure"),
    Input("drop-gen", "value"),
    Input("drop-type", "value"),
)
def update_output(sel_generation, sel_type):
    print(f"Você selecionou a {sel_generation} geração e tipo {sel_type}")
    # 1- Rotina da Primeira Figura
    df2 = df.loc[df.Generation == sel_generation]
    pok2 = df2.groupby(["Type 1"]).count()
    pok2.reset_index()
    pok2.reset_index(inplace=True)
    # Definição da Primeira figura
    fig1 = px.bar(pok2, x="Type 1", y="Total", hover_data=["Type 1"], barmode="stack")
    # 2 - Rotina da Segunda Figura
    df3 = df.loc[df.Generation == sel_generation & (df["Type 1"] == sel_type)]
    fig2 = px.box(df3, y="Attack")
    return fig1, fig2


if __name__ == "__main__":
    app.run_server(debug=True)
