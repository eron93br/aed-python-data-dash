import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import datetime 
from bcb import currency, Expectativas, sgs, TaxaJuros
from economics import START_DATE, END_DATE, get_moedas, get_selic, get_ipca, currencies, get_stocks
from utils import CODIGO_CORES, TICKERS

# st.image("assets/dash.jpg")
URL = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv"
df = pd.read_csv(URL)

with st.sidebar:
    st.image("assets/logo.jpg")
    scol1, scol2 = st.columns(2)
    with scol1:
        d1 = st.date_input("Data de começo", START_DATE)
    with scol2:
        d2 = st.date_input("Data fim", END_DATE)
    # Escolha da moeda
    moeda_sel = st.segmented_control(
        "Escolha a moeda:", currencies, default='USD'
    )
    compare_opts = st.multiselect(
        "Escolha os índices para comparação:",
        ["IPCA", "SELIC", "USD", "BOVESPA"],
        ["SELIC", "IPCA"],
    )
    print(f"Você selecionou começo: {d1} e Fim: {d2} | Moeda {moeda_sel}")

#  Solicitar informações de moedas pela biblioteca BCB
moedas_df = get_moedas(currencies, d1, d2)
selic, selic_hoje, selic_1a = get_selic(d1, d2)
ipca_data = get_ipca(d1, d2)
acoes = get_stocks(d1, d2)

# Container 1
with st.container():
    st.markdown(
        """
        <style>
        .header {
            background-color: #001E62; 
            color: white;
            padding: 10px;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    # Cria o header
    st.markdown(
        """
        <h1 style="color: white;" class='header'>Panorama Macroeconômico</h1>
        """,
        unsafe_allow_html=True
    )

    expc_atual = 1

    col1, col2, col3 = st.columns(3)
    with col1:
        taxa = selic_hoje / selic_1a
        if(taxa > 1):
            st.metric("SELIC", selic_hoje, f"{(selic_hoje-selic_1a)} %", "normal")
            # st.image("assets/up.png")
        else:
            st.metric("SELIC", selic_hoje, (selic_hoje-selic_1a), "normal")
            # st.image("assets/down.png")
    with col2:
        st.metric("IPCA", expc_atual, "-8%")
        #st.image("assets/down.png")
    with col3:
        st.metric("Dólar", "86%", "4%")
        #st.image("assets/dolar.png")

# Container 2
with st.container():
    st.header("Informações do Brasil")
    ccol1, ccol2 = st.columns(2)
    with ccol1:
        # Plota
        fig_selic = px.line(selic, y='selic', title='Taxa de Juros no Brasil (SELIC)')
        # Adicione rótulos de eixo
        fig_selic.update_layout(
            xaxis_title='Data Base',
            yaxis_title='Taxa de Juros - SELIC (%)'
        )
        st.plotly_chart(fig_selic)

    with ccol2:
        fig_ipca = px.line(ipca_data, y='IPCA_Media', title='Taxa da Expectativa do IPCA')
        st.plotly_chart(fig_ipca)

# Container 3
with st.container():
    st.header("Seleção de Moedas")
    fig = px.line(moedas_df, y=moeda_sel, title='Cotação da Moeda escolhida')
    st.plotly_chart(fig)

with st.container():
    fig_acoes = px.line(acoes, y='^BVSP', title='Cotação da Moeda escolhida')
    st.plotly_chart(fig_acoes)
    st.header("comparativo")
   