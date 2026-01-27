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

# Modern CSS styling with YouTube-style filters
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
    
    /* YouTube-style filter pills */
    .filter-container {
        display: flex;
        gap: 10px;
        padding: 1rem 0 2rem 0;
        overflow-x: auto;
        white-space: nowrap;
    }
    
    .filter-pill {
        display: inline-block;
        padding: 0.5rem 1.2rem;
        background: #f1f1f1;
        color: #030303;
        border-radius: 8px;
        font-weight: 500;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.2s ease;
        border: 1px solid transparent;
        text-decoration: none;
    }
    
    .filter-pill:hover {
        background: #e5e5e5;
    }
    
    .filter-pill-active {
        background: #030303;
        color: white;
        border: 1px solid #030303;
    }
    
    /* Category badge on cards */
    .category-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 6px;
        font-weight: 600;
        margin: 0.5rem 0;
        font-size: 0.85rem;
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
    
    .project-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #2c3e50;
        margin: 0.5rem 0;
    }
    
    .project-description {
        color: #6c757d;
        font-size: 0.9rem;
        line-height: 1.6;
        margin: 0.5rem 0;
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
    
    /* Divider */
    .custom-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 2rem 0;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Streamlit button styling */
    .stButton > button {
        background: #f1f1f1;
        color: #030303;
        border: 1px solid #e5e5e5;
        border-radius: 8px;
        padding: 0.5rem 1.2rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: #e5e5e5;
        border-color: #d0d0d0;
    }
    
    /* Active filter button */
    div[data-testid="stHorizontalBlock"] button[kind="secondary"] {
        background: #030303 !important;
        color: white !important;
        border-color: #030303 !important;
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
        return pd.DataFrame(columns=['URL', 'Image/Video', 'Title', 'Category', 'Description'])
    
    try:
        data = sheet.get_all_values()
        
        if len(data) > 1:
            df = pd.DataFrame(data[1:], columns=data[0])
            df = df[df['URL'].str.strip() != '']
            
            # Add columns if they don't exist
            for col in ['Title', 'Category', 'Description']:
                if col not in df.columns:
                    df[col] = ''
            
            return df
        else:
            return pd.DataFrame(columns=['URL', 'Image/Video', 'Title', 'Category', 'Description'])
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return pd.DataFrame(columns=['URL', 'Image/Video', 'Title', 'Category', 'Description'])

# Main app
def main():
    # Initialize session state for filter
    if 'selected_filter' not in st.session_state:
        st.session_state.selected_filter = 'All'
    
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
    
    # Get unique categories
    categories = ['All']
    if 'Category' in df.columns:
        unique_cats = sorted([cat.strip() for cat in df['Category'].unique() if cat.strip()])
        categories.extend(unique_cats)
    
    # YouTube-style filter buttons
    st.markdown("### 🎯 Browse by Category")
    
    # Create filter buttons
    cols = st.columns(len(categories))
    for idx, category in enumerate(categories):
        with cols[idx]:
            # Custom button styling based on selection
            button_type = "secondary" if st.session_state.selected_filter == category else "primary"
            if st.button(category, key=f"filter_{category}", use_container_width=True):
                st.session_state.selected_filter = category
                st.rerun()
    
    # Filter data based on selection
    if st.session_state.selected_filter != 'All':
        filtered_df = df[df['Category'].str.strip() == st.session_state.selected_filter]
    else:
        filtered_df = df
    
    # Stats Section
    total_projects = len(filtered_df)
    total_images = len(filtered_df[filtered_df['Image/Video'].str.lower().str.contains('image', na=False)])
    total_videos = len(filtered_df[filtered_df['Image/Video'].str.lower().str.contains('video', na=False)])
    
    st.markdown(f"""
        <div class="stats-container">
            <div class="stat-box">
                <div class="stat-number">{total_projects}</div>
                <div class="stat-label">Projects</div>
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
    
    # Divider
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # Display message if no projects in category
    if filtered_df.empty:
        st.info(f"No projects found in '{st.session_state.selected_filter}' category.")
        return
    
    # Display projects in a grid
    cols_per_row = 2
    
    for idx, (_, row) in enumerate(filtered_df.iterrows()):
        url = row.get('URL', '').strip()
        content_type = row.get('Image/Video', '').strip().lower()
        title = row.get('Title', '').strip()
        category = row.get('Category', '').strip()
        description = row.get('Description', '').strip()
        
        if not url:
            continue
        
        # Create a new row every cols_per_row items
        if idx % cols_per_row == 0:
            cols = st.columns(cols_per_row)
        
        col_idx = idx % cols_per_row
        
        with cols[col_idx]:
            st.markdown('<div class="project-card">', unsafe_allow_html=True)
            
            # Project number
            st.markdown(f'<div class="project-number">Project {idx + 1}</div>', unsafe_allow_html=True)
            
            # Category badge
            if category:
                st.markdown(f'<span class="category-badge">{category}</span>', unsafe_allow_html=True)
            
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
                
                # Display title
                if title:
                    st.markdown(f'<div class="project-title">{title}</div>', unsafe_allow_html=True)
                
                # Display description
                if description:
                    st.markdown(f'<div class="project-description">{description}</div>', unsafe_allow_html=True)
            
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
