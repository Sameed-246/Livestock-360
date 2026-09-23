import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


DATASET_PATH = "ai_engine/dataset/livestock_health.csv"
MODEL_PATH = "ai_engine/disease_model.pkl"


# Load dataset
df = pd.read_csv(
    DATASET_PATH,
    keep_default_na=False
)

print("Dataset loaded successfully!")
print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\nDisease distribution:")
print(df["disease"].value_counts())


# Keep data types consistent
df["vaccination_status"] = df[
    "vaccination_status"
].astype(str)

df["symptoms"] = (
    df["symptoms"]
    .astype(str)
    .str.replace(",", " ", regex=False)
    .str.strip()
)


# Features
features = [
    "animal_type",
    "age",
    "gender",
    "vaccination_status",
    "symptoms",
    "temperature",
]

X = df[features]
y = df["disease"]


# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# Categorical features
categorical_features = [
    "animal_type",
    "gender",
    "vaccination_status",
]


# Numeric features
numeric_features = [
    "age",
    "temperature",
]


# Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            categorical_features,
        ),
        (
            "symptoms",
            TfidfVectorizer(
                lowercase=True,
                ngram_range=(1, 2)
            ),
            "symptoms",
        ),
        (
            "numeric",
            "passthrough",
            numeric_features,
        ),
    ]
)


# Disease classifier
model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    class_weight="balanced"
)


# Complete pipeline
pipeline = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor
        ),
        (
            "model",
            model
        ),
    ]
)


# Train
print("\nTraining disease model...")

pipeline.fit(
    X_train,
    y_train
)

print("Disease model training completed!")


# Evaluate
predictions = pipeline.predict(
    X_test
)

accuracy = accuracy_score(
    y_test,
    predictions
)

print(
    "\nDisease Model Accuracy:",
    round(accuracy * 100, 2),
    "%"
)

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)


# Save model
joblib.dump(
    pipeline,
    MODEL_PATH
)

print("\nDisease model saved successfully!")
print("Location:", MODEL_PATH)