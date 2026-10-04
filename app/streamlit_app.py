import os
import joblib
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(page_title="Student Performance Analyzer", layout="wide")

st.title("Student Performance Analyzer")
st.write("Input student details below to predict expected academic performance.")


@st.cache_resource
def load_model(model_path="models/performance_model.pkl"):
    if not os.path.exists(model_path):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        alt_path = os.path.join(base_dir, "models", "performance_model.pkl")
        if os.path.exists(alt_path):
            model_path = alt_path
    return joblib.load(model_path)


try:
    model = load_model()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# Input Form
with st.form(key="student_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        study_hours = st.number_input(
            "Study Hours (per day)",
            min_value=1.0,
            max_value=10.0,
            value=5.0,
            step=0.1,
        )
        attendance = st.number_input(
            "Attendance (%)",
            min_value=50.0,
            max_value=100.0,
            value=75.0,
            step=0.1,
        )
        previous_marks = st.number_input(
            "Previous Marks (%)",
            min_value=35.0,
            max_value=100.0,
            value=65.0,
            step=0.1,
        )
        assignment_score = st.number_input(
            "Assignment Score (%)",
            min_value=30.0,
            max_value=100.0,
            value=70.0,
            step=0.1,
        )

    with col2:
        backlogs = st.number_input(
            "Backlogs",
            min_value=0,
            max_value=5,
            value=0,
            step=1,
        )
        python_level = st.selectbox(
            "Python Level",
            options=["Beginner", "Intermediate", "Advanced"],
        )
        sql_level = st.selectbox(
            "SQL Level",
            options=["Beginner", "Intermediate", "Advanced"],
        )
        ml_level = st.selectbox(
            "ML Level",
            options=["Beginner", "Intermediate", "Advanced"],
        )

    with col3:
        projects_completed = st.number_input(
            "Projects Completed",
            min_value=0,
            max_value=8,
            value=2,
            step=1,
        )
        study_consistency = st.selectbox(
            "Study Consistency",
            options=["Low", "Medium", "High"],
        )
        practice_frequency = st.selectbox(
            "Practice Frequency",
            options=["Low", "Medium", "High"],
        )

    submit_button = st.form_submit_button(label="Analyze Student")

if submit_button:
    # Ordinal mappings
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

    st.subheader("Analysis Result")
    if predicted_label == "Good":
        st.success(f"Predicted Performance: **{predicted_label}**")
    elif predicted_label == "Average":
        st.warning(f"Predicted Performance: **{predicted_label}**")
    else:
        st.error(f"Predicted Performance: **{predicted_label}**")
