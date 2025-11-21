import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from streamlit.components.v1 import iframe
import urllib.request
import urllib.error

st.set_page_config(page_title="Rack And POD Dashboard", layout="centered")

# Sidebar navigation: only Home, Random Walk, Rack And POD analytics
st.sidebar.title("Dashboard")
selection = st.sidebar.radio(
    "Choose an app",
    ("Home", "Random Walk", "Rack And POD analytics")
)

st.title("Rack And POD Dashboard")
st.markdown("A compact dashboard. Use the sidebar to navigate between Home, Random Walk, and Rack And POD analytics (LAN).")

EXTERNAL_URL = "http://iedubm0app02:8501/"

def try_server_fetch(url, timeout=5):
    """Attempt to fetch the URL from the server running this app and return status, headers or error."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Streamlit-Diagnostic/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            headers = dict(resp.getheaders())
            body = resp.read(1024)
            return {"ok": True, "status": resp.status, "headers": headers, "body_sample": body[:1024].decode(errors="replace")}
    except urllib.error.HTTPError as e:
        return {"ok": False, "error": f"HTTPError {e.code}: {e.reason}", "headers": dict(e.headers) if e.headers else {}}
    except urllib.error.URLError as e:
        return {"ok": False, "error": f"URLError: {e.reason}"}
    except Exception as e:
        return {"ok": False, "error": f"Exception: {e}"}

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

    st.info("Experimental: try embedding below. Embedding may be blocked by headers (X-Frame-Options/CSP) or by network/name resolution.")
    if st.checkbox("Try to embed the Rack And POD analytics app here (experimental)"):
        try:
            iframe(EXTERNAL_URL, height=800)
            st.success("Iframe inserted — if blank, open DevTools (F12) -> Console for errors (e.g., Mixed Content, X-Frame-Options).")
        except Exception as e:
            st.error("Embedding failed on the server side. Use the link above.")
            st.write(e)

    st.subheader("Server-side reachability test")
    st.write("This attempts to fetch the external URL from the machine running this dashboard and prints status/headers.")
    if st.button("Run server-side check"):
        result = try_server_fetch(EXTERNAL_URL)
        if result.get("ok"):
            st.success(f"Server can reach the URL — HTTP {result['status']}")
            st.write("Response headers (from server):")
            st.json(result["headers"])
            st.write("First 1KB of response body (sample):")
            st.code(result["body_sample"][:1000])
        else:
            st.error("Server-side fetch failed")
            st.write(result.get("error"))
            if "headers" in result and result["headers"]:
                st.write("Response headers:")
                st.json(result["headers"])

    st.markdown(
        """
        Quick troubleshooting checklist:
        1) From a LAN client: open http://iedubm0app02:8501/ directly — does it load?
        2) If it loads, with the dashboard open on that client: open DevTools (F12) -> Console, tick the embed checkbox, and paste any errors you see here.
        3) From a LAN machine, run these in a terminal and paste outputs here:
           - curl -I http://iedubm0app02:8501/
           - curl -v http://iedubm0app02:8501/
           Look for headers: X-Frame-Options, Content-Security-Policy (frame-ancestors)
        4) If X-Frame-Options: DENY or SAMEORIGIN or CSP frame-ancestors prevents framing, change the Rack & POD server config (examples below).
        5) If name resolution fails, try the IP: http://<IP-of-iedubm0app02>:8501/
        """
    )

# Render selection
if selection == "Home":
    show_home()
elif selection == "Random Walk":
    show_random_walk()
elif selection == "Rack And POD analytics":
    show_rack_pod()
else:
    st.write("Select an app from the sidebar.")
