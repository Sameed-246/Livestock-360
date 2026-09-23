from pathlib import Path
import joblib
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent

RISK_MODEL_PATH = BASE_DIR / "model.pkl"
DISEASE_MODEL_PATH = BASE_DIR / "disease_model.pkl"


def load_model(path):
    if not path.exists():
        return None

    return joblib.load(path)


def prepare_input(data):

    symptoms = str(
        data.get("symptoms", "")
    ).replace(",", " ").strip()

    return pd.DataFrame([{
        "animal_type": data.get(
            "animal_type",
            "Cattle"
        ),
        "age": float(
            data.get("age", 0)
        ),
        "gender": data.get(
            "gender",
            "Female"
        ),
        "vaccination_status": str(
            int(
                bool(
                    data.get(
                        "vaccination_status",
                        False
                    )
                )
            )
        ),
        "symptoms": symptoms,
        "temperature": float(
            data.get("temperature", 0)
        ),
    }])


def calculate_risk_score(
    probability_map,
    risk_level
):

    high = probability_map.get(
        "High",
        0
    )

    medium = probability_map.get(
        "Medium",
        0
    )

    low = probability_map.get(
        "Low",
        0
    )

    # Calculate probability-based score
    score = (
        (low * 10)
        + (medium * 50)
        + (high * 90)
    )

    score = float(score)

    # Keep score consistent with
    # the model's predicted risk level.
    if risk_level == "High":

        if score < 70:
            score = 70 + (
                high * 30
            )

    elif risk_level == "Medium":

        if score < 40:
            score = 40

        elif score >= 70:
            score = 69.99

    elif risk_level == "Low":

        if score >= 40:
            score = 39.99

    # Keep score between 0 and 100
    score = max(
        0,
        min(score, 100)
    )

    return float(
        round(
        score,
        2
    )
)


def get_recommendation(
    risk_level
):

    if risk_level == "High":

        return (
            "High-risk case detected. "
            "Veterinary examination is "
            "strongly recommended."
        )

    if risk_level == "Medium":

        return (
            "Moderate-risk case detected. "
            "Veterinary examination and "
            "monitoring are recommended."
        )

    if risk_level == "Low":

        return (
            "Low-risk case detected. "
            "Continue regular monitoring "
            "and preventive care."
        )

    return (
        "Risk level could not be determined. "
        "Veterinary review is recommended."
    )


def predict_health_risk(data):

    risk_model = load_model(
        RISK_MODEL_PATH
    )

    disease_model = load_model(
        DISEASE_MODEL_PATH
    )

    if risk_model is None:

        return {
            "risk_score": None,
            "risk_level": "Unknown",
            "predicted_disease": (
                "AI model not available"
            ),
            "disease_confidence": None,
            "recommendation": (
                "Your report has been received. "
                "A veterinarian should review "
                "the case."
            ),
        }

    input_data = prepare_input(
        data
    )

    # Predict risk level
    predicted_risk = risk_model.predict(
        input_data
    )[0]

    # Get risk probabilities
    probability_map = {}

    if hasattr(
        risk_model,
        "predict_proba"
    ):

        probabilities = (
            risk_model.predict_proba(
                input_data
            )[0]
        )

        classes = risk_model.classes_

        probability_map = dict(
            zip(
                classes,
                probabilities
            )
        )

    # Calculate consistent numeric score
    risk_score = calculate_risk_score(
        probability_map,
        predicted_risk
    )

    # Default disease result
    predicted_disease = (
        "No specific condition detected"
    )

    disease_confidence = None

    # Predict disease
    if disease_model is not None:

        predicted_disease = (
            disease_model.predict(
                input_data
            )[0]
        )

        if hasattr(
            disease_model,
            "predict_proba"
        ):

            disease_probabilities = (
                disease_model.predict_proba(
                    input_data
                )[0]
            )

            disease_classes = (
                disease_model.classes_
            )

            disease_probability_map = dict(
                zip(
                    disease_classes,
                    disease_probabilities
                )
            )

            disease_confidence = round(
                float(
                    disease_probability_map.get(
                        predicted_disease,
                        0
                    ) * 100
                ),
                2
            )

    recommendation = get_recommendation(
        predicted_risk
    )

    return {
        "risk_score": risk_score,
        "risk_level": predicted_risk,
        "predicted_disease": predicted_disease,
        "disease_confidence": disease_confidence,
        "recommendation": recommendation,
    }