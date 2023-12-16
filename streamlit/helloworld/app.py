import streamlit as st
import pandas as pd

#
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as po
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import matplotlib.pyplot as plt
import plotly.express as px
import random
import plotly.figure_factory as ff

st.title("App Hello World")

st.markdown(
    """
    ### Comandos para mostrar conteúdo na página do dashboard do streamlit

    - st.write(): Display text, dataframes, charts, and more.
    - st.title(), st.header(), st.subheader(): Display titles and headers.
    - st.markdown(): Render Markdown text.
    - st.text(), st.code(): Display plain text or code.
    - st.image(): Display images.
    - st.audio(), st.video(): Display audio or video files.
    - st.file_uploader(), st.file_downloader(): Upload/download files.
"""
)

# TODO: se quiser mostrar um video, descomentar o link abaixo.
# youtube_url = 'https://www.youtube.com/watch?v=LIMXarK87V8&ab_channel=MaaxcamAoVivo'  # Replace with your YouTube video URL
# st.video(youtube_url)

# Mostrar imagem do HelloWorld
st.image(
    "https://res.cloudinary.com/practicaldev/image/fetch/s--1YFE_lec--/c_imagga_scale,f_auto,fl_progressive,h_420,q_auto,w_1000/https://dev-to-uploads.s3.amazonaws.com/i/z6pkbof42d5ljfxtox3p.png"
)

DATA_PATH = "data/menu.csv"

df = pd.read_csv(DATA_PATH)

# Variáveis auxiliares para construção do dashboard
lista_itens = df["Category"].unique()

# SELECTBOX dos itens
option_categoria = st.selectbox(
    "Escolha a seleção da categoria de produtos:", lista_itens
)
print(f"Você selecionou {option_categoria}")

# Realizar operação de filtrar pela categoria desejada
dfs = df[df["Category"] == option_categoria]

st.write(dfs.head(5))

# Plot da primeira visualização
fig = px.bar(
    dfs, x="Item", y="Calories", text="Calories", title="Calories in Different Foods"
)

# data_canada = px.data.gapminder().query("country == 'Canada'")
# fig = px.bar(data_canada, x='year', y='pop')
# fig.show()

# Plot!
st.plotly_chart(fig, use_container_width=True)
