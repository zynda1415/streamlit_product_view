import streamlit as st

def show_header(logo_url):
    if logo_url:
        st.image(logo_url, use_container_width=True)

def show_products(products):
    if not products:
        st.info("No products to display")
        return

    for p in products:
        st.markdown(f"### {p['title']}")
        if "video" in p:
            st.video(p["video"])
