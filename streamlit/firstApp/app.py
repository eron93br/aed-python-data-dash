import streamlit as st
import pandas as pd
from PIL import Image
import seaborn as sns
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

# Rotina de importacao das bibliotecas que serao usadas no nosso app

# Import dataset
c_data = pd.read_csv("data/WA_Fn-UseC_-Telco-Customer-Churn.csv")
df = c_data.copy()
# Clean dataset
df["TotalCharges"] = (
    c_data["TotalCharges"].apply(lambda x: pd.to_numeric(x, errors="coerce")).dropna()
)
# colunas para filtro
cfilters1 = [
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "Churn",
]
cfilters2 = [
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
    "Churn",
]

# Configuracao geral
st.set_page_config(
    page_title="Churn Analysis",
)

# Estrutura do app Streamlit
header = st.container()
dataset = st.container()
features = st.container()
model_training = st.container()

back_img = Image.open("data/back_churn.png")

# Container com o Header do nosso app do streamlit (titulo)
with header:
    st.title("Churn Rate Dataset Analysis")
    st.image(back_img)
    st.text("Este primeiro app tem como exemplo testar inputs e basic funtions")
    len_d, sex_d = st.columns(2)

with dataset:
    st.title("Data Exploring")
    len_d = st.slider("Quantos dados voce quer mostrar?", 5, 25, 5)
    # Objetivo de Debug para um widget de input!
    print(f"Selecionado {len_d} instancias")
    st.dataframe(c_data.head(len_d))

with features:
    st.title("Exploratory Analysis")
    col1, col2 = st.columns([1, 1])
    insider = st.container()
    # input de sexto
    with insider:
        gtype = st.radio(
            "Selecione um tipo:",
            ("gender", "SeniorCitizen", "Partner", "Dependents"),
            horizontal=True,
        )
        print(f"Tipo Selecionado {gtype}")
    # rotina de criacao da figura
    # fig = px.bar(df, x=str(gtype), y="count", color=str(gtype), title=f"Churn count by {gtype}")
    fig = px.bar(df, x=gtype, color="Churn", title=f"Exploratory analysis by {gtype}")
    st.plotly_chart(fig, use_container_width=True)


with model_training:
    # Operacao de filtro do dataframe para criar matriz de correlacao
    st.title("Correlação dos Parâmetros ")
    cdf1 = df.filter(cfilters1, axis=1)
    cdf2 = df.filter(cfilters2, axis=1)
    for col in cfilters1:
        c1 = preprocessing.LabelEncoder()
        c1.fit(cdf1[col])
        cdf1[col] = c1.transform(cdf1[col])

    for col in cfilters2:
        c2 = preprocessing.LabelEncoder()
        c2.fit(cdf2[col])
        cdf2[col] = c2.transform(cdf2[col])
    # CorrMatrix 1
    corrMatrix1 = cdf1.corr()
    mask1 = np.triu(np.ones_like(corrMatrix1, dtype=bool))
    # create image from seaborn
    plt.figure(figsize=(20, 4))
    fig2, ax = plt.subplots()
    ax = sns.heatmap(corrMatrix1, mask=mask1, annot=True, cmap="Blues").set(
        title="Relacionados a Internet"
    )
    # CorrMatrix 2
    corrMatrix2 = cdf2.corr()
    mask2 = np.triu(np.ones_like(corrMatrix2, dtype=bool))
    # create image from seaborn
    plt.figure(figsize=(20, 4))
    fig3, ax1 = plt.subplots()
    ax1 = sns.heatmap(corrMatrix2, mask=mask2, annot=True, cmap="Blues").set(
        title="Relacionados a TV"
    )
    st.pyplot(fig2)
    st.pyplot(fig3)
