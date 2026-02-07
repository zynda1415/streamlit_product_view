import streamlit as st

def add_rotated_background_logo(logo_path="background_logo.png", rotation=-30, opacity=0.05, size=300):
    """
    Adds a rotated logo as background using st.image + CSS.
    Works on Streamlit Cloud and mobile.
    """
    try:
        st.image(
            logo_path,
            width=size,
            use_column_width=False,
            output_format="auto",
        )
        st.markdown(f"""
        <style>
        div[data-testid="stImage"] {{
            position: fixed !important;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) rotate({rotation}deg);
            opacity: {opacity};
            z-index: 0;
            pointer-events: none;
        }}
        .stApp > div:first-child {{
            z-index: 1;
        }}
        </style>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"Failed to load background logo: {e}")
