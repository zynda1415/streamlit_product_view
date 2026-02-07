import streamlit as st
from settings import load_google_sheet, load_analytics, save_analytics, increment_stat, load_app_data, save_app_data
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

# ----------------- Mobile-First CSS -----------------
st.markdown("""
<style>
    /* CRITICAL: Force mobile buttons to stay horizontal */
    @media (max-width: 768px) {
        /* Container adjustments */
        .block-container { 
            padding: 0.5rem !important; 
        }
        
        /* Force 3-column layout even on mobile */
        div[data-testid="column"] {
            flex: 1 1 33% !important;
            max-width: 33.33% !important;
            min-width: 30% !important;
            padding: 0 0.2rem !important;
        }
        
        /* Button sizing for mobile */
        .stButton > button {
            width: 100% !important;
            padding: 0.5rem 0.2rem !important;
            font-size: 1.3rem !important;
            min-width: 0 !important;
            white-space: nowrap !important;
        }
        
        /* Stats display - force horizontal */
        .product-stats-mobile {
            display: flex !important;
            flex-direction: row !important;
            justify-content: center !important;
            gap: 0.3rem !important;
            flex-wrap: nowrap !important;
            white-space: nowrap !important;
        }
    }
    
    /* Desktop and general styles */
    html {
        scroll-behavior: smooth;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.4);
    }
    
    .stSpinner > div {
        border-color: #4CAF50 transparent transparent transparent;
    }
    
    .element-container {
        transition: transform 0.2s ease;
    }
    
    .stTextInput > div > div > input {
        border-radius: 8px;
    }
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
    }
    
    .stMarkdown {
        margin-bottom: 1rem;
    }
    
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
    
    @keyframes heartBeat {
        0%, 100% { transform: scale(1); }
        25% { transform: scale(1.2); }
        50% { transform: scale(1.1); }
        75% { transform: scale(1.15); }
    }
    
    .favorite-active {
        animation: heartBeat 0.5s ease;
    }
    
    /* Column selector styling */
    .column-selector-btn {
        margin: 2px !important;
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

if "columns_count" not in st.session_state:
    st.session_state.columns_count = 2

if "language" not in st.session_state:
    app_data = load_app_data()
    st.session_state.language = app_data.get("language", "Kurdish")

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
    pass

# ----------------- Sidebar -----------------
# Logo
try:
    st.sidebar.image("fallback_logo.png", use_container_width=True)
except Exception:
    st.sidebar.markdown("## 🏢 Asankar")

st.sidebar.markdown("---")

# Language selector IN SIDEBAR
st.sidebar.markdown("### 🌐 Language / زمان")
language_options = ["Kurdish", "Arabic"]
language_labels = {
    "Kurdish": "کوردی (Kurdish)",
    "Arabic": "عربی (Arabic)"
}

selected_language = st.sidebar.radio(
    "Choose language",
    language_options,
    index=language_options.index(st.session_state.language),
    format_func=lambda x: language_labels[x],
    label_visibility="collapsed",
    help="Switch between Kurdish and Arabic"
)

# Save language preference if changed
if selected_language != st.session_state.language:
    st.session_state.language = selected_language
    app_data = load_app_data()
    app_data["language"] = selected_language
    save_app_data(app_data)
    st.rerun()

language = st.session_state.language

st.sidebar.markdown("---")

# ----------------- Column Selector (1-7) -----------------
st.sidebar.markdown("### 📊 View Layout")
st.sidebar.markdown("**Columns:**")

# Create two rows of buttons
col_row1 = st.sidebar.columns(4)
col_row2 = st.sidebar.columns(3)

for i in range(1, 8):
    if i <= 4:
        col = col_row1[i-1]
    else:
        col = col_row2[i-5]
    
    with col:
        button_type = "primary" if st.session_state.columns_count == i else "secondary"
        if st.button(
            f"{i}",
            key=f"col_{i}",
            use_container_width=True,
            type=button_type
        ):
            st.session_state.columns_count = i
            st.rerun()

columns_count = st.session_state.columns_count

st.sidebar.markdown("---")

# ----------------- Load Google Sheet -----------------
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
    filtered_df = filtered_df.iloc[::-1]
elif sort_option == "oldest":
    pass

# ----------------- Statistics -----------------
total_products = len(df)
filtered_products = len(filtered_df)

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

# Analytics metrics
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
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.markdown("# 📦 Asankar Products")
with col2:
    st.metric("Showing", min(st.session_state.visible_count, len(filtered_df)))
with col3:
    st.metric("Total", filtered_products)

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
