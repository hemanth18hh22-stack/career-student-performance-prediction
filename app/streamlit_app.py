import os
import sys
import time
from pathlib import Path
import streamlit as st

# Ensure project root is in sys.path so app.views imports resolve seamlessly
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from app.views.styles import inject, inject_base_styles
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

# 3. Handle Google Authentication & Session State
is_google_authenticated = False
if hasattr(st, "user"):
    try:
        is_google_authenticated = bool(st.user.get("is_logged_in", False))
    except Exception:
        is_google_authenticated = False

if is_google_authenticated:
    # Synchronize identity information from Google OIDC
    google_name = st.user.get("name")
    google_email = st.user.get("email")
    if not google_name and google_email:
        google_name = google_email.split("@")[0].replace(".", " ").title()

    st.session_state["user"] = {
        "name": google_name or "Student",
        "email": google_email or "",
        "picture": st.user.get("picture", ""),
        "auth_provider": "google",
    }

    # Auto-route authenticated Google users away from auth cards
    current_scr = st.session_state.get("screen")
    if current_scr in [None, "login", "signup", "otp"]:
        target_screen = "analyzer" if st.session_state.get("profile") else "onboarding"
        st.session_state["screen"] = target_screen

        # Short centered message while deciding which screen to show
        inject(
            """
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 55vh; text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 0.75rem; animation: heroLogoFloat 2s ease-in-out infinite;">🌅</div>
                <h3 style="font-size: 1.4rem; font-weight: 600; color: #1F2937; margin: 0 0 0.4rem 0;">Signing you in...</h3>
                <p style="font-size: 0.92rem; color: #6B7280; margin: 0;">Calibrating your student workspace</p>
            </div>
            """
        )
        time.sleep(0.3)
        st.rerun()

# 4. Initialize Session State Defaults
query_screen = st.query_params.get("screen")
if "screen" not in st.session_state:
    if query_screen and query_screen in ["login", "signup", "otp", "onboarding", "analyzer"]:
        st.session_state["screen"] = query_screen
    else:
        st.session_state["screen"] = "login"

if "user" not in st.session_state:
    st.session_state["user"] = {}
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
