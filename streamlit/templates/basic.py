# 1 --- Importe as bibliotecas necessárias
import pandas as pd
import streamlit as st
import plotly.express as px

# 2 --- Pode ser inserido uma parte de CSS para estilizacao do grafico
st.markdown(
    f"""
<style>
    .reportview-container .main .block-container{{
        max-width: 90%;
        padding-top: 5rem;
        padding-right: 5rem;
        padding-left: 5rem;
        padding-bottom: 5rem;
    }}
    img{{
    	max-width:40%;
    	margin-bottom:40px;
    }}
</style>
""",
    unsafe_allow_html=True,
)

# 3 --- Construa aqui a estrutura do seu app streamlit
# Streamlit apps podem ser dividios em diferentes seções
# container -> seções horizontais
# columns -> seções verticais(pode ser criado dentro de um container)
# sidebar -> a vertical bar on the side of your app

header_container = st.container()
stats_container = st.container()
# Carregar dataset
data = pd.read_csv("assets/JC-202103-citibike-tripdata.csv")

# Você pode colocar fotos, imagens e conteudo dentro dos containers!
with header_container:
    # Exemplo de imagem teste
    st.image("assets/logo2.png")
    # alguns outros componentes
    st.title("bem legal esse dashboard não?")
    st.header("Olá, vc gostou do streamlit?")
    st.subheader("app template")
    st.write("este é um template do streamlit =)")

with stats_container:
    # 5 --- Editando um pouco os dados para exibição
    start_station_list = ["All"] + data["start station name"].unique().tolist()
    end_station_list = ["All"] + data["end station name"].unique().tolist()
    # 6 --- Adicionando widgets de inputs do usuário
    text_input = st.text_input("colete dados do usuário aqui", "Something")
    print(f"usuário digitou {text_input}")
    st.write("digite algo no dropdown menu")
    s_station = st.selectbox(
        "Que estação inicial vc gostaria de ver?",
        start_station_list,
        key="start_station",
    )

    # Exibe o que foi selecionado
    st.write("Estação selecionada: " + str(s_station))

    st.write("Exibição de acordo com selecionado")
    if s_station != "All":
        display_data = data[data["start station name"] == s_station]
    else:
        display_data = data.copy()

    # Exibir o dataset na tela
    # https://plotly.com/python/table/
    st.write(display_data)
    st.write("podemos colocar algumas diferentes seções dentro do container")
    multi_select = st.multiselect(
        "QUAL ESTAÇÃO INICIAL?",
        start_station_list,
        key="start_station",
        default=["Harborside", "Marin Light Rail"],
    )
    slider_input = st.slider(
        "Quão longa deve ser essa viagem?",
        int(data["tripduration"].min() / 3600),
        int(data["tripduration"].max() / 3600),
        25,
    )

    # 7 --- criação de colunas dentro do container
    bar_col, pie_col = st.columns(2)

    # preparing data to display on pie chart
    user_type = data["usertype"].value_counts().reset_index()
    user_type.columns = ["user type", "count"]

    # 8 --- Criação de gráficos do plotly express
    start_location = data["start station name"].value_counts()
    bar_col.subheader("Duração da viagem por estação")
    bar_col.bar_chart(start_location)
    # não esquece dos titulos =)
    pie_col.subheader("Quantos usuários estão inscritos?")
    fig = px.pie(user_type, values="count", names="user type", hover_name="user type")

    fig.update_layout(
        showlegend=False,
        width=300,
        height=400,
        margin=dict(l=1, r=1, b=1, t=1),
        font=dict(color="#383635", size=15),
    )

    # Para mais informações, visit: https://plotly.com/python/pie-charts/
    fig.update_traces(textposition="inside", textinfo="percent+label")

    # Depois da criação da figura, podemos exibir com
    pie_col.write(fig)
