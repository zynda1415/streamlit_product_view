import streamlit as st
import os

def add_rotated_background_logo(
    logo_path="background_logo.png", 
    rotation=-30, 
    opacity=0.05, 
    size="300px"
):
    """
    Adds a rotated logo as background watermark using CSS.
    Works on Streamlit Cloud and mobile devices.
    
    Args:
        logo_path: Path to the logo image file
        rotation: Rotation angle in degrees (negative for counter-clockwise)
        opacity: Opacity value (0.0 to 1.0)
        size: Size of the logo (CSS units like '300px', '20vw', etc.)
    """
    # Validate inputs
    if not isinstance(rotation, (int, float)):
        rotation = -30
    
    if not isinstance(opacity, (int, float)) or not (0 <= opacity <= 1):
        opacity = 0.05
    
    if not isinstance(size, str):
        size = "300px"
    
    # Check if logo file exists
    if not os.path.exists(logo_path):
        # Silently fail - background logo is optional
        return
    
    try:
        # Create a container for the background logo
        st.markdown(f"""
        <style>
            /* Background logo watermark */
            .background-logo {{
                position: fixed !important;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%) rotate({rotation}deg);
                opacity: {opacity};
                z-index: -1;
                pointer-events: none;
                width: {size};
                height: auto;
            }}
            
            /* Ensure main content is above watermark */
            .main .block-container {{
                position: relative;
                z-index: 1;
            }}
            
            /* Mobile optimizations */
            @media (max-width: 768px) {{
                .background-logo {{
                    width: 200px;
                }}
            }}
            
            /* Hide during print */
            @media print {{
                .background-logo {{
                    display: none;
                }}
            }}
        </style>
        """, unsafe_allow_html=True)
        
        # Add the logo image
        # Using data URL to embed the image would be more reliable but more complex
        # For now, we'll use st.image with custom CSS
        
        # Create image element with custom class
        st.markdown(f"""
        <img src="app/static/{logo_path}" class="background-logo" alt="Background Logo">
        """, unsafe_allow_html=True)
        
    except Exception as e:
        # Silently fail - watermark is cosmetic
        pass

def add_custom_css():
    """
    Add general custom CSS improvements for the app
    """
    st.markdown("""
    <style>
        /* Smooth transitions */
        * {
            transition: all 0.2s ease;
        }
        
        /* Better scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #888;
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #555;
        }
        
        /* Card hover effects */
        .element-container:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        /* Better image loading */
        img {
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Loading states */
        .stSpinner {
            text-align: center;
        }
        
        /* Alert styling */
        .stAlert {
            border-radius: 8px;
            border-left: 4px solid;
        }
        
        /* Info alert */
        .stAlert[data-baseweb="notification"] {
            background-color: #e3f2fd;
        }
    </style>
    """, unsafe_allow_html=True)
