"""
🎨 Modern Animation Library for Asankar Product Preview App
Contains the best 10 professional animations for enhanced user experience
"""

import streamlit as st

# ============================================================================
# 1. FADE-IN ANIMATION FOR PRODUCT CARDS
# ============================================================================

def add_fade_in_animation():
    """
    Smooth fade-in effect for product cards as they appear.
    Creates a professional, smooth entrance animation.
    """
    st.markdown("""
    <style>
        /* Fade-in animation for product cards */
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
            animation: fadeIn 0.6s ease-out;
            animation-fill-mode: both;
        }
        
        /* Stagger animation for multiple cards */
        .element-container:nth-child(1) { animation-delay: 0.1s; }
        .element-container:nth-child(2) { animation-delay: 0.2s; }
        .element-container:nth-child(3) { animation-delay: 0.3s; }
        .element-container:nth-child(4) { animation-delay: 0.4s; }
        .element-container:nth-child(5) { animation-delay: 0.5s; }
        .element-container:nth-child(6) { animation-delay: 0.6s; }
    </style>
    """, unsafe_allow_html=True)


# ============================================================================
# 2. CARD HOVER EFFECT WITH LIFT & SHADOW
# ============================================================================

def add_card_hover_effect():
    """
    Smooth lift effect with expanding shadow on hover.
    Makes cards feel interactive and responsive.
    """
    st.markdown("""
    <style>
        /* Card hover effect */
        .element-container {
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border-radius: 12px;
        }
        
        .element-container:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
            z-index: 10;
        }
        
        /* Smooth image zoom on card hover */
        .element-container:hover img {
            transform: scale(1.05);
            transition: transform 0.3s ease;
        }
        
        .element-container img {
            transition: transform 0.3s ease;
        }
    </style>
    """, unsafe_allow_html=True)


# ============================================================================
# 3. BUTTON RIPPLE EFFECT
# ============================================================================

def add_button_ripple_effect():
    """
    Material Design ripple effect on buttons.
    Provides clear visual feedback on clicks.
    """
    st.markdown("""
    <style>
        /* Button ripple animation */
        @keyframes ripple {
            0% {
                transform: scale(0);
                opacity: 1;
            }
            100% {
                transform: scale(2.5);
                opacity: 0;
            }
        }
        
        .stButton > button {
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(76, 175, 80, 0.3);
        }
        
        .stButton > button:active {
            transform: translateY(0px);
        }
        
        .stButton > button::after {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.5);
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }
        
        .stButton > button:active::after {
            width: 300px;
            height: 300px;
        }
    </style>
    """, unsafe_allow_html=True)


# ============================================================================
# 4. SKELETON LOADING SCREEN
# ============================================================================

def add_skeleton_loading():
    """
    Elegant skeleton screen with shimmer effect during loading.
    Better perceived performance than spinners.
    """
    st.markdown("""
    <style>
        /* Skeleton loading animation */
        @keyframes shimmer {
            0% {
                background-position: -1000px 0;
            }
            100% {
                background-position: 1000px 0;
            }
        }
        
        .skeleton {
            background: linear-gradient(
                90deg,
                #f0f0f0 25%,
                #e0e0e0 50%,
                #f0f0f0 75%
            );
            background-size: 1000px 100%;
            animation: shimmer 2s infinite;
            border-radius: 8px;
        }
        
        /* Loading state styles */
        .stSpinner > div {
            border-top-color: #4CAF50 !important;
            animation: spin 0.8s cubic-bezier(0.5, 0, 0.5, 1) infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
    """, unsafe_allow_html=True)


# ============================================================================
# 5. SMOOTH SCROLL ANIMATIONS
# ============================================================================

def add_smooth_scroll():
    """
    Smooth scrolling behavior throughout the app.
    Creates a more polished, native-app feel.
    """
    st.markdown("""
    <style>
        /* Smooth scrolling */
        html {
            scroll-behavior: smooth;
        }
        
        /* Scroll fade-in effect */
        @keyframes scrollFadeIn {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Custom scrollbar animation */
        ::-webkit-scrollbar {
            width: 10px;
            transition: all 0.3s ease;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, #4CAF50, #45a049);
            border-radius: 10px;
            transition: background 0.3s ease;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(180deg, #45a049, #3d8b40);
        }
    </style>
    """, unsafe_allow_html=True)


# ============================================================================
# 6. HEART FAVORITE ANIMATION
# ============================================================================

def add_favorite_heart_animation():
    """
    Bouncy heart animation when favoriting products.
    Adds delightful micro-interaction feedback.
    """
    st.markdown("""
    <style>
        /* Heart bounce animation */
        @keyframes heartBeat {
            0%, 100% {
                transform: scale(1);
            }
            10%, 30% {
                transform: scale(0.9);
            }
            20%, 40%, 60%, 80% {
                transform: scale(1.1);
            }
            50%, 70% {
                transform: scale(1.05);
            }
        }
        
        /* Apply to favorite buttons */
        button[kind="secondary"]:active {
            animation: heartBeat 0.6s ease;
        }
        
        /* Pulse effect on hover */
        @keyframes pulse {
            0%, 100% {
                opacity: 1;
            }
            50% {
                opacity: 0.7;
            }
        }
        
        button[kind="secondary"]:hover {
            animation: pulse 1.5s infinite;
        }
    </style>
    """, unsafe_allow_html=True)


# ============================================================================
# 7. MODAL SLIDE-IN ANIMATION
# ============================================================================

def add_modal_animation():
    """
    Smooth slide-in animation for modals/dialogs.
    Professional entrance and exit animations.
    """
    st.markdown("""
    <style>
        /* Modal slide-in from bottom */
        @keyframes slideInUp {
            from {
                transform: translateY(100%);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }
        
        /* Modal background fade */
        @keyframes fadeInBackground {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }
        
        /* Apply to Streamlit dialog */
        [data-testid="stDialog"] {
            animation: slideInUp 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        [data-testid="stDialog"]::backdrop {
            animation: fadeInBackground 0.3s ease;
            backdrop-filter: blur(4px);
        }
        
        /* Smooth close animation */
        [data-testid="stDialog"].closing {
            animation: slideInUp 0.3s cubic-bezier(0.4, 0, 0.2, 1) reverse;
        }
    </style>
    """, unsafe_allow_html=True)


# ============================================================================
# 8. GRADIENT BACKGROUND ANIMATION
# ============================================================================

def add_animated_gradient_background():
    """
    Subtle animated gradient background.
    Creates modern, dynamic atmosphere.
    """
    st.markdown("""
    <style>
        /* Animated gradient background */
        @keyframes gradientShift {
            0% {
                background-position: 0% 50%;
            }
            50% {
                background-position: 100% 50%;
            }
            100% {
                background-position: 0% 50%;
            }
        }
        
        .stApp {
            background: linear-gradient(
                -45deg,
                #f8f9fa,
                #e9ecef,
                #f1f3f5,
                #ffffff
            );
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
        }
        
        /* Subtle overlay pattern */
        .stApp::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                repeating-linear-gradient(
                    45deg,
                    transparent,
                    transparent 10px,
                    rgba(255, 255, 255, 0.03) 10px,
                    rgba(255, 255, 255, 0.03) 20px
                );
            pointer-events: none;
            z-index: 0;
        }
    </style>
    """, unsafe_allow_html=True)


# ============================================================================
# 9. TOAST NOTIFICATION ANIMATION
# ============================================================================

def add_toast_notification_animation():
    """
    Slide-in toast notifications for success/error messages.
    Non-intrusive feedback animations.
    """
    st.markdown("""
    <style>
        /* Toast slide-in from right */
        @keyframes slideInRight {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        /* Toast fade-out */
        @keyframes fadeOut {
            from {
                opacity: 1;
            }
            to {
                opacity: 0;
                transform: translateX(100%);
            }
        }
        
        /* Apply to Streamlit alerts */
        .stAlert {
            animation: slideInRight 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            border-left: 4px solid;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        
        /* Success alert - green */
        .stAlert[data-baseweb="notification"][kind="success"] {
            border-left-color: #4CAF50;
            background: linear-gradient(90deg, #e8f5e9 0%, #ffffff 100%);
        }
        
        /* Error alert - red */
        .stAlert[data-baseweb="notification"][kind="error"] {
            border-left-color: #f44336;
            background: linear-gradient(90deg, #ffebee 0%, #ffffff 100%);
        }
        
        /* Info alert - blue */
        .stAlert[data-baseweb="notification"][kind="info"] {
            border-left-color: #2196F3;
            background: linear-gradient(90deg, #e3f2fd 0%, #ffffff 100%);
        }
        
        /* Warning alert - orange */
        .stAlert[data-baseweb="notification"][kind="warning"] {
            border-left-color: #ff9800;
            background: linear-gradient(90deg, #fff3e0 0%, #ffffff 100%);
        }
    </style>
    """, unsafe_allow_html=True)


# ============================================================================
# 10. COUNTER BADGE ANIMATION
# ============================================================================

def add_counter_badge_animation():
    """
    Animated counter badges for statistics and notifications.
    Eye-catching number updates.
    """
    st.markdown("""
    <style>
        /* Counter pop animation */
        @keyframes counterPop {
            0% {
                transform: scale(1);
            }
            50% {
                transform: scale(1.2);
            }
            100% {
                transform: scale(1);
            }
        }
        
        /* Number roll animation */
        @keyframes numberRoll {
            0% {
                transform: translateY(-20px);
                opacity: 0;
            }
            100% {
                transform: translateY(0);
                opacity: 1;
            }
        }
        
        /* Apply to metric components */
        [data-testid="stMetricValue"] {
            animation: numberRoll 0.5s ease-out;
            font-weight: 700;
        }
        
        [data-testid="stMetricDelta"] {
            animation: counterPop 0.6s ease;
        }
        
        /* Badge pulse effect */
        @keyframes badgePulse {
            0%, 100% {
                box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.7);
            }
            50% {
                box-shadow: 0 0 0 10px rgba(76, 175, 80, 0);
            }
        }
        
        /* Metric cards with subtle glow */
        [data-testid="metric-container"] {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            border-radius: 12px;
            padding: 1rem;
            border: 1px solid rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
        }
        
        [data-testid="metric-container"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
            border-color: #4CAF50;
        }
    </style>
    """, unsafe_allow_html=True)


# ============================================================================
# MASTER FUNCTION TO APPLY ALL ANIMATIONS
# ============================================================================

def apply_all_animations():
    """
    Apply all 10 modern animations to the app.
    Call this once in your main app.py file.
    
    Usage:
        from animate import apply_all_animations
        apply_all_animations()
    """
    add_fade_in_animation()              # 1. Fade-in cards
    add_card_hover_effect()              # 2. Card hover lift
    add_button_ripple_effect()           # 3. Button ripple
    add_skeleton_loading()               # 4. Loading skeleton
    add_smooth_scroll()                  # 5. Smooth scrolling
    add_favorite_heart_animation()       # 6. Heart animation
    add_modal_animation()                # 7. Modal slide-in
    add_animated_gradient_background()   # 8. Gradient background
    add_toast_notification_animation()   # 9. Toast notifications
    add_counter_badge_animation()        # 10. Counter badges


# ============================================================================
# INDIVIDUAL ANIMATION FUNCTIONS FOR CUSTOM USE
# ============================================================================

def apply_minimal_animations():
    """
    Apply only essential animations (recommended for performance).
    Good balance between visual appeal and speed.
    """
    add_fade_in_animation()
    add_card_hover_effect()
    add_button_ripple_effect()
    add_smooth_scroll()


def apply_loading_animations():
    """
    Apply only loading-related animations.
    Use when focusing on perceived performance.
    """
    add_skeleton_loading()
    add_smooth_scroll()


def apply_interaction_animations():
    """
    Apply only user interaction animations.
    Best for apps where user feedback is crucial.
    """
    add_button_ripple_effect()
    add_favorite_heart_animation()
    add_card_hover_effect()
    add_toast_notification_animation()


# ============================================================================
# CUSTOM ANIMATION BUILDER
# ============================================================================

def apply_custom_animations(animations_list):
    """
    Apply specific animations based on your preference.
    
    Args:
        animations_list: List of animation numbers (1-10) to apply
        
    Example:
        apply_custom_animations([1, 2, 5, 7])  # Only fade-in, hover, scroll, modal
    """
    animation_functions = {
        1: add_fade_in_animation,
        2: add_card_hover_effect,
        3: add_button_ripple_effect,
        4: add_skeleton_loading,
        5: add_smooth_scroll,
        6: add_favorite_heart_animation,
        7: add_modal_animation,
        8: add_animated_gradient_background,
        9: add_toast_notification_animation,
        10: add_counter_badge_animation
    }
    
    for num in animations_list:
        if num in animation_functions:
            animation_functions[num]()


# ============================================================================
# PERFORMANCE MODE
# ============================================================================

def apply_performance_mode():
    """
    Minimal animations optimized for slower devices.
    Reduces animation complexity while maintaining polish.
    """
    st.markdown("""
    <style>
        /* Simplified animations for performance */
        * {
            animation-duration: 0.2s !important;
            transition-duration: 0.2s !important;
        }
        
        /* Disable complex animations */
        @media (prefers-reduced-motion: reduce) {
            * {
                animation: none !important;
                transition: none !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)


# ============================================================================
# ANIMATION SHOWCASE (FOR TESTING)
# ============================================================================

def show_animation_demo():
    """
    Display a demo of all available animations.
    Use this to preview animations before applying.
    """
    st.markdown("## 🎨 Animation Showcase")
    
    st.markdown("### 1. Fade-in Animation")
    st.info("Cards fade in smoothly as they appear")
    
    st.markdown("### 2. Card Hover Effect")
    st.info("Hover over cards to see lift and shadow")
    
    st.markdown("### 3. Button Ripple")
    st.info("Click buttons to see ripple effect")
    
    st.markdown("### 4. Skeleton Loading")
    st.info("Shimmer effect during data loading")
    
    st.markdown("### 5. Smooth Scroll")
    st.info("Smooth scrolling throughout the app")
    
    st.markdown("### 6. Heart Animation")
    st.info("Hearts bounce when clicking favorite")
    
    st.markdown("### 7. Modal Slide-in")
    st.info("Modals slide up from bottom smoothly")
    
    st.markdown("### 8. Animated Background")
    st.info("Subtle gradient animation in background")
    
    st.markdown("### 9. Toast Notifications")
    st.info("Alerts slide in from the right")
    
    st.markdown("### 10. Counter Badges")
    st.info("Numbers pop and roll when updating")
