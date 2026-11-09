from pathlib import Path

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
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
from sklearn.preprocessing import OneHotEncoder


BASE_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = (
    BASE_DIR
    / "datasets"
    / "processed"
    / "mastitis_detection.csv"
)

MODEL_PATH = (
    BASE_DIR
    / "ai_engine"
    / "v2"
    / "mastitis_model.pkl"
)


TARGET = "class1"
GROUP = "Cow_ID"

CATEGORICAL_FEATURES = [
    "Breed",
]

NUMERIC_FEATURES = [
    "Months after giving birth",
    "Previous_Mastits_status",
    "IUFL",
    "EUFL",
    "IUFR",
    "EUFR",
    "IURL",
    "EURL",
    "IURR",
    "EURR",
    "Temperature",
    "Hardness",
    "Pain",
    "Milk_visibility",
]


def main():
    print("Loading mastitis dataset...")

    df = pd.read_csv(DATA_PATH)

    print("Rows:", len(df))
    print("Cows:", df[GROUP].nunique())

    features = (
        CATEGORICAL_FEATURES
        + NUMERIC_FEATURES
    )

    X = df[features]
    y = df[TARGET]
    groups = df[GROUP]

    print("\nTarget distribution:")
    print(y.value_counts().sort_index())

    # ---------------------------------------------------------
    # Cow-level stratified split
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

    train_cows = groups.iloc[train_idx]
    test_cows = groups.iloc[test_idx]

    print("\nTraining rows:", len(X_train))
    print("Testing rows:", len(X_test))

    print(
        "Training cows:",
        train_cows.nunique()
    )

    print(
        "Testing cows:",
        test_cows.nunique()
    )

    overlap = set(train_cows) & set(test_cows)

    print(
        "Cow overlap:",
        len(overlap)
    )

    # ---------------------------------------------------------
    # Preprocessing
    # ---------------------------------------------------------
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                Pipeline(
                    steps=[
                        (
                            "imputer",
                            SimpleImputer(
                                strategy="most_frequent"
                            ),
                        ),
                        (
                            "encoder",
                            OneHotEncoder(
                                handle_unknown="ignore"
                            ),
                        ),
                    ]
                ),
                CATEGORICAL_FEATURES,
            ),
            (
                "numeric",
                SimpleImputer(
                    strategy="median"
                ),
                NUMERIC_FEATURES,
            ),
        ]
    )

    # ---------------------------------------------------------
    # Model
    # ---------------------------------------------------------
    model = RandomForestClassifier(
        n_estimators=300,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1,
    )

    pipeline = Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor,
            ),
            (
                "model",
                model,
            ),
        ]
    )

    print("\nTraining V2 mastitis model...")

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
    print("V2 MASTITIS MODEL RESULTS")
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
    # Save separate V2 model
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