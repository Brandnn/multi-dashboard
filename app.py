import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from streamlit.components.v1 import iframe

st.set_page_config(page_title="Multi-App Dashboard", layout="centered")

# Dashboard sidebar navigation
st.sidebar.title("Dashboard")
selection = st.sidebar.radio(
    "Choose an app",
    ("Home", "Random Walk", "Sales Bars", "Data Table", "Scatter Explorer", "External App (LAN)")
)

st.title("Multi-App Dashboard")
st.markdown("A simple Streamlit dashboard with multiple small demo apps. Use the sidebar to navigate between apps.")

def show_home():
    st.header("Welcome")
    st.markdown(
        """
        This repository is a single Streamlit app that contains multiple small demo apps inside.
        Use the sidebar to switch between them:
        - Random Walk: a line chart demo
        - Sales Bars: an example bar chart
        - Data Table: interactive table with filters
        - Scatter Explorer: interactive scatter plot
        - External App (LAN): link/embed to an internal URL on your LAN
        """
    )
    st.info("This is a single deployable Streamlit app. All sub-apps are rendered inside this file.")

# ... (other app functions unchanged) ...
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

def show_sales_bars():
    st.header("Sales Bars")
    categories = st.multiselect("Choose categories", options=["A", "B", "C", "D"], default=["A", "B", "C", "D"])
    months = np.arange(1, 13)
    data = []
    rng = np.random.default_rng(123)
    for cat in categories:
        values = rng.integers(50, 300, size=len(months))
        for m, v in zip(months, values):
            data.append({"month": int(m), "category": cat, "sales": int(v)})
    df = pd.DataFrame(data)

    st.subheader("Monthly sales by category")
    bar = alt.Chart(df).mark_bar().encode(
        x=alt.X("month:O", title="Month"),
        y=alt.Y("sales:Q", title="Sales"),
        color="category:N",
        tooltip=["month", "category", "sales"]
    ).properties(height=400)
    st.altair_chart(bar, use_container_width=True)

    if st.checkbox("Show raw data"):
        st.dataframe(df)

def show_data_table():
    st.header("Interactive Data Table")
    n = st.slider("Rows", 10, 2000, 300)
    rng = np.random.default_rng(1)
    df = pd.DataFrame({
        "id": np.arange(1, n+1),
        "group": rng.choice(["alpha", "beta", "gamma"], size=n),
        "value": rng.normal(loc=100, scale=20, size=n).round(2)
    })
    group_filter = st.multiselect("Filter group", sorted(df["group"].unique()), default=sorted(df["group"].unique()))
    min_val, max_val = st.slider("Value range", float(df["value"].min()), float(df["value"].max()), (float(df["value"].min()), float(df["value"].max())))
    df_filtered = df[(df["group"].isin(group_filter)) & (df["value"].between(min_val, max_val))]
    st.write(f"{len(df_filtered)} rows matching filters")
    st.dataframe(df_filtered)

def show_scatter_explorer():
    st.header("Scatter Explorer")
    n = st.slider("Points", 100, 5000, 800)
    rng = np.random.default_rng(2025)
    df = pd.DataFrame({
        "x": rng.normal(size=n),
        "y": rng.normal(size=n),
        "size": rng.integers(10, 200, size=n),
        "category": rng.choice(["red", "green", "blue"], size=n)
    })

    st.subheader("Scatter plot with selection")
    scatter = alt.Chart(df).mark_circle().encode(
        x="x",
        y="y",
        size=alt.Size("size", scale=alt.Scale(range=[10, 500])),
        color="category",
        tooltip=["x", "y", "size", "category"]
    ).interactive().properties(height=500)
    st.altair_chart(scatter, use_container_width=True)

def show_external_app():
    st.header("External App (LAN)")
    external_url = "http://iedubm0app02:8501/"

    st.write("This is a link to an app on your LAN:")
    # Reliable link that opens in a new tab. Works for LAN users if their browser can resolve the host.
    st.markdown(
        f'<a href="{external_url}" target="_blank" rel="noopener noreferrer">Open external app (opens in new tab)</a>',
        unsafe_allow_html=True
    )

    st.info(
        "If you are viewing this dashboard from the same LAN and the target host allows embedding, you can try the experimental embed below. "
        "If the dashboard is served over HTTPS (for example, Streamlit Cloud), the browser will likely block embedding HTTP content (mixed content)."
    )

    if st.checkbox("Try to embed the external app here (experimental)"):
        st.write("Attempting to embed. If you see nothing or a browser error, embedding is blocked by the browser or by the remote server's headers (X-Frame-Options).")
        try:
            iframe(external_url, height=800)
        except Exception as e:
            st.warning("Embedding failed. Use the link above to open the app in a new tab.")
            st.write("Embed error:", e)

# Render selected app
if selection == "Home":
    show_home()
elif selection == "Random Walk":
    show_random_walk()
elif selection == "Sales Bars":
    show_sales_bars()
elif selection == "Data Table":
    show_data_table()
elif selection == "Scatter Explorer":
    show_scatter_explorer()
elif selection == "External App (LAN)":
    show_external_app()
else:
    st.write("Select an app from the sidebar.")
