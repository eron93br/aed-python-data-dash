import streamlit as st
import pandas as pd
from bcb import currency
import datetime
import plotly.express as px
from utils import fetch_btc_data

st.title("Dashboard de Dados Econômicos - CESAR School 24.1")

st.markdown("Este dashboard tem como objetivo mostrar dados econômicos!")

with st.sidebar:
    lista_moedas = []

    sel_ano = st.selectbox(
        label="Selecione o ano de análise:",
        options=[2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
        index=0,
    )
    st.write("Você selecionou:", sel_ano)

    # Checkbox de Moeda
    st.write("Selecione Moeda(s) para Análise")
    sel_usd = st.checkbox("USD Dolar", value=True)
    sel_eur = st.checkbox("Euro")
    sel_fsc = st.checkbox("CHG")
    
    if sel_usd:
        lista_moedas.append("USD")
    if sel_eur:
        lista_moedas.append("EUR")
    if sel_fsc:
        lista_moedas.append("CHF")
    print(f" As moedas selecionadas são: {lista_moedas}")

    jan_1 = datetime.date(sel_ano, 1, 1)
    dec_31 = datetime.date(sel_ano, 12, 31)

    # Seleciona as datas de interesse da cotação
    day = st.date_input(
        "Selecione as datas que você deseja verificar a cotação do dolar (USD):",
        (jan_1, datetime.date(sel_ano, 1, 7)),
        jan_1,
        dec_31,
        format="MM.DD.YYYY",
    )
    print(day)

# Container para visualização da cotação do dolar!
with st.container():
    # Gráfico da cotação da(s) moeda(s)
    with st.container():
        st.header(f"Cotação das Moedas selecionadas")
        moedas = currency.get(lista_moedas, start=day[0], end=day[1])
        # FIGURA 1 - Realizar a cotação das moedas
        # Fazer gráfico da cotação
        fig1 = px.line(moedas, y=lista_moedas)
        st.plotly_chart(fig1, use_container_width=True)
        
        # FIGURA 2 - Cotação do BTC
        st.header("Cotação do BTC")
        btc_data = fetch_btc_data()
        prices = btc_data['prices']
        btc_df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        btc_df['timestamp'] = pd.to_datetime(btc_df['timestamp'], unit='ms')
        fig2 = px.line(btc_df, y='price')
        st.plotly_chart(fig2, use_container_width=True)
