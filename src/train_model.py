import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

try:
    from src.data_preprocessing import load_and_preprocess_data
except ImportError:
    from data_preprocessing import load_and_preprocess_data


def main():
    # 1 & 2. Load and preprocess data to get train/test splits
    X_train, X_test, y_train, y_test = load_and_preprocess_data()

    # 3. Train RandomForestClassifier (n_estimators=100, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # 4. Evaluate on X_test: print accuracy_score, classification_report, and confusion_matrix
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    matrix = confusion_matrix(y_test, y_pred)

    print("\n--- Model Evaluation ---")
    print(f"Accuracy Score: {accuracy:.4f}\n")
    print("Classification Report:")
    print(report)
    print("\nConfusion Matrix:")
    print(matrix)

    # 5. Save the trained model to models/performance_model.pkl using joblib
    models_dir = "models"
    if not os.path.exists(models_dir) and not os.path.isabs(models_dir):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        alt_models_dir = os.path.join(base_dir, "models")
        if os.path.exists(os.path.dirname(alt_models_dir)):
            models_dir = alt_models_dir

    os.makedirs(models_dir, exist_ok=True)
    model_path = os.path.join(models_dir, "performance_model.pkl")

    joblib.dump(model, model_path)

    # 6. Print a final confirmation message once the model is saved
    print(f"\nModel successfully saved to {model_path}")


if __name__ == "__main__":
    main()
