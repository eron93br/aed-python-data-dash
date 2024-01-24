import streamlit as st
import pandas as pd
import base64

import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as po
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import matplotlib.pyplot as plt
import plotly.express as px
import random
import plotly.figure_factory as ff

with st.container():
    st.write("Meu container 1")
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Pag. 1", "Pag. 2", "Pag. 3", "Pag. 4", "Pag. 5", "Pag. 6"])

    with tab1:
        st.header("A cat")
        st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

    with tab2:
        st.header("A dog")
        st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

    with tab3:
        st.header("An owl")
        st.image("https://static.streamlit.io/examples/owl.jpg", width=200)

    with tab4:
        st.header("A cat")
        st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

    with tab5:
        st.header("A dog")
        st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

    with tab6:
        st.header("An owl")
        st.image("https://static.streamlit.io/examples/owl.jpg", width=200)