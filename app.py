import streamlit as st
from settings import load_google_sheet, sidebar_controls, load_analytics, save_analytics, increment_stat
from display import display_products, show_product_modal
from rotlogo import add_rotated_background_logo
import pandas as pd
import base64

# Helper function for icon display
def get_base64_image(image_path):
    """Convert image to base64 for inline display"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return ""

# ----------------- Page config -----------------
st.set_page_config(
    page_title="Asankar Products",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Asankar Product Preview - Modern product showcase application"
    }
)

# ----------------- Custom CSS for better UX -----------------
st.markdown("""
<style>
    /* Mobile optimizations */
    @media (max-width: 768px) {
        .block-container { 
            padding: 1rem !important; 
        }
        .stButton > button {
            width: 100%;
        }
    }
    
    /* Smooth scrolling */
    html {
        scroll-behavior: smooth;
    }
    
    /* Better button styling */
    .stButton > button {
        background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.4);
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border-color: #4CAF50 transparent transparent transparent;
    }
    
    /* Card-like appearance for products */
    .element-container {
        transition: transform 0.2s ease;
    }
    
    /* Search input styling */
    .stTextInput > div > div > input {
        border-radius: 8px;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
    }
    
    /* Better spacing */
    .stMarkdown {
        margin-bottom: 1rem;
    }
    
    /* Fade-in animation for products */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .element-container {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Heart animation */
    @keyframes heartBeat {
        0%, 100% { transform: scale(1); }
        25% { transform: scale(1.2); }
        50% { transform: scale(1.1); }
        75% { transform: scale(1.15); }
    }
    
    .favorite-active {
        animation: heartBeat 0.5s ease;
    }
    
    /* View mode icon buttons */
    div[data-testid="column"] button {
        background: transparent !important;
        border: 2px solid #e0e0e0 !important;
        border-radius: 8px !important;
        padding: 8px !important;
        min-height: 50px !important;
        transition: all 0.3s ease !important;
    }
    
    div[data-testid="column"] button:hover {
        border-color: #4CAF50 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 8px rgba(76, 175, 80, 0.2) !important;
    }
    
    /* Active state for selected view mode */
    .view-mode-active {
        border-color: #4CAF50 !important;
        background: rgba(76, 175, 80, 0.1) !important;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- Initialize session state -----------------
if "visible_count" not in st.session_state:
    st.session_state.visible_count = 12

if "favorites" not in st.session_state:
    st.session_state.favorites = set()

if "selected_product" not in st.session_state:
    st.session_state.selected_product = None

if "sort_option" not in st.session_state:
    st.session_state.sort_option = "None"

if "filter_tags" not in st.session_state:
    st.session_state.filter_tags = []

# Initialize analytics in session state
if "analytics_loaded" not in st.session_state:
    st.session_state.analytics = load_analytics()
    st.session_state.analytics_loaded = True

# ----------------- Add rotated background logo -----------------
try:
    add_rotated_background_logo(
        logo_path="background_logo.png",
        rotation=-25,
        opacity=0.05,
        size="300px"
    )
except Exception as e:
    # Silently fail if logo doesn't exist
    pass

# ----------------- Sidebar -----------------
language = sidebar_controls()

# Initialize columns_count in session state
if "columns_count" not in st.session_state:
    st.session_state.columns_count = 2

# View mode selector with icons
st.sidebar.markdown("### 📊 View Mode")

# View mode configuration
view_modes = {
    "List View": {"icon": "icons/list-view.png", "columns": 1},
    "Single": {"icon": "icons/single-view.png", "columns": 1},
    "Grid 2×2": {"icon": "icons/grid-2.png", "columns": 2},
    "Grid 3×3": {"icon": "icons/grid-3.png", "columns": 3}
}

# Create 4 columns for icons
icon_cols = st.sidebar.columns(4)

for idx, (mode_name, mode_data) in enumerate(view_modes.items()):
    with icon_cols[idx]:
        # Check if this is the active mode
        is_active = st.session_state.columns_count == mode_data['columns']
        
        # Create clickable container
        try:
            # Read and encode icon
            with open(mode_data['icon'], "rb") as img_file:
                icon_b64 = base64.b64encode(img_file.read()).decode()
            
            # Create custom HTML button with icon
            button_html = f"""
            <div style="text-align: center; margin-bottom: 8px;">
                <div style="
                    border: 2px solid {'#4CAF50' if is_active else '#e0e0e0'};
                    background: {'rgba(76, 175, 80, 0.1)' if is_active else 'transparent'};
                    border-radius: 8px;
                    padding: 8px;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    min-height: 50px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                ">
                    <img src="data:image/png;base64,{icon_b64}" 
                         style="width: 32px; height: 32px; opacity: {'1.0' if is_active else '0.5'};">
                </div>
            </div>
            """
            st.markdown(button_html, unsafe_allow_html=True)
            
            # Invisible button for functionality
            if st.button("​", key=f"view_{idx}", help=mode_name, use_container_width=True):
                st.session_state.columns_count = mode_data['columns']
                st.rerun()
                
        except Exception as e:
            # Fallback text button
            if st.button(mode_name[:1], key=f"view_{idx}_fb", help=mode_name, use_container_width=True):
                st.session_state.columns_count = mode_data['columns']
                st.rerun()

columns_count = st.session_state.columns_count

# ----------------- Load Google Sheet with error handling -----------------
try:
    with st.spinner("🔄 Loading products..."):
        df = load_google_sheet()
    
    if df.empty:
        st.warning("⚠️ No products found in the database.")
        st.stop()
        
except Exception as e:
    st.error(f"❌ Error loading products: {str(e)}")
    st.info("💡 Please check your Google Sheets configuration in secrets.toml")
    st.stop()

# ----------------- Filtering Section -----------------
st.sidebar.markdown("### 🔍 Filters")

# Tag search filter
tag_search = st.sidebar.text_input(
    "🏷️ Search",
    placeholder="Search by tag, color, or material...",
    help="Type to search across all product fields"
)

# Get unique tags, colors, and materials for filter options
language_suffix = "Kurdish" if language == "Kurdish" else "Arabic"
tag_col = "بابەتی" if language == "Kurdish" else "عنصر"
color_col = "ڕەنگی" if language == "Kurdish" else "الالوان"
material_col = "پێکهاتەی" if language == "Kurdish" else "مكون من"

# Multi-select filters
all_tags = set()
all_colors = set()
all_materials = set()

for col in [tag_col, color_col, material_col]:
    if col in df.columns:
        for val in df[col].dropna():
            items = str(val).split(',')
            for item in items:
                item = item.strip()
                if item:
                    if col == tag_col:
                        all_tags.add(item)
                    elif col == color_col:
                        all_colors.add(item)
                    else:
                        all_materials.add(item)

# Filter by tags
if all_tags:
    selected_tags = st.sidebar.multiselect(
        f"🏷️ {tag_col}",
        sorted(list(all_tags)),
        help="Filter by specific tags"
    )
else:
    selected_tags = []

# Filter by colors
if all_colors:
    selected_colors = st.sidebar.multiselect(
        f"🎨 {color_col}",
        sorted(list(all_colors)),
        help="Filter by specific colors"
    )
else:
    selected_colors = []

# Filter by materials
if all_materials:
    selected_materials = st.sidebar.multiselect(
        f"🧵 {material_col}",
        sorted(list(all_materials)),
        help="Filter by specific materials"
    )
else:
    selected_materials = []

# ----------------- Sorting Section -----------------
st.sidebar.markdown("### 🔀 Sort By")
sort_options = {
    "None": "Default",
    "newest": "🆕 Newest First",
    "oldest": "📅 Oldest First"
}

sort_option = st.sidebar.radio(
    "Sort products",
    list(sort_options.keys()),
    format_func=lambda x: sort_options[x],
    label_visibility="collapsed"
)

# ----------------- Apply filters -----------------
filtered_df = df.copy()

# Text search filter
if tag_search:
    mask = filtered_df.apply(
        lambda r: tag_search.lower() in " ".join(r.astype(str)).lower(), 
        axis=1
    )
    filtered_df = filtered_df[mask]
    # Track search
    increment_stat("total_searches")

# Tag filter
if selected_tags and tag_col in filtered_df.columns:
    mask = filtered_df[tag_col].apply(
        lambda x: any(tag in str(x) for tag in selected_tags)
    )
    filtered_df = filtered_df[mask]

# Color filter
if selected_colors and color_col in filtered_df.columns:
    mask = filtered_df[color_col].apply(
        lambda x: any(color in str(x) for color in selected_colors)
    )
    filtered_df = filtered_df[mask]

# Material filter
if selected_materials and material_col in filtered_df.columns:
    mask = filtered_df[material_col].apply(
        lambda x: any(material in str(x) for material in selected_materials)
    )
    filtered_df = filtered_df[mask]

# ----------------- Apply sorting -----------------
if sort_option == "newest":
    filtered_df = filtered_df.iloc[::-1]  # Reverse order
elif sort_option == "oldest":
    pass  # Keep original order

# ----------------- Statistics -----------------
total_products = len(df)
filtered_products = len(filtered_df)

# Get analytics stats
analytics = st.session_state.analytics
total_likes = analytics.get("total_likes", 0)
total_views = analytics.get("total_views", 0)
total_clicks = analytics.get("total_clicks", 0)
total_link_visits = analytics.get("total_link_visits", 0)
total_searches = analytics.get("total_searches", 0)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📈 Statistics")
st.sidebar.metric("Total Products", total_products)
if tag_search or selected_tags or selected_colors or selected_materials:
    st.sidebar.metric("Filtered Products", filtered_products)
st.sidebar.metric("Favorites", len(st.session_state.favorites))

# Analytics metrics in expander (Reset button removed)
with st.sidebar.expander("📊 Analytics"):
    st.metric("Total Likes", total_likes)
    st.metric("Total Views", total_views)
    st.metric("Total Clicks", total_clicks)
    st.metric("Link Visits", total_link_visits)
    st.metric("Searches", total_searches)

# Reset filters button
if st.sidebar.button("🔄 Reset All Filters", use_container_width=True):
    st.session_state.visible_count = 12
    st.rerun()

# ----------------- Main content -----------------
# Header with stats (removed "📦 Asankar Products" title)
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.markdown("")  # Empty space where title was
with col2:
    st.metric("Showing", min(st.session_state.visible_count, len(filtered_df)))
with col3:
    st.metric("Total", filtered_products)

# Display message if filtered
if filtered_products < total_products:
    st.info(f"🔍 Showing {filtered_products} of {total_products} products (filtered)")

# Display products
if filtered_df.empty:
    st.warning("😕 No products match your filters. Try adjusting your search criteria.")
else:
    display_products(
        filtered_df,
        language=language,
        columns_count=columns_count,
        visible_count=st.session_state.visible_count
    )
    
    # Load more button with better UX
    if st.session_state.visible_count < len(filtered_df):
        remaining = len(filtered_df) - st.session_state.visible_count
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(f"⬇️ Load {min(12, remaining)} More Products", use_container_width=True):
                st.session_state.visible_count += 12
                st.rerun()
    else:
        st.success("✅ All products loaded!")

# ----------------- Product Modal -----------------
if st.session_state.selected_product is not None:
    show_product_modal(
        st.session_state.selected_product,
        language
    )

# ----------------- Footer -----------------
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: #666; padding: 2rem 0;'>
    <p>Made with ❤️ by Asankar | Powered by Streamlit</p>
    <p style='font-size: 0.8rem;'>
        👁️ {total_views:,} views | 
        ❤️ {total_likes:,} likes | 
        🔗 {total_link_visits:,} link visits
    </p>
</div>
""", unsafe_allow_html=True)
