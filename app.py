import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from PIL import Image
import requests
from io import BytesIO
import re

# Page configuration
st.set_page_config(
    page_title="Interior Design Portfolio",
    page_icon="🏠",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stImage {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    h1 {
        color: #2c3e50;
        text-align: center;
        margin-bottom: 2rem;
    }
    .product-container {
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Function to extract YouTube video ID
def get_youtube_id(url):
    """Extract YouTube video ID from URL"""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
        r'youtube\.com\/watch\?.*v=([^&\n?#]+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

# Function to connect to Google Sheets
@st.cache_resource
def get_google_sheet():
    """Connect to Google Sheets using service account credentials"""
    try:
        # Define the scope
        scope = [
            'https://www.googleapis.com/auth/spreadsheets.readonly',
            'https://www.googleapis.com/auth/drive.readonly'
        ]
        
        # Load credentials from Streamlit secrets
        credentials = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=scope
        )
        
        # Authorize and connect
        client = gspread.authorize(credentials)
        
        # Open the sheet by name
        sheet = client.open("Streamlit Sheet product view").sheet1
        
        return sheet
    except gspread.exceptions.SpreadsheetNotFound:
        st.error("❌ Could not find the Google Sheet 'Streamlit Sheet product view'. Please check the sheet name.")
        return None
    except gspread.exceptions.APIError as e:
        st.error(f"❌ Google Sheets API Error: {str(e)}")
        return None
    except Exception as e:
        st.error(f"❌ Error connecting to Google Sheets: {str(e)}")
        st.info("💡 Make sure the sheet is shared with: streamlit-key@gen-lang-client-0089966801.iam.gserviceaccount.com")
        return None

# Function to load data from Google Sheets
@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_data():
    """Load data from Google Sheets"""
    sheet = get_google_sheet()
    if sheet is None:
        return pd.DataFrame(columns=['URL', 'Image/Video'])
    
    try:
        # Get all values
        data = sheet.get_all_values()
        
        # Debug info
        st.write(f"📊 Retrieved {len(data)} rows from Google Sheets")
        
        # Convert to DataFrame
        if len(data) > 1:
            df = pd.DataFrame(data[1:], columns=data[0])
            # Remove empty rows
            df = df[df['URL'].str.strip() != '']
            return df
        elif len(data) == 1:
            # Only headers, no data
            st.warning("⚠️ Google Sheet found but no data rows. Please add some content.")
            return pd.DataFrame(columns=data[0])
        else:
            # Empty sheet
            st.warning("⚠️ Google Sheet is empty. Please add headers and data.")
            return pd.DataFrame(columns=['URL', 'Image/Video'])
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        import traceback
        st.code(traceback.format_exc())
        return pd.DataFrame(columns=['URL', 'Image/Video'])

# Main app
def main():
    # Header
    st.title("🏠 Interior Design Portfolio")
    st.markdown("---")
    
    # Add refresh button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col3:
        if st.button("🔄 Refresh Content"):
            st.cache_data.clear()
            st.rerun()
    
    # Load data
    with st.spinner("Loading portfolio..."):
        df = load_data()
    
    if df.empty:
        st.info("No products found. Please add content to your Google Sheet.")
        st.markdown("""
        ### Instructions:
        1. Open your Google Sheet: **Streamlit Sheet product view**
        2. Add URLs in column A (images or YouTube videos)
        3. Add the type in column B ("Image" or "Video")
        4. Click the Refresh button above
        """)
        return
    
    # Filter and display content
    st.subheader(f"📸 Showcasing {len(df)} Projects")
    st.markdown("---")
    
    # Create columns for grid layout
    cols_per_row = 2
    
    for idx, row in df.iterrows():
        url = row.get('URL', '').strip()
        content_type = row.get('Image/Video', '').strip().lower()
        
        if not url:
            continue
        
        # Create a new row every cols_per_row items
        if idx % cols_per_row == 0:
            cols = st.columns(cols_per_row)
        
        col_idx = idx % cols_per_row
        
        with cols[col_idx]:
            with st.container():
                try:
                    if 'video' in content_type or 'youtube' in url.lower() or 'youtu.be' in url.lower():
                        # Display YouTube video
                        video_id = get_youtube_id(url)
                        if video_id:
                            st.markdown(f"### Project {idx + 1}")
                            st.video(f"https://www.youtube.com/watch?v={video_id}")
                        else:
                            st.warning(f"Invalid YouTube URL: {url}")
                    
                    elif 'image' in content_type or any(ext in url.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
                        # Display image
                        st.markdown(f"### Project {idx + 1}")
                        try:
                            # Try to load image from URL
                            response = requests.get(url, timeout=10)
                            img = Image.open(BytesIO(response.content))
                            st.image(img, use_container_width=True)
                        except Exception as e:
                            # If direct URL doesn't work, try as markdown
                            st.image(url, use_container_width=True)
                    
                    else:
                        st.warning(f"Unknown content type for: {url}")
                
                except Exception as e:
                    st.error(f"Error loading content: {str(e)}")
                
                st.markdown("---")
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #7f8c8d; padding: 2rem;'>
            <p>Interior Design Portfolio | Powered by Streamlit</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
