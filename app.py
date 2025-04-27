
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from io import BytesIO

st.set_page_config(page_title="LSDP Initiatives Explorer", layout="wide")

@st.cache_data
def load_data():
    df_initiatives = pd.read_excel("lsdp_initiatives.xlsx")
    df_kpis = pd.read_excel("LSDP KPI .xlsx")
    return df_initiatives, df_kpis

df, kpi_df = load_data()

# Header
col1, col2 = st.columns([1, 12])
with col1:
    st.image("lagos_logo.png", width=80)
with col2:
    st.title("LSDP Initiatives Explorer")

# Filters
selected_timeline = st.selectbox("Select Timeline", sorted(df["TIMELINE"].dropna().unique()))
selected_mda = st.selectbox("Select Lead MDA", sorted(df["LEAD MDA"].dropna().unique()))

initiative_type_filter = st.multiselect("Filter by Initiative Type", options=sorted(df["INITIATIVE TYPE"].dropna().unique()))
focus_area_filter = st.multiselect("Filter by Focus Area", options=sorted(df["FOCUS AREA"].dropna().unique()))

search_term = st.text_input("Search Initiatives (keywords):")

# Apply filters
filtered_df = df[(df["TIMELINE"] == selected_timeline) & (df["LEAD MDA"] == selected_mda)]

if initiative_type_filter:
    filtered_df = filtered_df[filtered_df["INITIATIVE TYPE"].isin(initiative_type_filter)]

if focus_area_filter:
    filtered_df = filtered_df[filtered_df["FOCUS AREA"].isin(focus_area_filter)]

if search_term:
    filtered_df = filtered_df[filtered_df["INITIATIVES"].str.contains(search_term, case=False, na=False)]

# Summary
st.subheader("Summary")
initiative_counts = filtered_df["INITIATIVE TYPE"].value_counts()
if filtered_df.empty:
    st.warning("No initiatives found for this combination.")
else:
    for itype, count in initiative_counts.items():
        st.markdown(f"- **{count} {itype} initiatives**")

    # Export
    def convert_df_to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Filtered")
        output.seek(0)
        return output

    st.download_button("Download filtered data as Excel",
        data=convert_df_to_excel(filtered_df),
        file_name="filtered_initiatives.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # Show table
    st.subheader("Initiatives Table")
    gb = GridOptionsBuilder.from_dataframe(filtered_df)
    gb.configure_default_column(wrapText=True, autoHeight=True)
    gb.configure_pagination()
    grid_options = gb.build()

    AgGrid(filtered_df, gridOptions=grid_options, fit_columns_on_grid_load=True, height=500)

    # KPI section below the table
    if len(focus_area_filter) == 1:
        focus_area = focus_area_filter[0]
        matching_kpis = kpi_df[kpi_df["FOCUS AREA"] == focus_area]["KPI"].dropna().tolist()

        if matching_kpis:
            st.markdown(f"### KPIs for Focus Area: {focus_area}")
            for kpi in matching_kpis:
                st.markdown(f"- {kpi}")
