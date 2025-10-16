import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
import joblib
import numpy as np
import os

# --- Configuration ---
CSV_FILE = "tomato_disease_symptoms_extended.csv"
MODEL_FILE = "tomato_disease_model.pkl"
MIN_SAMPLES_PER_CLASS = 5  # Set the minimum number of rows required for a disease class


def train_and_save_model():
    """
    Loads data, trains a Random Forest Classifier, and saves the model.
    Uses StratifiedKFold for robust accuracy reporting on imbalanced data.
    """
    try:
        # Load data
        df = pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        print(f"Error: {CSV_FILE} not found. Please ensure it is uploaded.")
        return

    # --- NEW: Data Filtering Step ---
    print(f"Original number of samples: {len(df)}")

    # 1. Count the occurrences of each disease
    class_counts = df['disease'].value_counts()

    # 2. Identify classes that meet the minimum sample requirement
    valid_classes = class_counts[class_counts >= MIN_SAMPLES_PER_CLASS].index.tolist()

    # 3. Filter the DataFrame to keep only rows with valid diseases
    df_filtered = df[df['disease'].isin(valid_classes)]

    print(f"Number of disease classes kept: {len(valid_classes)}")
    print(f"Filtered number of samples (min {MIN_SAMPLES_PER_CLASS} rows): {len(df_filtered)}")
    # --- END Data Filtering Step ---

    # Prepare data using the filtered DataFrame
    X = df_filtered.drop("disease", axis=1)
    y = df_filtered["disease"]

    # If all data was filtered out, exit
    if len(df_filtered) == 0:
        print("Error: No diseases met the minimum sample requirement. Cannot train model.")
        return

    # 1. Train Classifier with increased estimators
    print("Training Random Forest Classifier (n_estimators=500)...")
    clf = RandomForestClassifier(n_estimators=500, random_state=42)
    clf.fit(X, y)  # Fit on all data before saving for best final model

    # 2. Perform Stratified Cross-Validation (CV) for robust evaluation
    print("Performing 5-Fold Stratified Cross-Validation for robust accuracy...")
    try:
        # Use StratifiedKFold to handle imbalanced classes gracefully
        cv_splitter = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        cv_scores = cross_val_score(clf, X, y, cv=cv_splitter, scoring='accuracy')

        print(f"Cross-Validation Scores: {cv_scores}")
        print(f"Average CV Accuracy: {np.mean(cv_scores):.4f}")
    except Exception as e:
        print(f"Warning: Could not perform Stratified Cross-Validation. Error: {e}")
        # Fallback to single split test accuracy if CV fails
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        clf_test = RandomForestClassifier(n_estimators=500, random_state=42)
        clf_test.fit(X_train, y_train)
        print(f"Fallback Test Accuracy (80/20 split): {clf_test.score(X_test, y_test):.4f}")

    # 3. Save trained model (using the one fitted on all data)
    joblib.dump(clf, MODEL_FILE)

    print(f"\nModel saved successfully as {MODEL_FILE}!")

    # For debugging: print the feature columns the model expects
    print(f"\nModel Feature Columns ({len(X.columns)}):")
    print(X.columns.tolist())


# Run the training process
if __name__ == "__main__":
    train_and_save_model()
