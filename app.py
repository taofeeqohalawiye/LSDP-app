
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

st.set_page_config(page_title="LSDP Minimal Test", layout="wide")

@st.cache_data
def load_data():
    return pd.read_excel("lsdp_initiatives.xlsx")

df = load_data()

st.title("LSDP Initiatives Table (Test View)")

gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(wrapText=True, autoHeight=True)
gb.configure_pagination()
grid_options = gb.build()

AgGrid(df, gridOptions=grid_options, fit_columns_on_grid_load=True, height=500)
