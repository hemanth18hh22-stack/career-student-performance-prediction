import os
import time
import joblib
import numpy as np
import pandas as pd
import streamlit as st
from app.views.styles import inject_analyzer_styles


@st.cache_resource
def load_model(model_path="models/performance_model.pkl"):
    """Loads the trained machine learning model from disc."""
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
    return joblib.load(model_path)


def render_analyzer():
    """Renders the existing Student Performance Analyzer prediction UI and logic."""
    inject_analyzer_styles()

    # User status bar if logged in
    user = st.session_state.get("user", {})
    user_name = user.get("name") or user.get("email") or "Student"
    
    col_nav_left, col_nav_right = st.columns([3, 1])
    with col_nav_left:
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-top: 0.2rem;">
                <span style="background: #F3F4F6; color: #374151; font-weight: 600; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.88rem;">
                    👤 Active Session: <strong>{user_name}</strong>
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_nav_right:
        if st.button("🚪 Sign Out", key="analyzer_logout_btn", use_container_width=True):
            st.session_state["user"] = {}
            st.session_state["screen"] = "login"
            st.session_state["otp_code"] = None
            st.session_state["otp_target"] = None
            st.rerun()

    # Header Banner & Subtitle
    st.markdown(
        """
        <div class="header-banner">
            <h1>🎓 Student Performance Analyzer</h1>
            <p>Enter your details below and discover insights about your academic journey! 🚀</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    try:
        model = load_model()
    except Exception as e:
        st.error(f"Error loading model: {e}")
        st.stop()

    # Input Form divided into three section containers with marker spans
    with st.form(key="student_form"):
        # Card 1: Academic Info
        with st.container(border=True):
            st.markdown(
                '<span class="academic-marker"></span>', unsafe_allow_html=True
            )
            st.markdown(
                '<div class="card-title"><span class="icon-badge icon-blue">📖</span>Academic Info</div>',
                unsafe_allow_html=True,
            )
            col1, col2, col3 = st.columns(3)
            with col1:
                study_hours = st.number_input(
                    "⏰ Study Hours (per day)",
                    min_value=1.0,
                    max_value=10.0,
                    value=5.0,
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
            st.markdown(
                '<span class="skills-marker"></span>', unsafe_allow_html=True
            )
            st.markdown(
                '<div class="card-title"><span class="icon-badge icon-green">💻</span>Skills</div>',
                unsafe_allow_html=True,
            )
            col_s1, col_s2, col_s3 = st.columns(3)
            with col_s1:
                python_level = st.selectbox(
                    "🐍 Python Level",
                    options=["Beginner", "Intermediate", "Advanced"],
                )
            with col_s2:
                sql_level = st.selectbox(
                    "🗄️ SQL Level", options=["Beginner", "Intermediate", "Advanced"]
                )
            with col_s3:
                ml_level = st.selectbox(
                    "🤖 ML Level", options=["Beginner", "Intermediate", "Advanced"]
                )

        # Card 3: Learning Habits
        with st.container(border=True):
            st.markdown(
                '<span class="habits-marker"></span>', unsafe_allow_html=True
            )
            st.markdown(
                '<div class="card-title"><span class="icon-badge icon-orange">🎯</span>Learning Habits</div>',
                unsafe_allow_html=True,
            )
            col_h1, col_h2, col_h3 = st.columns(3)
            with col_h1:
                projects_completed = st.number_input(
                    "🚀 Projects Completed",
                    min_value=0,
                    max_value=8,
                    value=2,
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
            st.markdown(
                """
                <div class="result-card result-card-good">
                    <div class="result-title">🎉 Predicted Performance: Good</div>
                    <div class="result-subtitle">Outstanding work! Keep up the excellent effort and consistency!</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        elif predicted_label == "Average":
            st.markdown(
                """
                <div class="result-card result-card-average">
                    <div class="result-title">📊 Predicted Performance: Average</div>
                    <div class="result-subtitle">Solid foundation! A bit more practice can help you reach the top tier.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div class="result-card result-card-poor">
                    <div class="result-title">💪 Predicted Performance: Poor</div>
                    <div class="result-subtitle">Let's build a plan to improve! Focus on consistency and clearing backlogs.</div>
                </div>
                """,
                unsafe_allow_html=True,
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
