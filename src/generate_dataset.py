import os
import numpy as np
import pandas as pd


def generate_student_dataset(n_samples=1000, seed=42):
    """
    Generates a synthetic dataset of student performance data.

    Parameters:
        n_samples (int): Number of student records to generate.
        seed (int): Random seed for reproducibility.

    Returns:
        pd.DataFrame: DataFrame containing generated student records.
    """
    np.random.seed(seed)

    # 1. Numeric features within specified ranges
    study_hours = np.round(np.random.uniform(1.0, 10.0, n_samples), 1)
    attendance = np.round(np.random.uniform(50.0, 100.0, n_samples), 1)
    previous_marks = np.round(np.random.uniform(35.0, 100.0, n_samples), 1)
    assignment_score = np.round(np.random.uniform(30.0, 100.0, n_samples), 1)
    backlogs = np.random.randint(0, 6, n_samples)  # 0 to 5 inclusive
    projects_completed = np.random.randint(0, 9, n_samples)  # 0 to 8 inclusive

    # 2. Categorical features
    levels = ["Beginner", "Intermediate", "Advanced"]
    frequencies = ["Low", "Medium", "High"]

    python_level = np.random.choice(levels, n_samples, p=[0.4, 0.4, 0.2])
    sql_level = np.random.choice(levels, n_samples, p=[0.4, 0.4, 0.2])
    ml_level = np.random.choice(levels, n_samples, p=[0.5, 0.35, 0.15])

    study_consistency = np.random.choice(frequencies, n_samples, p=[0.3, 0.45, 0.25])
    practice_frequency = np.random.choice(frequencies, n_samples, p=[0.3, 0.45, 0.25])

    # 3. Mappings for score calculation
    level_map = {"Beginner": 0.0, "Intermediate": 0.5, "Advanced": 1.0}
    freq_map = {"Low": 0.0, "Medium": 0.5, "High": 1.0}

    python_num = np.vectorize(level_map.get)(python_level)
    sql_num = np.vectorize(level_map.get)(sql_level)
    ml_num = np.vectorize(level_map.get)(ml_level)
    consistency_num = np.vectorize(freq_map.get)(study_consistency)
    practice_num = np.vectorize(freq_map.get)(practice_frequency)

    # 4. Normalize numeric attributes to [0, 1] for balanced weighting
    study_hours_norm = (study_hours - 1.0) / 9.0
    attendance_norm = (attendance - 50.0) / 50.0
    previous_marks_norm = (previous_marks - 35.0) / 65.0
    assignment_score_norm = (assignment_score - 30.0) / 70.0
    projects_norm = projects_completed / 8.0
    backlogs_norm = backlogs / 5.0  # High backlogs negatively impact performance

    # 5. Weighted composite score
    score = (
        0.18 * study_hours_norm
        + 0.18 * attendance_norm
        + 0.20 * previous_marks_norm
        + 0.14 * assignment_score_norm
        + 0.06 * python_num
        + 0.05 * sql_num
        + 0.05 * ml_num
        + 0.08 * projects_norm
        + 0.06 * consistency_num
        + 0.05 * practice_num
        - 0.20 * backlogs_norm
    )

    # 6. Add Gaussian random noise for non-perfect relationship
    noise = np.random.normal(0, 0.08, n_samples)
    final_score = score + noise

    # 7. Convert continuous score into performance labels: Good, Average, Poor
    p33 = np.percentile(final_score, 33.33)
    p66 = np.percentile(final_score, 66.67)

    performance = []
    for val in final_score:
        if val >= p66:
            performance.append("Good")
        elif val >= p33:
            performance.append("Average")
        else:
            performance.append("Poor")

    # 8. Create DataFrame
    df = pd.DataFrame(
        {
            "study_hours": study_hours,
            "attendance": attendance,
            "previous_marks": previous_marks,
            "assignment_score": assignment_score,
            "backlogs": backlogs,
            "python_level": python_level,
            "sql_level": sql_level,
            "ml_level": ml_level,
            "projects_completed": projects_completed,
            "study_consistency": study_consistency,
            "practice_frequency": practice_frequency,
            "performance": performance,
        }
    )

    return df


if __name__ == "__main__":
    df = generate_student_dataset(n_samples=1000, seed=42)

    output_dir = os.path.join("data", "raw")
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, "student_data.csv")

    df.to_csv(file_path, index=False)
    print(f"Dataset successfully generated and saved to {file_path}\n")

    print("--- First 5 rows ---")
    print(df.head())

    print("\n--- Value counts of performance column ---")
    print(df["performance"].value_counts())
