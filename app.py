import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Asanar Product Preview",
    layout="wide"
)

st.title("🖼️ Asanar Product Images & Videos Preview")

# ---------------- AUTH ----------------
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

credentials = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)

gc = gspread.authorize(credentials)

# ---------------- LOAD SHEET ----------------
SHEET_NAME = "asanar_product_images"

try:
    sh = gc.open(SHEET_NAME)
    worksheet = sh.sheet1
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

except Exception as e:
    st.error("❌ Failed to load Google Sheet")
    st.code(str(e))
    st.stop()

# ---------------- VALIDATION ----------------
required_columns = [
    "URL",
    "Kurdish Tags",
    "Kurdish Color Tags",
    "Kurdish Material Tags",
    "Arabic Tags",
    "Arabic Colors Tags",
    "Arabic Material Tags"
]

missing = [c for c in required_columns if c not in df.columns]
if missing:
    st.error(f"Missing columns: {missing}")
    st.stop()

# ---------------- FILTER UI ----------------
st.sidebar.header("🔍 Filters")

tag_search = st.sidebar.text_input("Search Tag (any language)")
media_type = st.sidebar.selectbox(
    "Media Type",
    ["All", "Images", "Videos"]
)

# ---------------- FILTER LOGIC ----------------
filtered_df = df.copy()

if tag_search:
    filtered_df = filtered_df[
        filtered_df.apply(
            lambda row: tag_search.lower() in " ".join(row.astype(str)).lower(),
            axis=1
        )
    ]

# ---------------- DISPLAY ----------------
cols = st.columns(3)

for index, row in filtered_df.iterrows():
    url = row["URL"]
    lower_url = url.lower()

    col = cols[index % 3]

    with col:
        if lower_url.endswith((".jpg", ".jpeg", ".png", ".webp")):
            if media_type in ["All", "Images"]:
                st.image(url, use_container_width=True)

        elif lower_url.endswith((".mp4", ".mov", ".webm")):
            if media_type in ["All", "Videos"]:
                st.video(url)

        else:
            st.warning("Unsupported file type")

        st.caption(
            f"""
            **Kurdish:** {row['Kurdish Tags']}  
            **Arabic:** {row['Arabic Tags']}
            """
        )
