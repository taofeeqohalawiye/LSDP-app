
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

# Filters
selected_timeline = st.selectbox("Select Timeline", sorted(df["TIMELINE"].dropna().unique()))
selected_mda = st.selectbox("Select Lead MDA", sorted(df["LEAD MDA"].dropna().unique()))

# Filter base data by MDA and Timeline
base_df = df[(df["TIMELINE"] == selected_timeline) & (df["LEAD MDA"] == selected_mda)]

# Dynamic slicers based on MDA context
available_focus_areas = sorted(base_df["FOCUS AREA"].dropna().unique())
available_initiative_types = sorted(base_df["INITIATIVE TYPE"].dropna().unique())

focus_area_filter = st.multiselect("Filter by Focus Area", options=available_focus_areas)
initiative_type_filter = st.multiselect("Filter by Initiative Type", options=available_initiative_types)
search_term = st.text_input("Search Initiatives (keywords):")

# Apply all filters
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

# Show initiative table
if not filtered_df.empty:
    st.subheader("Initiatives Table")
    gb = GridOptionsBuilder.from_dataframe(filtered_df)
    gb.configure_default_column(wrapText=True, autoHeight=True)
    gb.configure_pagination()
    grid_options = gb.build()
    AgGrid(filtered_df, gridOptions=grid_options, fit_columns_on_grid_load=True, height=1000)
else:
    st.warning("No initiatives found for the selected filters.")

# Show all KPIs applicable to MDA's focus areas
mda_focus_areas = base_df["FOCUS AREA"].dropna().unique()
st.subheader("KPIs Linked to Selected MDA")
for fa in mda_focus_areas:
    kpis = kpi_df[kpi_df["FOCUS AREA"] == fa]["KPI"].dropna().tolist()
    if kpis:
        st.markdown(f"**Focus Area: {fa}**")
        for kpi in kpis:
            st.markdown(f"- {kpi}")
