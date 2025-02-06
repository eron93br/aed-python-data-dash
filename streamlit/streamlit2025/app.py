import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

st.title("Dashboard 2025")
st.write("Dashboard da Turma 2024.2 - AD")
_, col2, _ = st.columns(3)

with col2:
    st.image("assets/images.png")

# st.image("assets/dash.jpg")
URL = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv"

# Header 1
st.header("Conteúdo do DataFrame")

df = pd.read_csv(URL)

st.write(df.head(5))


# primeira visualização com streamlit
st.header("Visualização #1")
chart_data = df["size"]
st.bar_chart(chart_data)

# segunda visualização com PLotly express
st.header("Visualização #2 - Plotly")
fig1 = px.bar(df, y="size")
st.plotly_chart(fig1, use_container_width=True)

# elemento widget
st.header("Botão do usuário")

left, middle, right, right2 = st.columns(4)

if left.button("Plain button", use_container_width=True):
    left.markdown("You clicked the plain button.")
if middle.button("Emoji button", icon="😃", use_container_width=True):
    middle.markdown("You clicked the emoji button.")
if right.button("Material button", icon=":material/mood:", use_container_width=True):
    right.markdown("You clicked the Material button.")
if right2.button("BOtão de Eron", icon=":material/mood:", use_container_width=True):
    right2.markdown("Ele está explicando na aula")
