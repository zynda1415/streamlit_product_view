import streamlit as st

FALLBACK_LOGO = "fallback_logo.png"

# ----------------- Helpers -----------------
def is_youtube(url: str) -> bool:
    return "youtube.com" in url or "youtu.be" in url

def is_image(url: str) -> bool:
    return any(url.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".webp"])

# ----------------- Display Products -----------------
def display_products(df, language="Kurdish", columns_count=3, visible_count=12):
    """Display products using Streamlit columns (Pinterest style)"""
    if df.empty:
        st.info("No products to display")
        return

    df = df.head(visible_count)
    cols = st.columns(columns_count)

    for idx, row in df.iterrows():
        col = cols[idx % columns_count]

        if language == "Kurdish":
            tags = row.get("Kurdish Tags", "")
            colors = row.get("Kurdish Color Tags", "")
            materials = row.get("Kurdish Material Tags", "")
        else:
            tags = row.get("Arabic Tags", "")
            colors = row.get("Arabic Colors Tags", "")
            materials = row.get("Arabic Material Tags", "")

        url = row.get("URL", "")

        with col:
            try:
                if is_youtube(url):
                    if "youtu.be" in url:
                        video_id = url.split("/")[-1]
                    else:
                        video_id = url.split("v=")[-1].split("&")[0]
                    embed_url = f"https://www.youtube.com/embed/{video_id}"
                    st.video(embed_url)
                elif is_image(url):
                    st.image(url, use_container_width=True)
                else:
                    st.warning("Unsupported media type")
            except Exception:
                st.error("Error loading media")

            st.caption(f"Tags: {tags}\nColors: {colors}\nMaterials: {materials}")
