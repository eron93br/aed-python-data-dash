import streamlit as st
import pandas as pd
from PIL import Image
import csv
from csv import writer
from csv import DictWriter
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from st_pages import Page, show_pages, add_page_title

# Passo 1 - importar imagens e dados .csv
back_img = Image.open("assets/call-report.png")
wp_img = Image.open("assets/back.png")
cs_img = Image.open("assets/marca_cesar_school.png")

# configurações gerais
st.set_page_config(page_title="Report Projeto Final")
show_pages(
    [
        Page("report.py", "Home", "🏠"),
        Page("pages/exploratoria.py", "Analise Exploratória", "📚"),
        Page("pages/explain.py", "Análise Explanatória", "🔥"),
    ]
)

markdown_text = """
- Joe Dohn
- Mr. Bean
- 007
"""


# Passo 2 - Configuração da Pagina principal
sidebar = st.sidebar
header = st.container()
box = st.container()

with sidebar:
    st.image(cs_img)
    st.title("Projeto Final - CESAR School")
    st.markdown(markdown_text)

with header:
    st.image(wp_img)
    st.title("Titulo do meu report")

with box:
    st.title("Template legal?")

