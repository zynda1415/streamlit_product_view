import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# Page config
st.set_page_config(page_title="Product Catalog", layout="wide")

# Authentication setup
def get_gspread_client():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # Load credentials from Streamlit Secrets
    # We create a copy to avoid mutating the original secrets object
    creds_dict = dict(st.secrets["gcp_service_account"])
    
    # FIX: This line handles the PEM/Private Key formatting error
    if "private_key" in creds_dict:
        creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
    
    credentials = Credentials.from_service_account_info(creds_dict, scopes=scope)
    return gspread.authorize(credentials)

@st.cache_data(ttl=300)  # Data refreshes every 5 minutes
def load_data(sheet_name):
    client = get_gspread_client()
    # Ensure this matches your Google Sheet name exactly
    sheet = client.open(sheet_name).get_worksheet(0)
    data = sheet.get_all_records()
    return pd.DataFrame(data)

def display_content(url):
    """Detects if URL is image or video and displays accordingly."""
    image_extensions = ('.jpg', '.jpeg', '.png', '.webp', '.gif')
    video_extensions = ('.mp4', '.webm', '.ogg', '.mov')
    
    lowered_url = str(url).lower()
    
    if any(lowered_url.endswith(ext) for ext in image_extensions):
        st.image(url, use_container_width=True)
    elif any(lowered_url.endswith(ext) for ext in video_extensions):
        st.video(url)
    else:
        st.info(f"🔗 [View Media Link]({url})")

def main():
    st.title("📦 Product Showcase")
    st.markdown("---")

    # --- UPDATE THIS TO YOUR SHEET NAME ---
    SHEET_NAME = "Your_Sheet_Name_Here" 
    # ---------------------------------------
    
    try:
        df = load_data(SHEET_NAME)
        
        # Grid layout: 3 products per row
        cols_per_row = 3
        for i in range(0, len(df), cols_per_row):
            cols = st.columns(cols_per_row)
            
            for j, col in enumerate(cols):
                if i + j < len(df):
                    row = df.iloc[i + j]
                    with col:
                        display_content(row['URL'])
                        
                        # Displaying Kurdish and Arabic Tags
                        with st.expander("Product Details / زانیاری بەرهەم", expanded=True):
                            st.subheader("Kurdish")
                            st.write(f"**Tags:** {row['Kurdish Tags']}")
                            st.caption(f"🎨 {row['Kurdish Color Tags']} | 🧵 {row['Kurdish Material Tags']}")
                            
                            st.divider()
                            
                            st.subheader("Arabic")
                            st.write(f"**Tags:** {row['Arabic Tags']}")
                            st.caption(f"🎨 {row['Arabic Colors Tags']} | 🧵 {row['Arabic Material Tags']}")
                            
    except Exception as e:
        st.error(f"Error: {e}")
        st.warning("Tip: Check that the Sheet Name is correct and shared with the service account email.")

if __name__ == "__main__":
    main()
