
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

# Filters
selected_timeline = st.multiselect("Select Timeline", sorted(df["TIMELINE"].dropna().unique()))
selected_mda = st.multiselect("Select Lead MDA", sorted(df["LEAD MDA"].dropna().unique()))

base_df = df[(df["TIMELINE"].isin(selected_timeline)) & (df["LEAD MDA"].isin(selected_mda))]

available_focus_areas = sorted(base_df["FOCUS AREA"].dropna().unique())
available_initiative_types = sorted(base_df["INITIATIVE TYPE"].dropna().unique())

focus_area_filter = st.multiselect("Filter by Focus Area", options=available_focus_areas)
initiative_type_filter = st.multiselect("Filter by Initiative Type", options=available_initiative_types)
search_term = st.text_input("Search Initiatives (keywords):")

filtered_df = base_df.copy()
if focus_area_filter:
    filtered_df = filtered_df[filtered_df["FOCUS AREA"].isin(focus_area_filter)]
if initiative_type_filter:
    filtered_df = filtered_df[filtered_df["INITIATIVE TYPE"].isin(initiative_type_filter)]
if search_term:
    filtered_df = filtered_df[filtered_df["INITIATIVES"].str.contains(search_term, case=False, na=False)]

# Summary
st.subheader("Summary")
initiative_counts = filtered_df["INITIATIVE TYPE"].value_counts()
for initiative_type, count in initiative_counts.items():
    st.markdown(f"- **{count} {initiative_type} initiatives**")

# Toggle for table display
view_mode = st.radio("Choose Table Mode", ["Interactive Table", "Simple Table (Mobile-Friendly)"])

st.subheader("Initiatives Table")
if not filtered_df.empty:
    if view_mode == "Interactive Table":
        gb = GridOptionsBuilder.from_dataframe(filtered_df)
        gb.configure_default_column(wrapText=True, autoHeight=True)
        gb.configure_pagination()
        grid_options = gb.build()
        AgGrid(filtered_df, gridOptions=grid_options, fit_columns_on_grid_load=True, height=1000)
    else:
        st.dataframe(filtered_df, use_container_width=True)
else:
    st.warning("No initiatives found for the selected filters.")

# KPI Cards grouped by MDA focus areas
mda_focus_areas = base_df["FOCUS AREA"].dropna().unique()
st.subheader("KPIs Linked to Selected MDA")
for fa in mda_focus_areas:
    kpis = kpi_df[kpi_df["FOCUS AREA"].str.strip() == fa.strip()]["KPI"].dropna().tolist()
    if kpis:
        st.markdown(f"**Focus Area: {fa}**")
        for kpi in kpis:
            st.markdown(f"- {kpi}")
