import os
import pandas as pd
from sklearn.model_selection import train_test_split


def load_and_preprocess_data(
    raw_path="data/raw/student_data.csv",
    output_dir="data/processed",
):
    """
    Loads raw student performance data, encodes ordinal categorical features,
    splits dataset into train and test sets, saves processed CSV splits,
    and prints dataset shapes.

    Parameters:
        raw_path (str): Path to raw CSV file.
        output_dir (str): Directory where processed splits will be saved.

    Returns:
        tuple: (X_train, X_test, y_train, y_test)
    """
    # Resolve raw file path if running from subfolder
    if not os.path.exists(raw_path):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        alt_raw_path = os.path.join(base_dir, "data", "raw", "student_data.csv")
        if os.path.exists(alt_raw_path):
            raw_path = alt_raw_path

    # 1. Load data/raw/student_data.csv with pandas
    df = pd.read_csv(raw_path)

    # 2. Encode ordinal skill level columns: python_level, sql_level, ml_level
    level_mapping = {"Beginner": 0, "Intermediate": 1, "Advanced": 2}
    skill_cols = ["python_level", "sql_level", "ml_level"]
    for col in skill_cols:
        df[col] = df[col].map(level_mapping)

    # 3. Encode ordinal consistency/frequency columns: study_consistency, practice_frequency
    freq_mapping = {"Low": 0, "Medium": 1, "High": 2}
    freq_cols = ["study_consistency", "practice_frequency"]
    for col in freq_cols:
        df[col] = df[col].map(freq_mapping)

    # 4. Encode target column 'performance'
    target_mapping = {"Poor": 0, "Average": 1, "Good": 2}
    df["performance"] = df["performance"].map(target_mapping)

    # 5. Split features (X) and target (y), then split into train/test sets
    X = df.drop(columns=["performance"])
    y = df["performance"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 6. Save processed train/test splits as CSV files in data/processed/
    if not os.path.exists(output_dir) and not os.path.isabs(output_dir):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        alt_output_dir = os.path.join(base_dir, "data", "processed")
        if os.path.exists(os.path.dirname(alt_output_dir)):
            output_dir = alt_output_dir

    os.makedirs(output_dir, exist_ok=True)

    X_train.to_csv(os.path.join(output_dir, "X_train.csv"), index=False)
    X_test.to_csv(os.path.join(output_dir, "X_test.csv"), index=False)
    y_train.to_csv(os.path.join(output_dir, "y_train.csv"), index=False)
    y_test.to_csv(os.path.join(output_dir, "y_test.csv"), index=False)

    # 7. Print shapes of X_train, X_test, y_train, y_test
    print(f"X_train shape: {X_train.shape}")
    print(f"X_test shape: {X_test.shape}")
    print(f"y_train shape: {y_train.shape}")
    print(f"y_test shape: {y_test.shape}")

    return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    load_and_preprocess_data()
