import streamlit as st
import pandas as pd

# ---------------- PRODUCT DISPLAY ----------------
def show_products(products, media_type="All", tag_search=""):
    if not products:
        st.info("No products to display")
        return

    df = pd.DataFrame(products)
    filtered_df = df.copy()

    if tag_search:
        filtered_df = filtered_df[
            filtered_df.apply(
                lambda row: tag_search.lower() in " ".join(row.astype(str)).lower(),
                axis=1
            )
        ]

    cols = st.columns(3)
    for index, row in filtered_df.iterrows():
        url = row["URL"]
        url_lower = url.lower()
        url_base = url_lower.split("?")[0]  # remove query parameters

        col = cols[index % 3]

        with col:
            # Images
            if url_base.endswith((".jpg", ".jpeg", ".png", ".webp")):
                if media_type in ["All", "Images"]:
                    st.image(url, use_container_width=True)

            # Videos
            elif url_base.endswith((".mp4", ".mov", ".webm")) or "youtu.be" in url or "youtube.com/watch" in url:
                if media_type in ["All", "Videos"]:
                    st.video(url)

            else:
                st.warning(f"Unsupported file type: {url}")

            st.caption(
                f"**Kurdish:** {row.get('Kurdish Tags', '')}  \n"
                f"**Arabic:** {row.get('Arabic Tags', '')}"
            )
