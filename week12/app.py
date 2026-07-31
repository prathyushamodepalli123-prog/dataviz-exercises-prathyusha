"""
Lecture 12 Exercise — Extend the Dashboard with a Third Page
=============================================================
Run with: streamlit run app.py
"""

import streamlit as st

# Page config
st.set_page_config(
    page_title="London Airbnb Analytics",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Navigation
pg = st.navigation([
    st.Page(
        "pages/01_market.py",
        title="What does a night in London cost?",
        icon="🏠"
    ),
    st.Page(
        "pages/02_drilldown.py",
        title="Which neighbourhoods drive the premium?",
        icon="📍"
    ),
    st.Page(
        "pages/03_demand.py",
        title="Where is guest demand strongest?",
        icon="📈"
    ),
])

# Run selected page
pg.run()
