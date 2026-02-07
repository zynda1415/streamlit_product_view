import streamlit as st
import re
from urllib.parse import urlparse

FALLBACK_LOGO = "fallback_logo.png"

# ----------------- Media Detection Helpers -----------------
def is_youtube(url: str) -> bool:
    """Check if URL is a YouTube video"""
    if not url or not isinstance(url, str):
        return False
    return "youtube.com" in url.lower() or "youtu.be" in url.lower()

def is_image(url: str) -> bool:
    """Check if URL is an image"""
    if not url or not isinstance(url, str):
        return False
    image_extensions = [".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".svg"]
    return any(url.lower().endswith(ext) for ext in image_extensions)

def extract_youtube_id(url: str) -> str:
    """Extract YouTube video ID from URL"""
    try:
        if "youtu.be" in url:
            return url.split("/")[-1].split("?")[0]
        elif "youtube.com" in url:
            if "v=" in url:
                return url.split("v=")[1].split("&")[0]
            elif "embed/" in url:
                return url.split("embed/")[1].split("?")[0]
        return None
    except:
        return None

def is_valid_url(url: str) -> bool:
    """Validate URL format"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

# ----------------- Product Card Component -----------------
def render_product_card(row, idx, language="Kurdish"):
    """
    Render a single product card with media, details, and interaction buttons
    """
    # Get language-specific labels
    if language == "Kurdish":
        tag_label = "بابەتی"
        color_label = "ڕەنگی"
        material_label = "پێکهاتەی"
    else:
        tag_label = "عنصر"
        color_label = "الالوان"
        material_label = "مكون من"
    
    # Extract data
    tags = row.get(tag_label, "N/A")
    colors = row.get(color_label, "N/A")
    materials = row.get(material_label, "N/A")
    url = row.get("URL", "")
    
    # Card container with styling
    with st.container():
        # Media display
        media_success = False
        
        try:
            if is_youtube(url):
                video_id = extract_youtube_id(url)
                if video_id:
                    embed_url = f"https://www.youtube.com/embed/{video_id}"
                    st.video(embed_url)
                    media_success = True
                else:
                    st.warning("⚠️ Invalid YouTube URL")
            
            elif is_image(url):
                if is_valid_url(url):
                    st.image(url, use_container_width=True)
                    media_success = True
                else:
                    st.warning("⚠️ Invalid image URL")
            
            elif url:
                st.info("ℹ️ Unsupported media type")
            else:
                st.warning("⚠️ No media URL provided")
                
        except Exception as e:
            st.error(f"❌ Error loading media: {str(e)[:50]}")
        
        # Product details with better formatting
        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 1rem;
            border-radius: 8px;
            margin: 0.5rem 0;
        '>
            <p style='margin: 0.3rem 0; font-size: 0.9rem;'>
                <strong>{tag_label}:</strong> {tags}
            </p>
            <p style='margin: 0.3rem 0; font-size: 0.9rem;'>
                <strong>{color_label}:</strong> {colors}
            </p>
            <p style='margin: 0.3rem 0; font-size: 0.9rem;'>
                <strong>{material_label}:</strong> {materials}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Favorite button
            is_favorite = idx in st.session_state.favorites
            fav_icon = "❤️" if is_favorite else "🤍"
            if st.button(fav_icon, key=f"fav_{idx}", use_container_width=True):
                if is_favorite:
                    st.session_state.favorites.remove(idx)
                else:
                    st.session_state.favorites.add(idx)
                st.rerun()
        
        with col2:
            # View details button
            if st.button("👁️", key=f"view_{idx}", use_container_width=True, help="View details"):
                st.session_state.selected_product = row
                st.rerun()
        
        with col3:
            # Share/Link button
            if url and is_valid_url(url):
                st.link_button("🔗", url, use_container_width=True, help="Open link")
            else:
                st.button("🔗", key=f"link_{idx}", disabled=True, use_container_width=True)

# ----------------- Display Products Grid -----------------
def display_products(df, language="Kurdish", columns_count=3, visible_count=12):
    """
    Display products in a responsive grid layout with error handling
    """
    if df is None or df.empty:
        st.info("📭 No products to display")
        return
    
    # Limit to visible count
    df_display = df.head(visible_count)
    
    # Create columns
    cols = st.columns(columns_count)
    
    # Display products
    for idx, (row_idx, row) in enumerate(df_display.iterrows()):
        col = cols[idx % columns_count]
        
        with col:
            render_product_card(row, row_idx, language)
            st.markdown("---")  # Separator between products

# ----------------- Product Detail Modal -----------------
@st.dialog("Product Details", width="large")
def show_product_modal(product, language="Kurdish"):
    """
    Display detailed product information in a modal dialog
    """
    # Get language-specific labels
    if language == "Kurdish":
        tag_label = "بابەتی"
        color_label = "ڕەنگی"
        material_label = "پێکهاتەی"
    else:
        tag_label = "عنصر"
        color_label = "الالوان"
        material_label = "مكون من"
    
    # Extract data
    tags = product.get(tag_label, "N/A")
    colors = product.get(color_label, "N/A")
    materials = product.get(material_label, "N/A")
    url = product.get("URL", "")
    
    # Display media
    col1, col2 = st.columns([2, 1])
    
    with col1:
        try:
            if is_youtube(url):
                video_id = extract_youtube_id(url)
                if video_id:
                    embed_url = f"https://www.youtube.com/embed/{video_id}"
                    st.video(embed_url)
            elif is_image(url):
                if is_valid_url(url):
                    st.image(url, use_container_width=True)
        except Exception as e:
            st.error(f"Error loading media: {e}")
    
    with col2:
        st.markdown("### 📋 Details")
        st.markdown(f"**{tag_label}:** {tags}")
        st.markdown(f"**{color_label}:** {colors}")
        st.markdown(f"**{material_label}:** {materials}")
        
        if url and is_valid_url(url):
            st.link_button("🔗 Open Link", url, use_container_width=True)
    
    # Additional info if available
    st.markdown("---")
    
    # Display all other fields
    st.markdown("### 📊 All Information")
    info_data = {}
    for key, value in product.items():
        if key not in [tag_label, color_label, material_label, "URL"] and pd.notna(value):
            info_data[key] = value
    
    if info_data:
        for key, value in info_data.items():
            st.text(f"{key}: {value}")
    else:
        st.info("No additional information available")
    
    # Close button
    if st.button("✖️ Close", use_container_width=True):
        st.session_state.selected_product = None
        st.rerun()

# ----------------- Favorites View -----------------
def display_favorites(df, language="Kurdish", columns_count=3):
    """
    Display only favorited products
    """
    if not st.session_state.favorites:
        st.info("💔 No favorites yet. Click the heart icon on products to add them!")
        return
    
    favorite_indices = list(st.session_state.favorites)
    favorites_df = df.loc[df.index.isin(favorite_indices)]
    
    if favorites_df.empty:
        st.warning("⚠️ Favorited products no longer exist in the dataset")
        return
    
    st.markdown(f"### ❤️ Your Favorites ({len(favorites_df)} items)")
    
    display_products(
        favorites_df,
        language=language,
        columns_count=columns_count,
        visible_count=len(favorites_df)
    )

# ----------------- Empty State Component -----------------
def show_empty_state(message="No products found", icon="📭"):
    """Display a friendly empty state"""
    st.markdown(f"""
    <div style='
        text-align: center;
        padding: 4rem 2rem;
        color: #666;
    '>
        <div style='font-size: 4rem; margin-bottom: 1rem;'>{icon}</div>
        <h3>{message}</h3>
        <p>Try adjusting your filters or search terms</p>
    </div>
    """, unsafe_allow_html=True)

# Import pandas for type checking
import pandas as pd
