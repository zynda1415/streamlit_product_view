import streamlit as st
import json
import os

DATA_FILE = "app_data.json"

# ---------------- JSON DATA HANDLING ----------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"logo": None, "language": "Kurdish", "products": []}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# ---------------- LOGO UPLOADING ----------------
def upload_logo(data):
    uploaded_file = st.sidebar.file_uploader("Upload Logo", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        data["logo"] = uploaded_file.read()
        save_data(data)
        st.sidebar.success("✅ Logo uploaded!")

# ---------------- LANGUAGE SELECTION ----------------
def select_language(data):
    lang = st.sidebar.selectbox("Select Language", ["Kurdish", "Arabic"], index=0 if data.get("language")=="Kurdish" else 1)
    data["language"] = lang
    save_data(data)
    return lang

# ---------------- PRODUCTS MANAGEMENT ----------------
def add_product(data):
    st.sidebar.header("Add Product")
    url = st.sidebar.text_input("Product URL")
    kur_tags = st.sidebar.text_input("Kurdish Tags")
    ar_tags = st.sidebar.text_input("Arabic Tags")
    if st.sidebar.button("Add Product"):
        if url:
            product = {
                "URL": url,
                "Kurdish Tags": kur_tags,
                "Arabic Tags": ar_tags
            }
            data["products"].append(product)
            save_data(data)
            st.sidebar.success("✅ Product added!")
