def display_products(products, num_columns=3):
    """
    Pinterest-style grid with unique keys
    """
    if "preview_url" not in st.session_state:
        st.session_state.preview_url = None

    if not products:
        st.info("No products to display")
        return

    for i in range(0, len(products), num_columns):
        row = products[i:i + num_columns]
        cols = st.columns(num_columns, gap="medium")
        for j, (col, product) in enumerate(zip(cols, row)):
            with col:
                # Pass unique index as suffix for keys
                display_single_product(product, key_suffix=f"{i+j}")

    # Modal preview
    if st.session_state.preview_url:
        st.markdown("---")
        st.subheader("🔍 Preview")
        url = st.session_state.preview_url
        if is_youtube(url):
            st.video(url)
        elif is_image(url):
            st.image(url, use_container_width=True)
        st.button("Close Preview", on_click=lambda: clear_preview(), key="close_preview")

def display_single_product(product, key_suffix=""):
    """Show one product thumbnail + title with unique keys"""
    title = product.get("title", "")
    media = product.get("media", "")

    if is_youtube(media):
        st.video(media, start_time=0)
    elif is_image(media):
        # Make key unique by combining title + suffix
        if st.button(f"🔍 {title}", key=f"{media}_{key_suffix}"):
            st.session_state.preview_url = media
        st.image(media, use_container_width=True)
    else:
        st.warning("Unsupported media type")

    st.markdown(f"<p style='text-align:center'>{title}</p>", unsafe_allow_html=True)
