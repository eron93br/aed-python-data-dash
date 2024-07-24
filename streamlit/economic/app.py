import streamlit as st
import pandas as pd
from bcb import currency
import datetime
import plotly.express as px

st.title("Dashboard de Dados Econômicos - CESAR School 24.1")

st.markdown("Este dashboard tem como objetivo mostrar dados econômicos!")

with st.sidebar:
    sel_ano = st.selectbox(
        label="Selecione o ano de análise:",
        options=[2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
        index=0,
    )
    st.write("Você selecionou:", sel_ano)

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
    with st.container():
        # Realizar a cotação
        dolar = currency.get('USD', start=day[0], end=day[1])
        # Fazer gráfico da cotação
        fig = px.line(dolar, y='USD')
        # Plot!

        st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://static.streamlit.io/examples/cat.jpg")


    with col2:
        st.image("https://static.streamlit.io/examples/dog.jpg")