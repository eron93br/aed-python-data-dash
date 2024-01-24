import streamlit as st
import pandas as pd
import base64

#
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as po
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import matplotlib.pyplot as plt
import plotly.express as px
import random
import plotly.figure_factory as ff
from utils import (
    N_SELECTED,
    CESAR_LOGO,
    APP_TITLE,
    SALAD,
    DRINKS,
    PAGE_TITLE,
    MC_LOGO,
    LOGO,
    BREAKFAST_LOGO,
    BURGERS,
    CHICKEN,
    SIDES,
    BR_FLAG,
    US_FLAG,
    MC_CAFE,
    TREATS,
)

# Aqui onde configuramos o título da página e o logo que aparecerá no Browser!!!
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=LOGO,
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title(APP_TITLE)

## Data Operations ##
DATA_PATH = "data/menu.csv"
df = pd.read_csv(DATA_PATH)
## --------------- ##

## GLOBAL ##
selected_options = []

def png_to_base64(file_path):
    with open(file_path, "rb") as img_file:
        base64_encoded = base64.b64encode(img_file.read()).decode("utf-8")
        return base64_encoded


## vars
LISTA_C = [
    "Our Menu",
    "Download App",
    "MyMcDonalds Rewards",
    "Exclusive Deals",
    "About Our Food",
    "Locate",
    "Gift Cards",
]

# COLUNAS Imgs
mcol1, mcol2, mcol3, mcol4 = st.columns(4)
# COLUNAS flags

with st.sidebar:
    st.image(LOGO)
    #st.write("Visit our Website")
    st.markdown("<h3 style='text-align: center;'>Visit our Website</h3>", unsafe_allow_html=True)
    flc1, flc2, flc3, flc4= st.columns(4)
    with flc2:
        # FIXME: note que se usarmos a opção com st.image, não ficará centralizado!
        #        assim, escolho usar a opção de colocar imagens com Markdown.
        #st.image(BR_FLAG, width=30)
        mc_site_br = "https://www.mcdonalds.com.br/"  # Replace with your desired URL
        mc_site_us = "https://www.mcdonalds.com/us/en-us.html"

        st.markdown(
            f'<div style="display: flex; flex-direction: column; align-items: center;">'
            f'<a href="{mc_site_br}" target="_blank" onclick="open_link(\'{mc_site_br}\')"> '
            f'<img src="{BR_FLAG}" style="width: 30px;"></a>'
            f'</div>',
            unsafe_allow_html=True
        )
    with flc3:
        # FIXME: note que se usarmos a opção com st.image, não ficará centralizado!
        #        assim, escolho usar a opção de colocar imagens com Markdown.
        #st.image(US_FLAG, width=30)
        st.markdown(
            f'<div style="display: flex; flex-direction: column; align-items: center;">'
            f'<a href="{mc_site_us}" target="_blank" onclick="open_link(\'{mc_site_us}\')"> '
            f'<img src="{US_FLAG}" style="width: 30px;"></a>'
            f'</div>',
            unsafe_allow_html=True
        )

with st.container():
    with mcol1:
        st.image(BURGERS)
        sel_burgers = st.toggle("Select Burgers")
        st.image(TREATS)
        sel_desserts  = st.toggle("Select Desserts")

    with mcol2:
        st.image(CHICKEN)
        sel_chicken = st.toggle("Select Chicken")
        st.image(DRINKS)
        sel_drinks = st.toggle("Select Drinks")

    with mcol3:
        st.image(SIDES)
        sel_sides = st.toggle("Select Sides")
        st.image(MC_CAFE)
        sel_mccafe  = st.toggle("Select McCafe Coffes")

    with mcol4:
        st.image(BREAKFAST_LOGO)
        sel_break = st.toggle("Select Breakfast")
        st.image(SALAD)
        sel_salads = st.toggle("Select Salads")

    # Debug na tela das opções selecionadas, lembrando que selected_otions é um var global!
    selected_options.append("Beef & Pork" if sel_burgers else "")
    selected_options.append("Smoothies & Shakes" if sel_desserts else "")
    selected_options.append("Chicken & Fish" if sel_chicken else "")
    selected_options.append("Beverages" if sel_drinks else "")
    selected_options.append("Snacks & Sides" if sel_sides else "")
    selected_options.append("Coffee & Tea" if sel_mccafe else "")
    selected_options.append("Breakfast" if sel_break else "")
    selected_options.append("Salads" if sel_salads else "")

    # Filter out empty strings (options not selected)
    selected_options = [option for option in selected_options if option]

    print(f"Selected options: {', '.join(selected_options)}")

with st.container():
    st.write("------------------------------------------------")
    scol1, scol2 = st.columns(2)

    with scol1:
        tc1, _ = st.columns(2)
        with tc1:
            option = st.selectbox(
                'Selecione o parâmetro de análise desejado:',
                df.columns)
            # FIltrar daframe!!!
            dfs = df[df['Category'].isin(selected_options)]
        # Plot da primeira visualização
        fig = px.bar(
            dfs,
            x="Item",
            y=option,
            text=f"{option}",
            title=f"{option} in Different Foods",
        )
        st.plotly_chart(fig, use_container_width=True)



    with scol2:
            # Plot da primeira visualização
            fig = px.bar(
                dfs,
                x="Item",
                y=option,
                text=f"{option}",
                title=f"{option} in Different Foods",
            )
            st.plotly_chart(fig, use_container_width=True)

    st.write("------------------------------------------------")
    # st.write(df.head(5))

    # option = st.selectbox(
    #     'Selecione o parâmetro de análise desejado:',
    #     df.columns)
    
    # print(f" A opção desejada para plot foi {option}")

# with st.container():
#     # Variáveis auxiliares para construção do dashboard
#     lista_itens = df["Category"].unique()
#     col1, col2, col3 = st.columns(3)

#     col1.metric("Temperature", "70 °F", "1.2 °F")
#     col2.metric("Wind", "9 mph", "-8%")
#     col3.metric("Humidity", "86%", "4%")
#     # # SELECTBOX dos itens
#     # option_categoria = "Breakfast"
#     # print(f"Você selecionou {option_categoria}")

#     data_df = pd.DataFrame(
#         {
#             "category": [
#                 "📊 Data Exploration",
#                 "📈 Data Visualization",
#                 "📊 Data Exploration",
#             ],
#         }
#     )

#     st.data_editor(
#         data_df,
#         column_config={
#             "category": st.column_config.SelectboxColumn(
#                 "Choose your Visualization",
#                 help="The category of the app",
#                 width="medium",
#                 options=[
#                     "📊 Data Exploration",
#                     "📈 Data Visualization",
#                 ],
#                 required=True,
#             )
#         },
#         hide_index=True,
#     )

    # # Realizar operação de filtrar pela categoria desejada
    # dfs = df[df['Category'].isin(selected_options)]

    # st.write(dfs.head(N_SELECTED))

    # # Plot da primeira visualização
    # fig = px.bar(
    #     dfs,
    #     x="Item",
    #     y="Calories",
    #     text="Calories",
    #     title="Calories in Different Foods",
    # )

    # st.plotly_chart(fig, use_container_width=True)
