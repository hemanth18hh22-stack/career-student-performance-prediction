# Student Performance & Career Prediction — Runtime Architecture

An interactive, high-level runtime architecture diagram for this repository has been generated using **Archify** and saved as [`architecture_diagram.html`](file:///c:/Users/Hemanth/Desktop/Career-Student-Performance-Prediction/architecture_diagram.html).

---

## 🏗️ Architecture Overview

The repository implements an end-to-end Machine Learning web application composed of two primary operating zones: an **Online Interactive Inference Application** built with Streamlit and an **Offline Synthetic Data & ML Pipeline**.

```
[ Student / User ]
        │ (HTTPS / Form Submit)
        ▼
[ Streamlit Web App ] ──► [ Feature Encoder ] ──► [ RandomForest Model ] ◄── [ Model Loader ]
                                                                                   │ (joblib)
                                                                                   ▼
                                                                        [ Serialized Model .pkl ]
```

---

## 🧩 Core Runtime & Pipeline Components (11 Components)

| Component ID | Label | Sublabel / Module | Category | Primary Function | Source Evidence |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `web_user` | **Student / User** | Web Browser (HTTP/WS) | External | Submits student academic metrics, skills, & habits via form | [streamlit_app.py:L32-L110](file:///c:/Users/Hemanth/Desktop/Career-Student-Performance-Prediction/app/streamlit_app.py#L32-L110) |
| `streamlit_ui` | **Streamlit Web App** | `streamlit_app.py` (:8501) | Frontend | Form layout, custom CSS cards, progress bar, & balloon alerts | [streamlit_app.py:L1-L30](file:///c:/Users/Hemanth/Desktop/Career-Student-Performance-Prediction/app/streamlit_app.py#L1-L30) |
| `ui_preprocessor` | **Inference Feature Encoder** | Ordinal Value Mapper | Security / Logic | Encodes UI dropdown values (`Beginner`/`Intermediate`/`Advanced`, `Low`/`Medium`/`High`) into 1-row DataFrame vector | [streamlit_app.py:L112-L125](file:///c:/Users/Hemanth/Desktop/Career-Student-Performance-Prediction/app/streamlit_app.py#L112-L125) |
| `model_loader` | **Model Cache Loader** | `@st.cache_resource` | Backend | Cached resource loader loading `.pkl` model into memory | [streamlit_app.py:L17-L28](file:///c:/Users/Hemanth/Desktop/Career-Student-Performance-Prediction/app/streamlit_app.py#L17-L28) |
| `rf_classifier` | **Random Forest Model** | 100 Estimator Ensemble | Cloud / ML Model | Multi-class classification (`Poor`, `Average`, `Good`) & confidence probabilities | [train_model.py:L17](file:///c:/Users/Hemanth/Desktop/Career-Student-Performance-Prediction/src/train_model.py#L17), [streamlit_app.py:L127-L138](file:///c:/Users/Hemanth/Desktop/Career-Student-Performance-Prediction/app/streamlit_app.py#L127-L138) |
| `model_store` | **Serialized Model Artifact** | `performance_model.pkl` | Database / Store | Pickled binary storage for trained RandomForestClassifier | [models/performance_model.pkl](file:///c:/Users/Hemanth/Desktop/Career-Student-Performance-Prediction/models/performance_model.pkl) |
| `synthetic_gen` | **Data Synthesizer** | `generate_dataset.py` | Backend | Generates 1,000 synthetic student profiles with weighted scoring & noise | [generate_dataset.py:L6-L106](file:///c:/Users/Hemanth/Desktop/Career-Student-Performance-Prediction/src/generate_dataset.py#L6-L106) |
| `raw_csv` | **Raw Dataset CSV** | `student_data.csv` | Database / Store | File store containing raw generated student records | [student_data.csv](file:///c:/Users/Hemanth/Desktop/Career-Student-Performance-Prediction/data/raw/student_data.csv#L1) |
| `data_preprocessor` | **Data Preprocessor** | `data_preprocessing.py` | Backend | Reads raw CSV, encodes ordinal targets, & splits 80/20 train/test sets | [data_preprocessing.py:L6-L76](file:///c:/Users/Hemanth/Desktop/Career-Student-Performance-Prediction/src/data_preprocessing.py#L6-L76) |
| `processed_csv` | **Processed CSV Splits** | `X_train`, `X_test`, `y_train`, `y_test` | Database / Store | Directory containing preprocessed CSV splits | [X_train.csv](file:///c:/Users/Hemanth/Desktop/Career-Student-Performance-Prediction/data/processed/X_train.csv#L1) |
| `model_trainer` | **Model Trainer & Evaluator** | `train_model.py` | Backend | Fits RandomForest on training split, evaluates test metrics, & serializes model | [train_model.py:L12-L47](file:///c:/Users/Hemanth/Desktop/Career-Student-Performance-Prediction/src/train_model.py#L12-L47) |

---

## 🔒 Trust & Security Boundaries

1. **Client Interface Boundary (`security-group`)**: Separates external end users (Browser Client) from local server execution.
2. **Online Inference Runtime (`region`)**: Encloses the Streamlit Web Application, UI Feature Encoder, Model Cache Loader, and Scikit-Learn Model Instance.
3. **Offline ML Pipeline (`region`)**: Encloses batch data generation, raw storage, dataset preprocessing, train/test split storage, and offline model training.

---

## 📇 Supporting Detail Cards

- **Interactive Web UI & Runtime**: Streamlit web interface running on port 8501 with scoped CSS, Poppins font, custom metric badges, and interactive confidence gauge.
- **Machine Learning Model**: Scikit-Learn `RandomForestClassifier` with 100 decision trees predicting multi-class targets (`Poor`: 0, `Average`: 1, `Good`: 2) along with prediction probabilities.
- **Offline Data & Training Pipeline**: Synthetic dataset generation of 1,000 student rows using normalized weighted attributes, Gaussian random noise ($\sigma = 0.08$), percentile binning, and 80/20 stratified splitting.
- **External Dependencies & Security**: Python dependencies (`streamlit`, `scikit-learn`, `pandas`, `numpy`, `joblib`). Isolated runtime scopes prevent training code from mutating live user sessions.

---

## 📁 Generated Diagram File

The diagram was validated against git commit `4c0c3a05a92ea427875faf8d4799156a20a8e9ce` (**0 errors, 0 warnings**) and rendered into:
- [`architecture_diagram.html`](file:///c:/Users/Hemanth/Desktop/Career-Student-Performance-Prediction/architecture_diagram.html) (opened automatically in your web browser).
