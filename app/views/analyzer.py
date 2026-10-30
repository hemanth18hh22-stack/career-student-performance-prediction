import os
import time
import joblib
import numpy as np
import pandas as pd
import streamlit as st
from app.views.styles import inject, inject_analyzer_styles


_IS_MODEL_LOADED = False


@st.cache_resource
def load_model(model_path="models/performance_model.pkl"):
    """Loads the trained machine learning model from disc."""
    global _IS_MODEL_LOADED
    if not os.path.exists(model_path):
        # 3 directories up (root from app/views/analyzer.py)
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        alt_path = os.path.join(root_dir, "models", "performance_model.pkl")
        if os.path.exists(alt_path):
            model_path = alt_path
        else:
            # 2 directories up (from app/analyzer.py if moved)
            alt_path2 = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models", "performance_model.pkl")
            if os.path.exists(alt_path2):
                model_path = alt_path2
    m = joblib.load(model_path)
    _IS_MODEL_LOADED = True
    return m


def is_model_loaded() -> bool:
    """Returns True if the performance model has already been loaded into memory."""
    return _IS_MODEL_LOADED


def render_analyzer():
    """Renders the existing Student Performance Analyzer prediction UI and logic."""
    inject_analyzer_styles()

    # Pre-fill defaults from profile if available
    profile = st.session_state.get("profile", {})
    skills_profile = profile.get("skills", {})

    # 1. Study hours: weekly_hours / 7 clamped to 1.0 - 10.0
    raw_weekly = profile.get("weekly_hours")
    if raw_weekly is not None:
        try:
            calc_daily = float(raw_weekly) / 7.0
            default_study_hours = float(round(max(1.0, min(10.0, calc_daily)), 1))
        except (ValueError, TypeError):
            default_study_hours = 5.0
    else:
        default_study_hours = 5.0

    # 2. Skill levels: from skills named exactly "Python", "SQL", "Machine Learning" if selected (else Beginner)
    skill_level_options = ["Beginner", "Intermediate", "Advanced"]

    py_skill = skills_profile.get("Python", "Beginner")
    default_py_idx = (
        skill_level_options.index(py_skill)
        if py_skill in skill_level_options
        else 0
    )

    sql_skill = skills_profile.get("SQL", "Beginner")
    default_sql_idx = (
        skill_level_options.index(sql_skill)
        if sql_skill in skill_level_options
        else 0
    )

    ml_skill = skills_profile.get("Machine Learning", "Beginner")
    default_ml_idx = (
        skill_level_options.index(ml_skill)
        if ml_skill in skill_level_options
        else 0
    )

    # 3. Projects completed: from projects
    raw_projects = profile.get("projects")
    if raw_projects is not None:
        try:
            default_projects = int(max(0, min(8, int(raw_projects))))
        except (ValueError, TypeError):
            default_projects = 2
    else:
        default_projects = 2

    # User status bar if logged in
    user = st.session_state.get("user", {})
    user_name = user.get("name") or user.get("email") or "Student"
    user_picture = user.get("picture", "")
    avatar_html = (
        f'<img src="{user_picture}" style="width: 22px; height: 22px; border-radius: 50%; vertical-align: middle; margin-right: 6px;" />'
        if user_picture
        else '👤 '
    )
    
    col_nav_left, col_nav_right = st.columns([3, 1])
    with col_nav_left:
        inject(
            f"""
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-top: 0.2rem;">
                <span style="background: #F3F4F6; color: #374151; font-weight: 600; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.88rem; display: inline-flex; align-items: center;">
                    {avatar_html}Active Session: <strong style="margin-left: 4px;">{user_name}</strong>
                </span>
            </div>
            """
        )
    with col_nav_right:
        if st.button("🚪 Sign Out", key="analyzer_logout_btn", use_container_width=True):
            st.session_state.clear()
            st.session_state["screen"] = "login"
            try:
                if hasattr(st, "user") and st.user.get("is_logged_in", False):
                    st.logout()
            except Exception:
                pass
            st.rerun()

    # Welcome banner if just finished onboarding
    if st.session_state.get("profile_just_completed"):
        st.session_state["profile_just_completed"] = False
        inject(
            f"""
            <div style="background: linear-gradient(135deg, #ECFDF5 0%, #EDE9FE 100%); border: 1.5px solid #A7F3D0; border-radius: 16px; padding: 1.2rem 1.6rem; margin-bottom: 1.5rem; box-shadow: 0 4px 15px rgba(16, 185, 129, 0.1);">
                <div style="font-weight: 700; color: #065F46; font-size: 1.15rem; margin-bottom: 0.25rem;">
                    🎉 Welcome to your dashboard, {user_name}!
                </div>
                <div style="color: #047857; font-size: 0.92rem;">
                    Your academic profile and skill proficiencies from onboarding have been loaded below. Every field stays editable.
                </div>
            </div>
            """
        )

    # Header Banner & Subtitle
    inject(
        """
        <div class="header-banner">
            <h1>🎓 Student Performance Analyzer</h1>
            <p>Enter your details below and discover insights about your academic journey! 🚀</p>
        </div>
        """
    )

    try:
        if not is_model_loaded():
            with st.spinner("Preparing your dashboard..."):
                model = load_model()
        else:
            model = load_model()
    except Exception as e:
        st.error(f"Error loading model: {e}")
        st.stop()

    # Input Form divided into three section containers with marker spans
    with st.form(key="student_form"):
        # Card 1: Academic Info
        with st.container(border=True):
            inject('<span class="academic-marker"></span>')
            inject(
                '<div class="card-title"><span class="icon-badge icon-blue">📖</span>Academic Info</div>'
            )
            col1, col2, col3 = st.columns(3)
            with col1:
                study_hours = st.number_input(
                    "⏰ Study Hours (per day)",
                    min_value=1.0,
                    max_value=10.0,
                    value=default_study_hours,
                    step=0.1,
                )
                attendance = st.number_input(
                    "📅 Attendance (%)",
                    min_value=50.0,
                    max_value=100.0,
                    value=75.0,
                    step=0.1,
                )
            with col2:
                previous_marks = st.number_input(
                    "📈 Previous Marks (%)",
                    min_value=35.0,
                    max_value=100.0,
                    value=65.0,
                    step=0.1,
                )
                assignment_score = st.number_input(
                    "📝 Assignment Score (%)",
                    min_value=30.0,
                    max_value=100.0,
                    value=70.0,
                    step=0.1,
                )
            with col3:
                backlogs = st.number_input(
                    "⚠️ Backlogs", min_value=0, max_value=5, value=0, step=1
                )

        # Card 2: Skills
        with st.container(border=True):
            inject('<span class="skills-marker"></span>')
            inject(
                '<div class="card-title"><span class="icon-badge icon-green">💻</span>Skills</div>'
            )
            col_s1, col_s2, col_s3 = st.columns(3)
            with col_s1:
                python_level = st.selectbox(
                    "🐍 Python Level",
                    options=skill_level_options,
                    index=default_py_idx,
                )
            with col_s2:
                sql_level = st.selectbox(
                    "🗄️ SQL Level",
                    options=skill_level_options,
                    index=default_sql_idx,
                )
            with col_s3:
                ml_level = st.selectbox(
                    "🤖 ML Level",
                    options=skill_level_options,
                    index=default_ml_idx,
                )

        # Card 3: Learning Habits
        with st.container(border=True):
            inject('<span class="habits-marker"></span>')
            inject(
                '<div class="card-title"><span class="icon-badge icon-orange">🎯</span>Learning Habits</div>'
            )
            col_h1, col_h2, col_h3 = st.columns(3)
            with col_h1:
                projects_completed = st.number_input(
                    "🚀 Projects Completed",
                    min_value=0,
                    max_value=8,
                    value=default_projects,
                    step=1,
                )
            with col_h2:
                study_consistency = st.selectbox(
                    "🔄 Study Consistency", options=["Low", "Medium", "High"]
                )
            with col_h3:
                practice_frequency = st.selectbox(
                    "🏋️ Practice Frequency", options=["Low", "Medium", "High"]
                )

        submit_button = st.form_submit_button(label="🔍 Analyze Student")

    # Analysis Trigger
    if submit_button:
        with st.spinner("Analyzing student profile..."):
            time.sleep(1.0)

        # Ordinal mappings (exact same as original logic)
        level_map = {"Beginner": 0, "Intermediate": 1, "Advanced": 2}
        freq_map = {"Low": 0, "Medium": 1, "High": 2}

        # Build single-row DataFrame matching exact feature column order
        input_df = pd.DataFrame(
            [
                {
                    "study_hours": study_hours,
                    "attendance": attendance,
                    "previous_marks": previous_marks,
                    "assignment_score": assignment_score,
                    "backlogs": backlogs,
                    "python_level": level_map[python_level],
                    "sql_level": level_map[sql_level],
                    "ml_level": level_map[ml_level],
                    "projects_completed": projects_completed,
                    "study_consistency": freq_map[study_consistency],
                    "practice_frequency": freq_map[practice_frequency],
                }
            ]
        )

        # Predict using loaded model
        prediction = model.predict(input_df)[0]
        target_map = {0: "Poor", 1: "Average", 2: "Good"}
        predicted_label = target_map.get(prediction, "Unknown")

        # Calculate prediction confidence
        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(input_df)[0]
            confidence = float(np.max(probabilities))
        else:
            confidence = 1.0

        # Display large animated-style result card
        if predicted_label == "Good":
            st.balloons()
            inject(
                """
                <div class="result-card result-card-good">
                    <div class="result-title">🎉 Predicted Performance: Good</div>
                    <div class="result-subtitle">Outstanding work! Keep up the excellent effort and consistency!</div>
                </div>
                """
            )
        elif predicted_label == "Average":
            inject(
                """
                <div class="result-card result-card-average">
                    <div class="result-title">📊 Predicted Performance: Average</div>
                    <div class="result-subtitle">Solid foundation! A bit more practice can help you reach the top tier.</div>
                </div>
                """
            )
        else:
            inject(
                """
                <div class="result-card result-card-poor">
                    <div class="result-title">💪 Predicted Performance: Poor</div>
                    <div class="result-subtitle">Let's build a plan to improve! Focus on consistency and clearing backlogs.</div>
                </div>
                """
            )

        # Confidence Progress Bar
        st.markdown("### 📊 Analysis Confidence & Summary")
        st.write(f"**Model Prediction Confidence:** `{confidence * 100:.1f}%`")
        st.progress(confidence)

        # Key Metrics Cards Overview
        st.markdown("#### Key Metrics Overview")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("⏰ Study Hours", f"{study_hours} hrs/day")
        m2.metric("📅 Attendance", f"{attendance:.1f}%")
        m3.metric("📈 Previous Marks", f"{previous_marks:.1f}%")
        m4.metric("⚠️ Backlogs", f"{backlogs}")
