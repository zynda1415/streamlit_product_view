import streamlit as st
import pandas as pd

def convert_youtube_url(url):
    if "youtu.be/" in url:
        video_id = url.split("/")[-1].split("?")[0]
        return f"https://www.youtube.com/watch?v={video_id}"
    return url

def get_columns():
    if st.session_state.get("mobile_view", True):
        return st.columns(1)
    return st.columns(3)

def show_products(records, media_type="All", search=""):
    if not records:
        st.info("No products to display")
        return

    df = pd.DataFrame(records)

    if search:
        df = df[df.apply(
            lambda r: search.lower() in " ".join(r.astype(str)).lower(),
            axis=1
        )]

    cols = get_columns()

    for i, row in df.iterrows():
        url = row.get("URL", "")
        url_base = url.lower().split("?")[0]

        col = cols[i % len(cols)]
        with col:

            # IMAGE
            if url_base.endswith((".jpg", ".jpeg", ".png", ".webp")):
                if media_type in ["All", "Images"]:
                    st.image(url, use_container_width=True)

            # VIDEO
            elif (
                url_base.endswith((".mp4", ".mov", ".webm")) or
                "youtube.com/watch" in url or
                "youtu.be" in url
            ):
                if media_type in ["All", "Videos"]:
                    st.video(convert_youtube_url(url))

            else:
                st.warning("Unsupported media")

            st.caption(f"🟡 {row.get('Kurdish Tags','')}")
            st.caption(f"🟢 {row.get('Arabic Tags','')}")
