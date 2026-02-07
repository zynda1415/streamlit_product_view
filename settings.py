import json
import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import time
import os

APP_DATA_FILE = "app_data.json"

# ---------- App data with error handling ----------
def load_app_data():
    """Load persisted app settings from JSON with error handling"""
    try:
        with open(APP_DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Validate data structure
            if not isinstance(data, dict):
                return get_default_app_data()
            return data
    except FileNotFoundError:
        return get_default_app_data()
    except json.JSONDecodeError:
        st.warning("⚠️ Settings file corrupted. Using defaults.")
        return get_default_app_data()
    except Exception as e:
        st.error(f"Error loading settings: {e}")
        return get_default_app_data()

def get_default_app_data():
    """Return default app settings with analytics"""
    return {
        "language": "Kurdish",
        "last_updated": datetime.now().isoformat(),
        "theme": "light",
        "analytics": {
            "total_likes": 0,
            "total_views": 0,
            "total_clicks": 0,
            "total_link_visits": 0,
            "total_searches": 0,
            "product_stats": {}
        }
    }

def save_app_data(data):
    """Save app settings to JSON with error handling"""
    try:
        data["last_updated"] = datetime.now().isoformat()
        with open(APP_DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"❌ Error saving settings: {e}")
        return False

# ---------- Analytics Functions ----------
def load_analytics():
    """Load analytics data from app_data.json"""
    app_data = load_app_data()
    if "analytics" not in app_data:
        app_data["analytics"] = {
            "total_likes": 0,
            "total_views": 0,
            "total_clicks": 0,
            "total_link_visits": 0,
            "total_searches": 0,
            "product_stats": {}
        }
        save_app_data(app_data)
    return app_data["analytics"]

def save_analytics(analytics_data):
    """Save analytics data to app_data.json"""
    app_data = load_app_data()
    app_data["analytics"] = analytics_data
    save_app_data(app_data)

def increment_stat(stat_name, product_id=None):
    """
    Increment a statistics counter
    
    Args:
        stat_name: Name of the stat (e.g., 'total_likes', 'total_views')
        product_id: Optional product ID for product-specific stats
    """
    analytics = load_analytics()
    
    # Increment total stat
    if stat_name in analytics:
        analytics[stat_name] += 1
    else:
        analytics[stat_name] = 1
    
    # Track product-specific stats
    if product_id is not None:
        if "product_stats" not in analytics:
            analytics["product_stats"] = {}
        
        product_id_str = str(product_id)
        if product_id_str not in analytics["product_stats"]:
            analytics["product_stats"][product_id_str] = {
                "likes": 0,
                "views": 0,
                "clicks": 0,
                "link_visits": 0
            }
        
        # Map stat name to product stat
        stat_mapping = {
            "total_likes": "likes",
            "total_views": "views",
            "total_clicks": "clicks",
            "total_link_visits": "link_visits"
        }
        
        if stat_name in stat_mapping:
            product_stat = stat_mapping[stat_name]
            analytics["product_stats"][product_id_str][product_stat] += 1
    
    save_analytics(analytics)
    
    # Update session state
    if "analytics" in st.session_state:
        st.session_state.analytics = analytics

def get_product_stats(product_id):
    """Get statistics for a specific product"""
    analytics = load_analytics()
    product_stats = analytics.get("product_stats", {})
    product_id_str = str(product_id)
    
    return product_stats.get(product_id_str, {
        "likes": 0,
        "views": 0,
        "clicks": 0,
        "link_visits": 0
    })

def get_top_products(stat_type="likes", limit=10):
    """
    Get top products by a specific statistic
    
    Args:
        stat_type: Type of stat ('likes', 'views', 'clicks', 'link_visits')
        limit: Number of top products to return
    """
    analytics = load_analytics()
    product_stats = analytics.get("product_stats", {})
    
    # Sort products by stat
    sorted_products = sorted(
        product_stats.items(),
        key=lambda x: x[1].get(stat_type, 0),
        reverse=True
    )
    
    return sorted_products[:limit]

# ---------- Google Sheet with improved error handling ----------
@st.cache_data(ttl=3600, show_spinner=False)  # Cache for 1 hour
def load_google_sheet():
    """
    Load Google Sheet as a Pandas DataFrame with comprehensive error handling
    Returns: DataFrame with product data
    """
    try:
        # Validate secrets exist
        if "gcp_service_account" not in st.secrets:
            raise ValueError("Missing 'gcp_service_account' in secrets.toml")
        
        if "google_sheet_id" not in st.secrets:
            raise ValueError("Missing 'google_sheet_id' in secrets.toml")
        
        # Setup credentials
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        
        creds = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=scopes
        )
        
        # Authorize and connect
        client = gspread.authorize(creds)
        
        # Get sheet with retry logic
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                sheet = client.open_by_key(st.secrets["google_sheet_id"]).sheet1
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    raise e
        
        # Get all records
        records = sheet.get_all_records()
        
        if not records:
            st.warning("⚠️ Google Sheet is empty")
            return pd.DataFrame()
        
        # Create DataFrame
        df = pd.DataFrame(records)
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Remove empty rows
        df = df.dropna(how='all')
        
        # Validate required columns
        required_cols = ["URL"]
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            st.warning(f"⚠️ Missing columns in sheet: {', '.join(missing_cols)}")
        
        return df
        
    except ValueError as ve:
        st.error(f"❌ Configuration Error: {ve}")
        st.info("💡 Please add the required secrets to your .streamlit/secrets.toml file")
        return pd.DataFrame()
        
    except gspread.exceptions.SpreadsheetNotFound:
        st.error("❌ Google Sheet not found. Please check the sheet ID in secrets.toml")
        return pd.DataFrame()
        
    except gspread.exceptions.APIError as api_err:
        st.error(f"❌ Google Sheets API Error: {api_err}")
        st.info("💡 Please check your service account permissions")
        return pd.DataFrame()
        
    except Exception as e:
        st.error(f"❌ Unexpected error loading data: {e}")
        st.info("💡 Please contact support if this persists")
        return pd.DataFrame()

def refresh_data():
    """Clear cache and reload data"""
    st.cache_data.clear()
    st.success("✅ Data refreshed!")
    st.rerun()

# ---------- Sidebar with enhanced controls ----------
def sidebar_controls():
    """Display enhanced sidebar with logo and language switch"""
    
    # Load settings
    app_data = load_app_data()
    
    # Logo display with fallback
    try:
        st.sidebar.image("fallback_logo.png", use_container_width=True)
    except Exception:
        st.sidebar.markdown("## 🏢 Asankar")
    
    st.sidebar.markdown("---")
    
    # Language selector
    st.sidebar.markdown("### 🌐 Language / زمان")
    language = st.sidebar.radio(
        "Choose language",
        ["Kurdish", "Arabic"],
        index=0 if app_data.get("language", "Kurdish") == "Kurdish" else 1,
        label_visibility="collapsed",
        help="Switch between Kurdish and Arabic"
    )
    
    # Save language preference
    if language != app_data.get("language"):
        app_data["language"] = language
        save_app_data(app_data)
    
    st.sidebar.markdown("---")
    
    # Advanced options in expander
    with st.sidebar.expander("⚙️ Advanced Options"):
        # Refresh data button
        if st.button("🔄 Refresh Data", use_container_width=True):
            refresh_data()
        
        # Export analytics
        if st.button("📊 Export Analytics", use_container_width=True):
            analytics = load_analytics()
            analytics_json = json.dumps(analytics, indent=2, ensure_ascii=False)
            st.download_button(
                label="⬇️ Download Analytics JSON",
                data=analytics_json,
                file_name=f"analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        # Cache info
        st.caption("Data is cached for 1 hour for better performance")
        
        # Show last update time
        if "last_updated" in app_data:
            try:
                last_update = datetime.fromisoformat(app_data["last_updated"])
                st.caption(f"Last updated: {last_update.strftime('%Y-%m-%d %H:%M')}")
            except:
                pass
    
    return language

# ---------- Export functionality ----------
@st.cache_data(ttl=300)
def export_to_csv(df, language):
    """Export filtered data to CSV"""
    try:
        csv = df.to_csv(index=False, encoding='utf-8-sig')
        return csv
    except Exception as e:
        st.error(f"Error exporting data: {e}")
        return None

def show_export_options(df, language):
    """Display export options in sidebar"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📥 Export")
    
    if st.sidebar.button("📄 Export to CSV", use_container_width=True):
        csv = export_to_csv(df, language)
        if csv:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            st.sidebar.download_button(
                label="⬇️ Download CSV",
                data=csv,
                file_name=f"asankar_products_{timestamp}.csv",
                mime="text/csv",
                use_container_width=True
            )
