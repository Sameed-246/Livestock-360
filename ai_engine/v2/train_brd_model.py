from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import Pipeline


BASE_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = (
    BASE_DIR
    / "datasets"
    / "processed"
    / "brd_early_warning.csv"
)

MODEL_PATH = (
    BASE_DIR
    / "ai_engine"
    / "v2"
    / "brd_early_warning_model.pkl"
)


FEATURES = [
    "Temp",
    "Breath",
    "Temp_score",
    "Gender",
    "agefeeder",
    "Fecal",
    "Milk_Intake",
    "Lying_time",
    "Lying_bouts",
    "lying_daily",
]

TARGET = "brd_early_warning"
GROUP = "IdSeq"


def main():
    print("Loading processed BRD dataset...")

    df = pd.read_csv(DATA_PATH)

    print("Rows:", len(df))
    print("Animals:", df[GROUP].nunique())

    X = df[FEATURES]
    y = df[TARGET]
    groups = df[GROUP]

    print("\nOverall target distribution:")
    print(y.value_counts().sort_index())

    # ---------------------------------------------------------
    # Animal-level stratified split
    # ---------------------------------------------------------
    splitter = StratifiedGroupKFold(
        n_splits=5,
        shuffle=True,
        random_state=42,
    )

    train_idx, test_idx = next(
        splitter.split(X, y, groups)
    )

    X_train = X.iloc[train_idx]
    X_test = X.iloc[test_idx]

    y_train = y.iloc[train_idx]
    y_test = y.iloc[test_idx]

    train_groups = groups.iloc[train_idx]
    test_groups = groups.iloc[test_idx]

    print("\nTraining rows:", len(X_train))
    print("Testing rows:", len(X_test))

    print(
        "Training animals:",
        train_groups.nunique()
    )

    print(
        "Testing animals:",
        test_groups.nunique()
    )

    overlap = set(train_groups) & set(test_groups)

    print(
        "Animal overlap:",
        len(overlap)
    )

    print("\nTraining target distribution:")
    print(y_train.value_counts().sort_index())

    print("\nTesting target distribution:")
    print(y_test.value_counts().sort_index())

    # ---------------------------------------------------------
    # Model pipeline
    # ---------------------------------------------------------
    pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy="median"
                ),
            ),
            (
                "model",
                RandomForestClassifier(
                    n_estimators=300,
                    random_state=42,
                    class_weight="balanced",
                    n_jobs=-1,
                ),
            ),
        ]
    )

    print("\nTraining V2 BRD early-warning model...")

    pipeline.fit(
        X_train,
        y_train,
    )

    print("Training completed!")

    # ---------------------------------------------------------
    # Evaluation
    # ---------------------------------------------------------
    predictions = pipeline.predict(X_test)

    probabilities = pipeline.predict_proba(
        X_test
    )[:, 1]

    accuracy = accuracy_score(
        y_test,
        predictions,
    )

    balanced_accuracy = balanced_accuracy_score(
        y_test,
        predictions,
    )

    roc_auc = roc_auc_score(
        y_test,
        probabilities,
    )

    print("\n==============================")
    print("V2 BRD MODEL RESULTS")
    print("==============================")

    print(
        "Accuracy:",
        round(accuracy * 100, 2),
        "%",
    )

    print(
        "Balanced accuracy:",
        round(balanced_accuracy * 100, 2),
        "%",
    )

    print(
        "ROC-AUC:",
        round(roc_auc, 4),
    )

    print("\nConfusion matrix:")
    print(
        confusion_matrix(
            y_test,
            predictions,
        )
    )

    print("\nClassification report:")
    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0,
        )
    )

    # ---------------------------------------------------------
    # Save V2 model only
    # ---------------------------------------------------------
    MODEL_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    joblib.dump(
        pipeline,
        MODEL_PATH,
    )

    print("\nV2 model saved to:")
    print(MODEL_PATH)


if __name__ == "__main__":
    main()