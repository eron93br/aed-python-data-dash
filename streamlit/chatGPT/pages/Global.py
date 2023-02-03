import streamlit as st
import streamlit.components.v1 as components

# layout second pag
header2 = st.container()

with header2:
    st.title("Estatísticas Mundiais 🌎")
    st.write("Interesse ao longo do tempo")
    components.html(
        """
        <script type="text/javascript" src="https://ssl.gstatic.com/trends_nrtr/3197_RC04/embed_loader.js"></script> <script type="text/javascript"> trends.embed.renderExploreWidget("TIMESERIES", {"comparisonItem":[{"keyword":"chatGPT","geo":"","time":"today 12-m"}],"category":0,"property":""}, {"exploreQuery":"q=chatGPT&date=today 12-m","guestPath":"https://trends.google.com:443/trends/embed/"}); </script>
        """,
        height=500,
    )
    components.html(
        """
        <script type="text/javascript" src="https://ssl.gstatic.com/trends_nrtr/3197_RC04/embed_loader.js"></script> <script type="text/javascript"> trends.embed.renderExploreWidget("GEO_MAP", {"comparisonItem":[{"keyword":"chatGPT","geo":"","time":"today 12-m"}],"category":0,"property":""}, {"exploreQuery":"q=chatGPT&date=today 12-m","guestPath":"https://trends.google.com:443/trends/embed/"}); </script>
        """,
        height=500,
    )
    st.write("Fonte: https://trends.google.com/trends/explore?q=chatGPT")
