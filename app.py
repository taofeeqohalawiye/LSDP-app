
import streamlit as st
import pandas as pd

# Load data
@st.cache_data
def load_data():
    return pd.read_excel("lsdp_initiatives.xlsx")

df = load_data()

# Page config
st.set_page_config(page_title="LSDP Initiatives Explorer", layout="wide")

# Header with Lagos logo
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

# Filtered Data
filtered_df = df[(df["TIMELINE"] == selected_timeline) & (df["LEAD MDA"] == selected_mda)]

# Initiative count by type
st.subheader("Summary")
initiative_counts = filtered_df["INITIATIVE TYPE"].value_counts()

for initiative_type, count in initiative_counts.items():
    st.markdown(f"- **{count} {initiative_type} initiatives**")

# Grouped display by initiative type
st.subheader("Grouped Initiatives Table")
for initiative_type in filtered_df["INITIATIVE TYPE"].dropna().unique():
    group_df = filtered_df[filtered_df["INITIATIVE TYPE"] == initiative_type]
    with st.expander(f"{initiative_type} ({len(group_df)} initiatives)"):
        st.dataframe(group_df.reset_index(drop=True))
