import streamlit as st
import pandas as pd
# import plotly express!
import plotly.express as px
from PIL import Image
from io import BytesIO
import requests
from bs4 import BeautifulSoup
import urllib

def get_wikipedia_image_link(page_title):
    # Construct the URL of the Wikipedia page
    url = f"{page_title}"

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the infobox image element
    infobox_image = soup.find("table", class_="infobox").find("img")

    # Extract the source attribute (image link) from the image element
    image_link = infobox_image["src"]
    image_link = image_link[2:]
    result = 'https://' + image_link
    return result

# 1 - Carregar o dataset
df = pd.read_csv('gols.csv')
TIMES = df.clube.unique()
time_dict = {string: len(string) for string in TIMES}
time_dict['Fluminense']= 'https://pt.wikipedia.org/wiki/Fluminense_Football_Club'
time_dict['Internacional'] = 'https://pt.wikipedia.org/wiki/Sport_Club_Internacional'
time_dict['Sao Paulo'] = 'https://pt.wikipedia.org/wiki/S%C3%A3o_Paulo_Futebol_Clube'
time_dict['Cruzeiro'] = 'https://pt.wikipedia.org/wiki/Cruzeiro_Esporte_Clube'
time_dict['Palmeiras'] = 'https://pt.wikipedia.org/wiki/Sociedade_Esportiva_Palmeiras'
time_dict['Santos'] = 'https://pt.wikipedia.org/wiki/Santos_Futebol_Clube'
time_dict['Bahia'] = 'https://pt.wikipedia.org/wiki/Esporte_Clube_Bahia'
time_dict['Sport'] = 'https://pt.wikipedia.org/wiki/Sport_Club_do_Recife'
time_dict['Athletico-PR'] = 'https://pt.wikipedia.org/wiki/Club_Athletico_Paranaense'
time_dict['Criciuma'] = 'https://pt.wikipedia.org/wiki/Crici%C3%BAma_Esporte_Clube'
time_dict['Botafogo-RJ'] = 'https://pt.wikipedia.org/wiki/Botafogo_de_Futebol_e_Regatas'
time_dict['Vitoria'] = 'https://pt.wikipedia.org/wiki/Esporte_Clube_Vit%C3%B3ria'
time_dict['Corinthians'] = 'https://pt.wikipedia.org/wiki/Sport_Club_Corinthians_Paulista'
time_dict['Goias'] = 'https://pt.wikipedia.org/wiki/Goi%C3%A1s_Esporte_Clube'
time_dict['Gremio'] = 'https://pt.wikipedia.org/wiki/Gr%C3%AAmio_Foot-Ball_Porto_Alegrense'
time_dict['Atletico-MG'] = 'https://pt.wikipedia.org/wiki/Clube_Atl%C3%A9tico_Mineiro'
time_dict['Chapecoense'] = 'https://pt.wikipedia.org/wiki/Associa%C3%A7%C3%A3o_Chapecoense_de_Futebol'
time_dict['Coritiba'] = 'https://pt.wikipedia.org/wiki/Coritiba_Foot_Ball_Club'
time_dict['Flamengo'] = 'https://pt.wikipedia.org/wiki/Clube_de_Regatas_do_Flamengo'
time_dict['Figueirense'] = 'https://pt.wikipedia.org/wiki/Figueirense_Futebol_Clube'
time_dict['Ponte Preta'] = 'https://pt.wikipedia.org/wiki/Associa%C3%A7%C3%A3o_Atl%C3%A9tica_Ponte_Preta'
time_dict['Avai'] = 'https://pt.wikipedia.org/wiki/Ava%C3%AD_Futebol_Clube'
time_dict['Vasco'] = 'https://pt.wikipedia.org/wiki/Club_de_Regatas_Vasco_da_Gama'
time_dict['Joinville'] = 'https://pt.wikipedia.org/wiki/Joinville_Esporte_Clube'
time_dict['Santa Cruz'] = 'https://pt.wikipedia.org/wiki/Santa_Cruz_Futebol_Clube'
time_dict['America-MG'] = 'https://pt.wikipedia.org/wiki/Am%C3%A9rica_Futebol_Clube_(Belo_Horizonte)'
time_dict['Atletico-GO'] = 'https://pt.wikipedia.org/wiki/Atl%C3%A9tico_Clube_Goianiense'
time_dict['Parana'] = 'https://pt.wikipedia.org/wiki/Paran%C3%A1_Clube'
time_dict['Ceara'] = 'https://pt.wikipedia.org/wiki/Cear%C3%A1_Sporting_Club'
time_dict['Fortaleza'] = 'https://pt.wikipedia.org/wiki/Fortaleza_Esporte_Clube'
time_dict['CSA'] = 'https://pt.wikipedia.org/wiki/Centro_Sportivo_Alagoano'
time_dict['Bragantino'] = 'https://pt.wikipedia.org/wiki/Red_Bull_Bragantino'
time_dict['Cuiaba'] = 'https://pt.wikipedia.org/wiki/Cuiab%C3%A1_Esporte_Clube'
time_dict['Juventude'] = 'https://pt.wikipedia.org/wiki/Esporte_Clube_Juventude'

#
response = requests.get('https://upload.wikimedia.org/wikipedia/pt/8/82/Brasileiro_Serie_A_2020.png')
image_br = Image.open(BytesIO(response.content))

# 2 - Definição de interface do dashboard
st.set_page_config(page_title="Dash Brasileirão")

header = st.container()
msidebar = st.sidebar
box1 = st.container()
box2 = st.container()

# Descrição dos elementos de interface

with header:
    # elemento de titulo
    st.title("Dashboard Brasileirão com Streamlit")
    hcol1, hcol2, hcol3 = st.columns(3)
    with hcol1:
        st.write("")
    with hcol2:
        st.image(image_br, use_column_width=True)
    with hcol3:
        st.write("")

with msidebar:
    # editar a sidebar
    option_time = st.selectbox('Selecione o time:', (df.clube.unique()))
    st.title(" ")
    rodada = st.slider('Selecione as rodadas de interesse:', 1, 38, (1, 38))
    # processo de mostrar a figura do time
    image_url = get_wikipedia_image_link(time_dict[option_time])
    response = requests.get(image_url)
    #
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("")
    with col2:
        st.image(Image.open(BytesIO(response.content)))
    with col3:
        st.write("")
    print(f"Você selecionou o time {option_time}")
    print(rodada)

with box1:
    #st.header("Goleadores")
    # colocar aqui o input
    #n_slider = int(st.text_input('Defina quantas linhas do dataset você deseja atualizar:', 5))
    st.header('Artilheiros do time no Campeonato')
    # st.write(df.head(n_slider))
    dff = df.loc[df['clube'] == option_time]
    fig1 = px.bar(dff, x="atleta")
    st.plotly_chart(fig1, use_container_width=True)

with box2:
    st.header('Tipo de gol')
    dfs = dff.loc[(dff['rodata']>= rodada[0]) & (dff['rodata'] <= rodada[1])]
    fig2 = px.bar(dfs, x="tipo_de_gol")
    st.plotly_chart(fig2, use_container_width=True)