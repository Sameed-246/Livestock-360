import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# ---------------------------------------
# 1. Load dataset
# ---------------------------------------

DATASET_PATH = "ai_engine/dataset/livestock_health.csv"
MODEL_PATH = "ai_engine/model.pkl"

df = pd.read_csv(DATASET_PATH)

print("Dataset loaded successfully!")
print("Rows:", len(df))
print("Columns:", len(df.columns))


# ---------------------------------------
# 2. Prepare the data
# ---------------------------------------

# Convert missing disease values to "None"
df["disease"] = df["disease"].fillna("None")

# Convert vaccination status to text
df["vaccination_status"] = df["vaccination_status"].astype(str)

features = [
    "animal_type",
    "age",
    "gender",
    "vaccination_status",
    "symptoms",
    "temperature",
]

X = df[features]

# We will train the model to predict risk level
y = df["risk_level"]


# ---------------------------------------
# 3. Split training and testing data
# ---------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))


# ---------------------------------------
# 4. Preprocess categorical data
# ---------------------------------------

categorical_features = [
    "animal_type",
    "gender",
    "vaccination_status",
    "symptoms",
]

numeric_features = [
    "age",
    "temperature",
]

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features,
        ),
        (
            "numeric",
            "passthrough",
            numeric_features,
        ),
    ]
)


# ---------------------------------------
# 5. Create Random Forest model
# ---------------------------------------

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)


# ---------------------------------------
# 6. Create complete ML pipeline
# ---------------------------------------

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model),
    ]
)


# ---------------------------------------
# 7. Train the model
# ---------------------------------------

print("\nTraining model...")

pipeline.fit(X_train, y_train)

print("Model training completed!")


# ---------------------------------------
# 8. Evaluate the model
# ---------------------------------------

predictions = pipeline.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\nModel Accuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:")
print(classification_report(y_test, predictions, zero_division=0))


# ---------------------------------------
# 9. Save trained model
# ---------------------------------------

joblib.dump(pipeline, MODEL_PATH)

print("\nModel saved successfully!")
print("Location:", MODEL_PATH)