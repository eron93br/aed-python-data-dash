import streamlit as st
import pandas as pd
from PIL import Image
import chatgpt
import csv
from csv import writer
from csv import DictWriter
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

header = st.container()
myquestions = st.container()

# Import images
back_img = Image.open("data/back_gpt.png")
# CSV
wdf_path = "data/questions.csv"
# word cloud configs
comment_words = ""
stopwords = set(STOPWORDS)

with header:
    st.title("chatGPT Dashboard")
    st.image(back_img)
    #
    len_d, sex_d = st.columns(2)
    #
    question_input = st.text_input(
        "Digite algo 👇",
    )

    # decide what to do
    if question_input == "":
        st.write("Por favor digite algo...")
    else:
        with open("data/questions.csv", "a") as f_object:
            thisdict = {
                "perguntas": question_input,
            }
            field_names = thisdict.keys()
            dictwriter_object = DictWriter(f_object, fieldnames=field_names)
            dictwriter_object.writerow(thisdict)
            f_object.close()
        question_ans = chatgpt.process_response(
            chatgpt.call_chatgpt_api(question_input)
        )
        if question_input:
            st.write("Resposta: ", question_ans)

with myquestions:
    st.set_option("deprecation.showPyplotGlobalUse", False)
    st.title("Word Cloud")
    list_wc = []
    # iterate through the csv file
    wdf = pd.read_csv(wdf_path, encoding="latin-1")
    for val in wdf.perguntas:
        # typecaste each val to string
        val = str(val)
        # split the value
        tokens = val.split()
        # Converts each token into lowercase
        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()
        comment_words += " ".join(tokens) + " "
    #
    fig, ax = plt.subplots(figsize=(12, 8))
    wordcloud = WordCloud(
        width=800,
        height=800,
        background_color="white",
        stopwords=stopwords,
        min_font_size=10,
    ).generate(comment_words)
    #
    plt.imshow(wordcloud)
    plt.axis("off")
    st.pyplot()
