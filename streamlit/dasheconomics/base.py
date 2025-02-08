
# Este é o arquivo de base para estruturar o dashboard macroeconômico

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px

# st.image("assets/dash.jpg")
URL = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv"
df = pd.read_csv(URL)

with st.sidebar:
    st.write("ESTÉ É O DASHBOARD DO SUCESSO!")
    st.image("assets/images.png")

# Container 1
with st.container():
    st.write("CONTAINER 1")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("métrica1")
        st.image("https://cdn-icons-png.flaticon.com/512/10011/10011320.png")
    with col2:
        st.write("métrica2")
        st.image("https://cdn-icons-png.flaticon.com/512/10011/10011320.png")
    with col3:
        st.write("métrica1")
        st.image("https://cdn-icons-png.flaticon.com/512/10011/10011320.png")

# Container 2
with st.container():
    st.write("CONTAINER 1")
    ccol1, ccol2 = st.columns(2)
    with ccol1:
        st.write("FIGURA 1")
        chart_data = df["size"]
        st.bar_chart(chart_data)
    with ccol2:
        st.write("FIGURA 2")
        chart_data = df["size"]
        st.bar_chart(chart_data)

# Container 3
with st.container():
    st.write("CONTAINER 1")
    chart_data = df["sex"]
    st.bar_chart(chart_data)