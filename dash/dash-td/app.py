# Import required libraries
import pickle
import copy
import pathlib
import urllib.request
import dash
import math
import datetime as dt
import pandas as pd
from dash.dependencies import Input, Output, State, ClientsideFunction
from dash import dcc
from dash import html
import plotly.express as px
import plotly.graph_objects as go
import operator
import os
from datetime import datetime, date, timedelta
import yfinance as yf
import base64
import io

# TODO: MOCK DAS FUNCIONALIDADES DO CSV-------------------------------------------------
def stockData(stock_name, start_date, end_date=date.today(), country="US"):
    """
    This function return a dataframe with the price of the stock
    since the start_date until the end_date.
    """
    stock = stock_name
    if country == "BR":
        stock = stock_name + ".SA"
    df = pd.DataFrame()
    # import data to data frame
    df = yf.download(stock, start=start_date, end=end_date)
    return df

# ---------------------------------------------------------------------------------------

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)
app.title = "Extrato B3"
server = app.server

# Create global chart template
mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h"),
    title="Satellite Overview",
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(lon=-78.05, lat=42.54),
        zoom=7,
    ),
)

# eron grafico/callback #1
@app.callback(
    Output("plotly_figura1", "figure"),
    Output("card_value1", "children"),
    Output("card_value2", "children"),
    Input("upload-data", "contents"),
    Input("upload-data", "filename"),
    Input("investimento_selector", "value"),
    Input("index_type_selector", "value"),
)
def update_graph_1(contents, filename, investimento, indexador):
    print(f"Escolha TIPO {investimento}| INDEX {indexador}")

    # analise do tesouro direto
    if investimento == "tesouro":
        # (1) get data frame ---
        df = parse_contents(contents, filename, "Tesouro Direto")
        dfa = df.dropna(axis=0)  # limpar os NaN do dataframe, caso tenha!
        dfc = df.drop(["Código ISIN", "Motivo", "Quantidade Disponível"], axis=1)
        investimentos_td = dfc["Produto"].unique()
        df_ipca = dfc[dfc["Indexador"] == indexador]
        ntnb = pd.pivot_table(
            df_ipca, index=["Produto"], values=["Valor Aplicado"], aggfunc="sum"
        )
        # (2) calculate card values ---
        rcard2 = "{:.2f}".format(dfc["Valor Aplicado"].sum())
        rcard1 = len(list(dfc["Produto"].unique()))
        # ativos_lista = df["Produto"].unique()  # numero de ativos diferentes
        # (3) figure Routine ---
        fig = px.pie(ntnb, values="Valor Aplicado", names=ntnb.index)
        fig.update_layout(
            title="Portfolio de Investimentos TD",
        )
        return fig, rcard1, rcard2
    elif investimento == "acoes":
        dfa = parse_contents(contents, filename, "Acoes")
        dfa = dfa.dropna(axis=0)  # limpar os NaN do dataframe, caso tenha!
        # calculate card values
        rcard2 = "{:.2f}".format(dfa["Valor Atualizado"].sum())
        rcard1 = len(dfa["Produto"].unique())  # numero de ativos diferentes
        # ativos_lista = dfa["Produto"].unique()
        # Figure Routine ---
        fig = px.pie(dfa, values="Valor Atualizado", names="Produto")
        fig.update_layout(
            title="Portfolio de Investimentos Ações",
        )
        return fig, rcard1, rcard2


@app.callback(
    Output("risco_carteira", "children"),
    Output("total_investido", "children"),
    Input("upload-data", "contents"),
    Input("upload-data", "filename"),
)
def update_graph_2(contents, filename):
    # TODO: here...
    renda_fixa = parse_contents(contents, filename, "Tesouro Direto")
    renda_var = parse_contents(contents, filename, "Acoes")
    renda_fixa = renda_fixa.drop(
        ["Código ISIN", "Motivo", "Quantidade Disponível"], axis=1
    )
    renda_var = renda_var.dropna(axis=0)  # limpar os NaN do dataframe, caso tenha!

    pos_rf = renda_fixa["Valor Aplicado"].sum()
    pos_rvar = renda_var["Valor Atualizado"].sum()

    risk = (0.25 * pos_rf + 0.75 * pos_rvar) / (pos_rvar + pos_rf)

    # Set outputs
    risk = "{:.2f}".format(risk)
    total_inv = "{:.2f}".format(pos_rvar + pos_rf)

    return risk, total_inv


# stock callback
@app.callback(
    Output("plotly_figura2", "figure"),
    Input("button-example-1", "n_clicks"),
    State("input-box", "value"),
)
def update_output(n_clicks, value):
    try:
        stock_df = stockData(
            value, start_date="2020-01-03", end_date="2021-03-31", country="BR"
        )
    except Exception as e:
        print("Erro no ticker da Ação desejada!")        
    fig_stock = px.line(
        stock_df,
        y="Close",
        title=f"Variação valor fechamento de {value}",
    )
    return fig_stock


# Create app layout
app.layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src="/assets/logo.png",
                            id="plotly-image",
                            style={
                                "height": "100px",
                                "width": "auto",
                                "margin-bottom": "25px",
                            },
                        )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Extrato B3",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Analise de Investimentos",
                                    style={"margin-top": "0px"},
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                # --- BOTAO DE LEARN MORE ---
                html.Div(
                    [
                        html.A(
                            html.Button("Saiba Mais", id="learn-more-button"),
                            href="https://atendimento.b3.com.br/atendimento?id=kb_category_b3&kb_category=83cbb04c1b7f281015b36538fa4bcb66&kb_id=f2c2829f1b3d1050b9da23853a4bcbb5",
                        )
                    ],
                    className="one-third column",
                    id="button",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        # BARRA LATERAL ESQUERDA TODO:
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            "Realize o Uploado arquivo extrato B3:",
                            className="control_label",
                        ),
                        dcc.Upload(
                            id="upload-data",
                            children=html.Div(
                                ["Drag and Drop or ", html.A("Select Files")]
                            ),
                            style={
                                "width": "95%",
                                "height": "60px",
                                "lineHeight": "60px",
                                "borderWidth": "1px",
                                "borderStyle": "dashed",
                                "borderRadius": "5px",
                                "textAlign": "center",
                                "margin": "10px",
                            },
                            # Not allow multiple files to be uploaded
                            multiple=False,
                        ),
                        html.P(
                            "Selecione o tipo de investimento p/ Análise:",
                            className="control_label",
                        ),
                        dcc.RadioItems(
                            id="investimento_selector",  # antigo well_status_selector
                            options=[
                                {
                                    "label": "TesouroDireto ",
                                    "value": "tesouro",
                                },  # active
                                {"label": "Ações ", "value": "acoes"},  # custom
                            ],
                            value="tesouro",
                            labelStyle={
                                "display": "inline-block",
                                "margin-left": "40px",
                            },
                            className="dcc_control",
                        ),
                        html.P(
                            "Selecione o Indexador de Renda Fixa:",
                            className="control_label",
                        ),
                        dcc.RadioItems(
                            id="index_type_selector",  #
                            options=[
                                {"label": "SELIC", "value": "SELIC"},  # active
                                {"label": "IPCA ", "value": "IPCA"},  # custom
                            ],
                            value="IPCA",
                            labelStyle={
                                "display": "inline-block",
                                "margin-left": "50px",
                                "margin-right": "30px",
                            },
                            className="dcc_control",
                        ),
                        # dcc.Dropdown(
                        #     id="my-dynamic-dropdown",
                        #     value="my-dynamic-dropdown-value",
                        #     multi=False,
                        # ),
                    ],
                    className="pretty_container four columns",
                    id="cross-filter-options",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6("Total de Ativos"),
                                        html.H6(
                                            id="card_value1",
                                            style={"textAlign": "center"},
                                        ),
                                    ],
                                    className="mini_container",
                                ),
                                html.Div(
                                    [
                                        html.H6("Valor Investido"),
                                        html.H6(
                                            id="card_value2",
                                            style={"textAlign": "center"},
                                        ),
                                    ],
                                    id="gas",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [
                                        html.H6(
                                            "Risco da Carteira", style={"fontSize": 18}
                                        ),
                                        html.H6(
                                            id="risco_carteira",
                                            style={"textAlign": "center"},
                                        ),
                                    ],  
                                    id="oil",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [
                                        html.H6("Total Investido"),
                                        html.H6(
                                            id="total_investido",
                                            style={"textAlign": "center"},
                                        ),
                                    ], 
                                    id="water",
                                    className="mini_container",
                                ),
                            ],
                            id="info-container",
                            className="row container-display",
                        ),
                        html.Div(
                            [
                                dcc.Graph(id="plotly_figura1")
                            ],  # # eron grafico/callback #1
                            id="countGraphContainer",
                            className="pretty_container",
                        ),
                    ],
                    id="right-column",
                    className="eight columns",
                ),
            ],
            className="row flex-display",
        ),
        # TERCEIRA LINHA -------
        html.Div(
            [
                # STOCK ROUTINE
                html.Div(
                    [
                        html.H6("Digite o a Ação para Analise: "),
                        html.Div(
                            [
                                html.Div(dcc.Input(id="input-box", type="text")),
                                html.Button("Submit", id="button-example-1", value='PETR4'),
                            ],
                        ),
                        dcc.Graph(id="plotly_figura2"),
                        html.Div(id="output-container-button"),
                        html.H6(
                            "Desenvolvido por Eronides Neto - AED CESAR SCHOOL 2022.1",
                            style={"textAlign": "center"},
                        ),
                    ],
                    className="pretty_container twelve columns",
                ),
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)


# -------------------------------------- base functions ------------------------------------------------------------------------------------


def parse_contents(contents, filename, inv_type):
    print(f"Arquivo Selecionado: {filename}")
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)

    try:
        if "xlsx" in filename:
            df = pd.read_excel(io.BytesIO(decoded), sheet_name=inv_type)
        else:
            print("Arquivo Invalido!")
            return None
    except Exception as e:
        print("Arquivo Invalido!")
        return None

    return df


# --------------------------------------------- Create callbacks ---------------------------------------------------------------------------
app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="resize"),
    Output("output-clientside", "children"),
    [Input("count_graph", "figure")],
)

# Main
if __name__ == "__main__":
    app.run_server(debug=True)
