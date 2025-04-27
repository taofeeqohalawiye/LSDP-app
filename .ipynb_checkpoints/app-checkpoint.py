
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

# Header with logo
col1, col2 = st.columns([1, 12])
with col1:
    st.image("lagos_logo.png", width=80)
with col2:
    st.title("LSDP 2052 Initiatives Explorer")

# Filters
selected_timeline = st.selectbox("Select Timeline", sorted(df["TIMELINE"].dropna().unique()))
selected_mda = st.selectbox("Select Lead MDA", sorted(df["LEAD MDA"].dropna().unique()))
initiative_type_filter = st.multiselect("Filter by Initiative Type", sorted(df["INITIATIVE TYPE"].dropna().unique()))
focus_area_filter = st.multiselect("Filter by Focus Area to see KPIs", sorted(df["FOCUS AREA"].dropna().unique()))
search_term = st.text_input("Search Initiatives (keywords):")

# Apply filters
filtered_df = df[(df["TIMELINE"] == selected_timeline) & (df["LEAD MDA"] == selected_mda)]
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

# AgGrid table for filtered initiatives
if not filtered_df.empty:
    st.subheader("Initiatives Table")
    gb = GridOptionsBuilder.from_dataframe(filtered_df)
    gb.configure_default_column(wrapText=True, autoHeight=True)
    gb.configure_pagination()
    grid_options = gb.build()
    AgGrid(filtered_df, gridOptions=grid_options, fit_columns_on_grid_load=True, height=1000)
else:
    st.warning("No initiatives found for the selected filters.")

# KPI card section
if focus_area_filter:
    for focus_area in focus_area_filter:
        kpis = kpi_df[kpi_df["FOCUS AREA"] == focus_area]["KPI"].dropna().tolist()
        if kpis:
            st.markdown(f"### KPIs for Focus Area: {focus_area}")
            for kpi in kpis:
                st.markdown(f"- {kpi}")
