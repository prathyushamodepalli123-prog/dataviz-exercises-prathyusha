import pandas as pd
import streamlit as st
from pathlib import Path

# -----------------------------------------------------------------------------
# Load data once and cache it
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():

    # Dataset should be in the repository root
    path = Path(__file__).parent / "airbnb_london.csv"

    # Debug information
    st.write("CSV Path:", path)
    st.write("CSV Exists:", path.exists())

    if not path.exists():
        st.error(f"CSV file not found: {path}")
        st.stop()

    df = pd.read_csv(path)

    # Remove extreme outliers
    p95 = df["price"].quantile(0.95)
    df = df[df["price"] <= p95].copy()

    return df, p95


# -----------------------------------------------------------------------------
# Initialise sidebar filters
# -----------------------------------------------------------------------------
def init_filters(df):

    defaults = {
        "flt_rooms": list(df["room_type"].unique()),
        "flt_hoods": sorted(df["neighbourhood"].unique()),
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if "flt_price" not in st.session_state:
        st.session_state["flt_price"] = (
            int(df["price"].min()),
            int(df["price"].max())
        )


# -----------------------------------------------------------------------------
# Sidebar filters
# -----------------------------------------------------------------------------
def sidebar_filters(df, p95):

    init_filters(df)

    with st.sidebar:

        st.header("🔎 Filters")

        st.multiselect(
            "Room type",
            options=sorted(df["room_type"].unique()),
            key="flt_rooms",
        )

        st.multiselect(
            "Neighbourhood",
            options=sorted(df["neighbourhood"].unique()),
            key="flt_hoods",
        )

        min_price = int(df["price"].min())
        max_price = int(df["price"].max())

        st.slider(
            "Price (£/night)",
            min_value=min_price,
            max_value=max_price,
            key="flt_price",
        )

        st.divider()

        st.caption(
            f"Prices capped at the 95th percentile (£{p95:.0f}) to remove extreme outliers."
        )

    filtered = df[
        (df["room_type"].isin(st.session_state["flt_rooms"]))
        & (df["neighbourhood"].isin(st.session_state["flt_hoods"]))
        & (df["price"].between(*st.session_state["flt_price"]))
    ]

    if filtered.empty:
        st.warning("No listings match the selected filters.")
        st.stop()

    return filtered
