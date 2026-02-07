import streamlit as st
from display import show_logo

def load_data():
    """Return empty dict; no settings now"""
    return {}

def sidebar_logo():
    """Show fallback logo at top of sidebar"""
    show_logo(None, in_sidebar=True)
