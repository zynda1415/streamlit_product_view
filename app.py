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
    creds_dict = st.secrets["gcp_service_account"]
    credentials = Credentials.from_service_account_info(creds_dict, scopes=scope)
    return gspread.authorize(credentials)

@st.cache_data(ttl=600)  # Cache data for 10 minutes to stay fast
def load_data(sheet_name):
    client = get_gspread_client()
    # Replace with your actual Sheet Name or Sheet ID
    sheet = client.open(sheet_name).get_worksheet(0)
    data = sheet.get_all_records()
    return pd.DataFrame(data)

def display_content(url):
    """Detects if URL is image or video and displays accordingly."""
    image_extensions = ('.jpg', '.jpeg', '.png', '.webp', '.gif')
    video_extensions = ('.mp4', '.webm', '.ogg', '.mov')
    
    lowered_url = url.lower()
    
    if any(lowered_url.endswith(ext) for ext in image_extensions):
        st.image(url, use_container_width=True)
    elif any(lowered_url.endswith(ext) for ext in video_extensions):
        st.video(url)
    else:
        st.warning(f"Unsupported format or direct link: [Click here to view]({url})")

def main():
    st.title("📦 Product Showcase")
    st.markdown("---")

    # UPDATE THIS: Put your Google Sheet name here
    SHEET_NAME = "Your_Google_Sheet_Name_Here" 
    
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
                        # Display Media
                        display_content(row['URL'])
                        
                        # Display Tags in an organized way
                        with st.expander("View Details", expanded=True):
                            st.markdown(f"**Kurdish:** {row['Kurdish Tags']}")
                            st.caption(f"🎨 {row['Kurdish Color Tags']} | 🧵 {row['Kurdish Material Tags']}")
                            
                            st.markdown("---")
                            
                            st.markdown(f"**Arabic:** {row['Arabic Tags']}")
                            st.caption(f"🎨 {row['Arabic Colors Tags']} | 🧵 {row['Arabic Material Tags']}")
                            
    except Exception as e:
        st.error(f"Error connecting to Google Sheets: {e}")
        st.info("Make sure the Google Sheet name matches and it is shared with the service account email.")

if __name__ == "__main__":
    main()
