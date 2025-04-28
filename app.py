
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from io import BytesIO

st.set_page_config(page_title="LSDP 2052 Initiatives Explorer", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_excel("lsdp_initiatives.xlsx")
    kpi_df = pd.read_excel("LSDP KPI .xlsx")
    return df, kpi_df

df, kpi_df = load_data()

# Header
col1, col2 = st.columns([1, 12])
with col1:
    st.image("lagos_logo.png", width=80)
with col2:
    st.title("LSDP 2052 Initiatives Explorer")

# Vision
st.markdown("### Vision")
st.markdown("*To become Africa’s model megacity — a global economic hub that is safe, secure, functional, and productive.*")

# LSDP Essence
st.markdown("### LSDP 2052 – Essence")
st.markdown("*The Lagos State Development Plan (LSDP) 2052 is a comprehensive 30-year blueprint guiding the state's transformation into a globally competitive megacity. Anchored on four strategic pillars — Thriving Economy, Human-centric City, Modern Infrastructure, and Effective Governance — it outlines 447 strategic initiatives aimed at fostering inclusive prosperity, resilience, and innovation across all sectors.*")

# Tagline
st.markdown("#### _A 30-Year Blueprint for Prosperity and Innovation_")

# Continue with filters and table logic...
