import os
import sys
from pathlib import Path
import streamlit as st

# Ensure project root is in sys.path so app.views imports resolve seamlessly
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from app.views.styles import inject_base_styles
from app.views.auth import (
    render_login,
    render_signup,
    render_otp,
)
from app.views.onboarding import render_onboarding
from app.views.analyzer import render_analyzer

# 1. Set Page Configuration
st.set_page_config(
    page_title="Student Performance & Career Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 2. Inject Shared Design System CSS
inject_base_styles()

# 3. Initialize Session State Defaults
query_screen = st.query_params.get("screen")
if "screen" not in st.session_state:
    if query_screen and query_screen in ["login", "signup", "otp", "onboarding", "analyzer"]:
        st.session_state["screen"] = query_screen
    else:
        st.session_state["screen"] = "login"

if "user" not in st.session_state:
    st.session_state["user"] = {"name": "Alex Sharma", "email": "alex@example.com"}
if "otp_code" not in st.session_state:
    st.session_state["otp_code"] = "482910"
if "otp_target" not in st.session_state:
    st.session_state["otp_target"] = "alex@example.com"

# Active Screen Routing
current_screen = st.session_state.get("screen", "login")
st.query_params["screen"] = current_screen

if current_screen == "login":
    render_login()
elif current_screen == "signup":
    render_signup()
elif current_screen == "otp":
    render_otp()
elif current_screen == "onboarding":
    render_onboarding()
elif current_screen == "analyzer":
    render_analyzer()
else:
    st.session_state["screen"] = "login"
    st.rerun()
