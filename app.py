import streamlit as st
from settings import load_google_sheet, sidebar_controls
from display import display_products, show_product_modal
from rotlogo import add_rotated_background_logo
import pandas as pd

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

# Columns selector
st.sidebar.markdown("### 📊 View Settings")
columns_count = st.sidebar.slider(
    "📱 Columns",
    min_value=1,
    max_value=4,
    value=2,
    help="Adjust number of columns for your screen"
)

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

st.sidebar.markdown("---")
st.sidebar.markdown("### 📈 Statistics")
st.sidebar.metric("Total Products", total_products)
if tag_search or selected_tags or selected_colors or selected_materials:
    st.sidebar.metric("Filtered Products", filtered_products)
st.sidebar.metric("Favorites", len(st.session_state.favorites))

# Reset filters button
if st.sidebar.button("🔄 Reset All Filters", use_container_width=True):
    st.session_state.visible_count = 12
    st.rerun()

# ----------------- Main content -----------------
# Header with stats
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.markdown("# 📦 Asankar Products")
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
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem 0;'>
    <p>Made with ❤️ by Asankar | Powered by Streamlit</p>
</div>
""", unsafe_allow_html=True)
