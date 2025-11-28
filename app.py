import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from streamlit.components.v1 import iframe

st.set_page_config(page_title="Rack And POD Dashboard", layout="centered")

# Sidebar navigation: only Home, Random Walk, Rack And POD analytics
st.sidebar.title("Dashboard")
selection = st.sidebar.radio(
    "Choose an app",
    ("Home", "link1", "Rack And POD analytics, ")
)

st.title("Rack And POD Dashboard")
st.markdown("A compact dashboard. Use the sidebar to navigate between Home, Random Walk, and Rack And POD analytics (LAN).")

EXTERNAL_URL = "http://iedubm0app02:8501/"

def show_home():
    st.header("Welcome")
    st.write("This dashboard provides quick navigation to the Rack And POD analytics app on the LAN and a small demo Random Walk app.")
    st.markdown(
        "- Click 'Rack And POD analytics' in the sidebar to open or embed the LAN analytics app.\n"
        "- Click 'Random Walk' for a demo chart."
    )

def show_random_walk():
    st.header("Random Walk")
    rows = st.slider("Number of points", 10, 2000, 200, step=10)
    seed = st.number_input("Random seed", min_value=0, value=42, step=1)
    cumulative = st.checkbox("Show cumulative sum", value=True)

    np.random.seed(int(seed))
    x = np.arange(rows)
    y = np.random.randn(rows)
    if cumulative:
        y = np.cumsum(y)
    df = pd.DataFrame({"x": x, "y": y})

    st.subheader("Line chart")
    chart = alt.Chart(df).mark_line().encode(x="x", y="y").interactive().properties(height=400)
    st.altair_chart(chart, use_container_width=True)

    if st.checkbox("Show data table"):
        st.dataframe(df)

def show_rack_pod():
    st.header("Rack And POD analytics (LAN)")
    st.write("If you are on the same LAN, use the link below to open the analytics app in a new tab.")
    st.markdown(
        f'<a href="{EXTERNAL_URL}" target="_blank" rel="noopener noreferrer">Open Rack And POD analytics (opens in new tab)</a>',
        unsafe_allow_html=True
    )

    st.info("Experimental: try embedding below. Embedding may be blocked by mixed-content or by the remote server's headers.")
    if st.checkbox("Try to embed the Rack And POD analytics app here (experimental)"):
        try:
            iframe(EXTERNAL_URL, height=800)
            st.success("Iframe inserted — if blank, check your browser console for Mixed Content or X-Frame-Options errors.")
        except Exception as e:
            st.error("Embedding failed on the server side. Use the link above.")
            st.write(e)

# Render selection
if selection == "Home":
    show_home()
elif selection == "Random Walk":
    show_random_walk()
elif selection == "Rack And POD analytics":
    show_rack_pod()
else:
    st.write("Select an app from the sidebar.")
