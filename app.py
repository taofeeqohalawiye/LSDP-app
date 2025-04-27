
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from io import BytesIO

st.set_page_config(page_title="LSDP Initiatives Explorer", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_excel("lsdp_initiatives.xlsx")
    df.columns = df.columns.str.strip().str.upper()
    return df

df = load_data()

# Rename reference for consistency
df = df.rename(columns={"INITIATIVES": "INITIATIVE"})

# Header
col1, col2 = st.columns([1, 12])
with col1:
    st.image("lagos_logo.png", width=80)
with col2:
    st.title("LSDP Initiatives Explorer")

# Filters
timeline_options = df["TIMELINE"].dropna().unique()
mda_options = df["LEAD MDA"].dropna().unique()

selected_timeline = st.selectbox("Select Timeline", sorted(timeline_options))
selected_mda = st.selectbox("Select Lead MDA", sorted(mda_options))
search_term = st.text_input("Search Initiatives (keywords):")

# Apply filters
filtered_df = df[(df["TIMELINE"] == selected_timeline) & (df["LEAD MDA"] == selected_mda)]

if search_term:
    filtered_df = filtered_df[filtered_df["INITIATIVE"].str.contains(search_term, case=False, na=False)]

# Summary
st.subheader("Summary")
initiative_counts = filtered_df["INITIATIVE TYPE"].value_counts()
if filtered_df.empty:
    st.warning("No initiatives found for this combination.")
else:
    for initiative_type, count in initiative_counts.items():
        st.markdown(f"- **{count} {initiative_type} initiatives**")

    # Export
    def convert_df_to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Filtered Initiatives')
        output.seek(0)
        return output

    st.download_button(
        label="Download all filtered data as Excel",
        data=convert_df_to_excel(filtered_df),
        file_name="filtered_initiatives.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # Grouped tables
    st.subheader("Grouped Initiatives Table")
    for initiative_type in filtered_df["INITIATIVE TYPE"].dropna().unique():
        group_df = filtered_df[filtered_df["INITIATIVE TYPE"] == initiative_type]
        with st.expander(f"{initiative_type} ({len(group_df)} initiatives)"):
            gb = GridOptionsBuilder.from_dataframe(group_df)
            gb.configure_default_column(wrapText=True, autoHeight=True)
            gb.configure_pagination()
            grid_options = gb.build()
            AgGrid(group_df, gridOptions=grid_options, fit_columns_on_grid_load=True, height=300)
