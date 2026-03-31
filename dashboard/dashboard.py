import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import os

sns.set(style="dark")
st.set_page_config(layout="wide")
st.title("⛽ Oil & Gas Production Dashboard")

# =========================
# LOAD DATA
# =========================


@st.cache_data
def load_data():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE_DIR, "all_data.csv")
    
    df = pd.read_csv(file_path, parse_dates=["Year"])
    return df

data = load_data()

# =========================
# SIDEBAR FILTER
# =========================
min_year = data["Year"].min().year
max_year = data["Year"].max().year

with st.sidebar:
    st.image("https://www.freeiconspng.com/uploads/oil-and-gas-icon-2.png")
    year_range = st.slider("Filter Tahun", min_year, max_year, (min_year, max_year))

main_df = data[(data["Year"].dt.year >= year_range[0]) & (data["Year"].dt.year <= year_range[1])]

# =========================
# 1️⃣ TREND PRODUKSI
# =========================
st.header("📈 Tren Produksi Minyak & Gas")

trend_oil = main_df.groupby("Year")["Oil Produced, bbl"].sum()
trend_gas = main_df.groupby("Year")["Gas Produced, Mcf"].sum()

col1, col2 = st.columns(2)
with col1:
    st.metric("Total Oil Produced", f"{trend_oil.sum():,.0f} bbl")
with col2:
    st.metric("Total Gas Produced", f"{trend_gas.sum():,.0f} Mcf")

fig, ax = plt.subplots(1,2, figsize=(14,5))
ax[0].plot(trend_oil.index, trend_oil.values, marker="o")
ax[0].set_title("Tren Produksi Minyak per Tahun")
ax[1].plot(trend_gas.index, trend_gas.values, marker="o", color="red")
ax[1].set_title("Tren Produksi Gas per Tahun")
st.pyplot(fig)

# =========================
# 2️⃣ TOP COUNTY
# =========================
st.header("🏆 Top County Produksi")

top_oil = main_df.groupby("County")["Oil Produced, bbl"].sum().sort_values(ascending=False).head(10)
top_gas = main_df.groupby("County")["Gas Produced, Mcf"].sum().sort_values(ascending=False).head(10)

col1, col2 = st.columns(2)
with col1:
    fig, ax = plt.subplots(figsize=(10,6))
    sns.barplot(x=top_oil.values, y=top_oil.index, ax=ax)
    ax.set_title("Top 10 County by Oil")
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(10,6))
    sns.barplot(x=top_gas.values, y=top_gas.index, ax=ax, color="red")
    ax.set_title("Top 10 County by Gas")
    st.pyplot(fig)

# =========================
# 3️⃣ TOP OPERATOR
# =========================
st.header("👷 Top Operator Produksi")

top_oil_op = main_df.groupby("Operator")["Oil Produced, bbl"].sum().sort_values(ascending=False).head(10)
top_gas_op = main_df.groupby("Operator")["Gas Produced, Mcf"].sum().sort_values(ascending=False).head(10)

col1, col2 = st.columns(2)
with col1:
    fig, ax = plt.subplots(figsize=(10,6))
    sns.barplot(x=top_oil_op.values, y=top_oil_op.index, ax=ax)
    ax.set_title("Top 10 Operator by Oil")
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(10,6))
    sns.barplot(x=top_gas_op.values, y=top_gas_op.index, ax=ax, color="red")
    ax.set_title("Top 10 Operator by Gas")
    st.pyplot(fig)

# =========================
# 4️⃣ CLUSTER SUMUR
# =========================

cluster_oil = main_df.groupby("Well Cluster")[["Oil Produced, bbl"]].mean()
cluster_gas = main_df.groupby("Well Cluster")[["Gas Produced, Mcf"]].mean()
st.header("🔎 Produksi Berdasarkan Cluster Sumur")

col1, col2 = st.columns(2)

# Visualisasi bar chart
fig, ax = plt.subplots(1,2, figsize=(14,5))
ax[0].bar(cluster_oil.index, cluster_oil["Oil Produced, bbl"])
ax[0].set_title("Produksi Minyak per Cluster")
ax[0].tick_params(axis="x", rotation=45)

ax[1].bar(cluster_gas.index, cluster_gas["Gas Produced, Mcf"], color="red")
ax[1].set_title("Produksi Gas per Cluster")
ax[1].tick_params(axis="x", rotation=45)

st.pyplot(fig)

# =========================
# 5️⃣ PETA DISTRIBUSI
# =========================
import folium
import streamlit as st

st.header("🗺️ Peta Distribusi Produksi")

# Buat peta
map_energy = folium.Map(
    location=[main_df["Latitude"].mean(), main_df["Longitude"].mean()],
    zoom_start=6
)

# Tambahkan marker
for _, row in main_df.iterrows():
    if row["Oil Produced, bbl"] > 0:
        folium.CircleMarker(
            location=[row["Latitude"], row["Longitude"]],
            radius=3,
            color="blue",
            fill=True,
            fill_color="blue"
        ).add_to(map_energy)
    if row["Gas Produced, Mcf"] > 0:
        folium.CircleMarker(
            location=[row["Latitude"], row["Longitude"]],
            radius=3,
            color="red",
            fill=True,
            fill_color="red"
        ).add_to(map_energy)

# Render peta ke Streamlit
st.components.v1.html(map_energy._repr_html_(), width=1200, height=500)