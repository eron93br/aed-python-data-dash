import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as po
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import matplotlib.pyplot as plt
import plotly.express as px
import random
import plotly.figure_factory as ff
from utils import LOGO, BIG_MAC, Q_DELUXE, XBG
import base64
from pathlib import Path

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded


st.set_page_config(
    page_title="Burgers",
    page_icon=LOGO,
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Burgers")
col1, col2, col3 = st.columns(3)

header_html = "<img src='data:image/png;base64,{}' class='img-fluid' style='width: 150px; align-items: center;'>".format(img_to_bytes(BIG_MAC))

with col1:
    st.write("Column 1")
    st.markdown(header_html, unsafe_allow_html=True)
    st.markdown(
        f'<div style="display: flex; flex-direction: column; align-items: center;">'
        f'<img src="{BIG_MAC}" style="width: 150px;">'
        f'<img src="{Q_DELUXE}" style="width: 150px;">'
        f'<img src="{XBG}" style="width: 150px;">'
        f'</div>',
        unsafe_allow_html=True
    )

with col2:
    st.write("Column 2")
    st.markdown(
        f'<div style="display: flex; flex-direction: column; align-items: center;">'
        f'<img src="{BIG_MAC}" style="width: 150px;">'
        f'<img src="{Q_DELUXE}" style="width: 150px;">'
        f'<img src="{XBG}" style="width: 150px;">'
        f'</div>',
        unsafe_allow_html=True
    )

with col3:
    st.write("Column 3")
    st.markdown(
        f'<div style="display: flex; flex-direction: column; align-items: center;">'
        f'<img src="{BIG_MAC}" style="width: 150px;">'
        f'<img src="{Q_DELUXE}" style="width: 150px;">'
        f'<img src="{XBG}" style="width: 150px;">'
        f'</div>',
        unsafe_allow_html=True
    )