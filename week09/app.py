import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="World Happiness Dashboard",
    page_icon="🌍",
    layout="wide"
)

# -----------------------------
# Load Data
# -----------------------------
path = Path(__file__).parent / "world_happiness_2023.csv"
df = pd.read_csv(path)

df.columns = [
    "Country",
    "Region",
    "Score",
    "GDP",
    "Social_Support",
    "Life_Expectancy",
    "Freedom",
    "Generosity",
    "Corruption"
]

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.header("Filters")

    regions = ["All"] + sorted(df["Region"].unique().tolist())

    selected_region = st.selectbox(
        "Region",
        regions
    )

    top_n = st.slider(
        "Show Top N Countries",
        min_value=5,
        max_value=30,
        value=15
    )

# -----------------------------
# Filter Data
# -----------------------------
if selected_region == "All":
    filtered = df
else:
    filtered = df[df["Region"] == selected_region]

top = filtered.nlargest(top_n, "Score").sort_values("Score")

# -----------------------------
# Title
# -----------------------------
st.title("🌍 World Happiness Dashboard")
st.caption("Source: World Happiness Report 2023")

# -----------------------------
# KPI Row
# -----------------------------
k1, k2, k3 = st.columns(3)

k1.metric(
    "Countries",
    len(filtered)
)

k2.metric(
    "Average Happiness",
    f"{filtered['Score'].mean():.2f}",
    f"{filtered['Score'].mean()-df['Score'].mean():+.2f} vs Global"
)

k3.metric(
    "Happiest Country",
    filtered.loc[filtered["Score"].idxmax(), "Country"],
    f"{filtered['Score'].max():.2f}"
)

st.divider()

# -----------------------------
# Charts
# -----------------------------
left, right = st.columns(2)

with left:

    st.subheader("Top Happiness Rankings")

    fig1 = px.bar(
        top,
        x="Score",
        y="Country",
        orientation="h",
        color="Score",
        color_continuous_scale="Blues",
        labels={
            "Score": "Happiness Score",
            "Country": ""
        }
    )

    fig1.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        coloraxis_showscale=False
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

with right:

    st.subheader("GDP vs Happiness")

    fig2 = px.scatter(
        filtered,
        x="GDP",
        y="Score",
        hover_name="Country",
        color_discrete_sequence=["#2E75B6"]
    )

    fig2.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# -----------------------------
# Factor Breakdown
# -----------------------------
st.subheader("Top 10 Countries - Factor Breakdown")

factors = [
    "GDP",
    "Social_Support",
    "Life_Expectancy",
    "Freedom"
]

top10 = filtered.nlargest(10, "Score")

fig3 = px.bar(
    top10.melt(
        id_vars="Country",
        value_vars=factors
    ),
    x="value",
    y="Country",
    color="variable",
    orientation="h",
    barmode="stack",
    labels={
        "value": "Contribution",
        "variable": "Factor",
        "Country": ""
    },
    color_discrete_sequence=[
        "#2E75B6",
        "#70AD47",
        "#FFC000",
        "#AAAAAA"
    ]
)

fig3.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    legend=dict(
        orientation="h"
    )
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

st.divider()
st.caption("Built with ❤️ using Streamlit & Plotly")
