import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px

# 1 - Carregar dataset e imagens ----
df = pd.read_csv("assets/pokemon.csv")
N_POK = len(df)
back_img = Image.open("assets/capa.jpg")

# 2 - config geral
st.set_page_config(page_title="Dask Pokemon")
# Estruturação da página do dashboard
header = st.container()
dataset = st.container()
explorer = st.container()

# Descrever container header
with header:
    st.title("Pokemon Dashboard")
    st.image(back_img)
    st.markdown(
        "Pokemons são criaturas fictícias do universo Pokemon. Eles existem em todas as formas e tamanhos, e todos têm habilidades diferentes, como ataques de fogo, ataques elétricos e ataques de gelo. Os jogadores coletam e treinam essas criaturas para usá-las em batalhas contra outros treinadores. O objetivo é coletar o maior número possível de Pokémons e torná-los os mais poderosos possível."
    )

with dataset:
    st.header("Conheça seus pokemons:")
    poke_len = st.slider(
        "Determine quantos pokemons você vai listar:", 1, 5, (1, N_POK)
    )
    st.dataframe(df.iloc[poke_len[0] : poke_len[1], :])
    st.write(f"Você selecionou do Pokemon #{poke_len[0]} até o POkemon #{poke_len[1]}!")

with explorer:
    st.header("Tipos por Geração de Pokemon")
    # 1- Rotina da Primeira Figura
    # sel_generation = st.number_input('Digite o número da geração: ')
    sel_generation = st.selectbox("Qual a geração para o plot?", (1, 2, 3, 4, 5, 6))
    df2 = df.loc[df.Generation == sel_generation]
    pok2 = df2.groupby(["Type 1"]).count()
    pok2.reset_index()
    pok2.reset_index(inplace=True)
    # Definição da Primeira figura
    fig = px.bar(pok2, x="Type 1", y="Total", hover_data=["Type 1"], barmode="stack")
    # exibe figura no dashboard!
    st.plotly_chart(fig, use_container_width=True)
