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
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Modern CSS styling
st.markdown("""
    <style>
    /* Main styling */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Hero section */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 4rem 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 3rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        opacity: 0.95;
        font-weight: 300;
    }
    
    /* Category pills */
    .category-pill {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 25px;
        font-weight: 600;
        margin: 0.5rem 0.5rem 0.5rem 0;
        font-size: 0.9rem;
    }
    
    /* Project cards */
    .project-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 2rem;
        border: 1px solid #f0f0f0;
    }
    
    .project-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .project-number {
        color: #667eea;
        font-weight: 700;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    
    /* Images */
    .stImage {
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Stats section */
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin: 2rem 0 3rem 0;
        padding: 2rem;
        background: #f8f9fa;
        border-radius: 15px;
    }
    
    .stat-box {
        text-align: center;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 800;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        color: #6c757d;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        margin-top: 4rem;
    }
    
    .footer-title {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .contact-button {
        display: inline-block;
        padding: 1rem 2.5rem;
        background: white;
        color: #667eea;
        border-radius: 30px;
        font-weight: 700;
        text-decoration: none;
        margin-top: 1rem;
        transition: transform 0.3s ease;
    }
    
    .contact-button:hover {
        transform: scale(1.05);
    }
    
    /* Filter buttons */
    .filter-container {
        margin: 2rem 0;
        text-align: center;
    }
    
    /* Divider */
    .custom-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 2rem 0;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
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
        scope = [
            'https://www.googleapis.com/auth/spreadsheets.readonly',
            'https://www.googleapis.com/auth/drive.readonly'
        ]
        
        credentials = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=scope
        )
        
        client = gspread.authorize(credentials)
        sheet = client.open("Streamlit Sheet product view").sheet1
        
        return sheet
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return None

# Function to load data from Google Sheets
@st.cache_data(ttl=300)
def load_data():
    """Load data from Google Sheets"""
    sheet = get_google_sheet()
    if sheet is None:
        return pd.DataFrame(columns=['URL', 'Image/Video', 'Title', 'Category'])
    
    try:
        data = sheet.get_all_values()
        
        if len(data) > 1:
            df = pd.DataFrame(data[1:], columns=data[0])
            df = df[df['URL'].str.strip() != '']
            
            # Add Title and Category columns if they don't exist
            if 'Title' not in df.columns:
                df['Title'] = ''
            if 'Category' not in df.columns:
                df['Category'] = ''
            
            return df
        else:
            return pd.DataFrame(columns=['URL', 'Image/Video', 'Title', 'Category'])
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return pd.DataFrame(columns=['URL', 'Image/Video', 'Title', 'Category'])

# Main app
def main():
    # Hero Section
    st.markdown("""
        <div class="hero-section">
            <div class="hero-title">✨ Interior Design Portfolio</div>
            <div class="hero-subtitle">Transform Your Space into a Masterpiece</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Load data
    with st.spinner("Loading our latest projects..."):
        df = load_data()
    
    if df.empty:
        st.info("🎨 Portfolio coming soon! Check back later for amazing designs.")
        return
    
    # Stats Section
    total_projects = len(df)
    total_images = len(df[df['Image/Video'].str.lower().str.contains('image', na=False)])
    total_videos = len(df[df['Image/Video'].str.lower().str.contains('video', na=False)])
    
    st.markdown(f"""
        <div class="stats-container">
            <div class="stat-box">
                <div class="stat-number">{total_projects}</div>
                <div class="stat-label">Total Projects</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{total_images}</div>
                <div class="stat-label">Photos</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{total_videos}</div>
                <div class="stat-label">Videos</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Filter by category if available
    if 'Category' in df.columns and df['Category'].str.strip().any():
        categories = ['All'] + sorted(df['Category'].str.strip().unique().tolist())
        categories = [cat for cat in categories if cat]  # Remove empty strings
        
        if len(categories) > 1:
            st.markdown('<div class="filter-container">', unsafe_allow_html=True)
            selected_category = st.selectbox(
                "Filter by Category",
                categories,
                label_visibility="collapsed"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            if selected_category != 'All':
                df = df[df['Category'].str.strip() == selected_category]
    
    # Divider
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # Display projects in a grid
    cols_per_row = 2
    
    for idx, row in df.iterrows():
        url = row.get('URL', '').strip()
        content_type = row.get('Image/Video', '').strip().lower()
        title = row.get('Title', '').strip()
        category = row.get('Category', '').strip()
        
        if not url:
            continue
        
        # Create a new row every cols_per_row items
        if idx % cols_per_row == 0:
            cols = st.columns(cols_per_row)
        
        col_idx = idx % cols_per_row
        
        with cols[col_idx]:
            st.markdown('<div class="project-card">', unsafe_allow_html=True)
            
            # Project number and category
            st.markdown(f'<div class="project-number">Project {idx + 1}</div>', unsafe_allow_html=True)
            if category:
                st.markdown(f'<span class="category-pill">{category}</span>', unsafe_allow_html=True)
            
            try:
                if 'video' in content_type or 'youtube' in url.lower() or 'youtu.be' in url.lower():
                    # Display YouTube video
                    video_id = get_youtube_id(url)
                    if video_id:
                        st.video(f"https://www.youtube.com/watch?v={video_id}")
                    else:
                        st.warning(f"Invalid YouTube URL")
                
                elif 'image' in content_type or any(ext in url.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
                    # Display image
                    try:
                        response = requests.get(url, timeout=10)
                        img = Image.open(BytesIO(response.content))
                        st.image(img, use_container_width=True)
                    except:
                        st.image(url, use_container_width=True)
                
                # Display title if available
                if title:
                    st.markdown(f"**{title}**")
            
            except Exception as e:
                st.error(f"Error loading content")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer CTA
    st.markdown("""
        <div class="footer">
            <div class="footer-title">Ready to Transform Your Space?</div>
            <p>Let's create something beautiful together</p>
            <a href="mailto:your-email@example.com" class="contact-button">
                📧 Contact Us
            </a>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
