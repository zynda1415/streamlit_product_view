import streamlit as st
from settings import load_google_sheet, sidebar_controls
from display import render_products

st.set_page_config(
    page_title="Product Viewer",
    layout="wide"
)

language = sidebar_controls()

df = load_google_sheet()

# ---------- Filters ----------
if language == "ku":
    tag_col = "Kurdish Tags"
    color_col = "Kurdish Color Tags"
    material_col = "Kurdish Material Tags"
else:
    tag_col = "Arabic Tags"
    color_col = "Arabic Colors Tags"
    material_col = "Arabic Material Tags"

with st.sidebar:
    tag_filter = st.multiselect("Tags", sorted(df[tag_col].dropna().unique()))
    color_filter = st.multiselect("Colors", sorted(df[color_col].dropna().unique()))
    material_filter = st.multiselect("Material", sorted(df[material_col].dropna().unique()))

    view = st.selectbox(
        "View",
        ["Extra Large", "Large", "Medium", "Small"]
    )

# ---------- View → columns ----------
view_map = {
    "Extra Large": 2,
    "Large": 3,
    "Medium": 4,
    "Small": 6
}
columns = view_map[view]

# ---------- Apply filters ----------
if tag_filter:
    df = df[df[tag_col].isin(tag_filter)]
if color_filter:
    df = df[df[color_col].isin(color_filter)]
if material_filter:
    df = df[df[material_col].isin(material_filter)]

render_products(df, language, columns)
