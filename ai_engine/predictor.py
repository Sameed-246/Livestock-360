from pathlib import Path
import joblib
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent

RISK_MODEL_PATH = BASE_DIR / "model.pkl"
DISEASE_MODEL_PATH = BASE_DIR / "disease_model.pkl"


def load_model(path):
    if not path.exists():
        return None

    try:
        return joblib.load(path)
    except Exception as e:
        print(f"Warning: Failed to load model from {path}: {e}")
        return None


def prepare_input(data):

    symptoms = str(
        data.get("symptoms", "")
    ).replace(",", " ").strip()

    age_val = data.get("age")
    try:
        age = float(age_val) if age_val not in (None, "") else 0.0
    except (ValueError, TypeError):
        age = 0.0

    temp_val = data.get("temperature")
    try:
        temp = float(temp_val) if temp_val not in (None, "") else 0.0
    except (ValueError, TypeError):
        temp = 0.0

    return pd.DataFrame([{
        "animal_type": data.get(
            "animal_type",
            "Cattle"
        ),
        "age": age,
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
        "temperature": temp,
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
    try:
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
                    "AI assessment unavailable — veterinarian review required"
                ),
                "disease_confidence": None,
                "recommendation": (
                    "AI assessment unavailable — veterinarian review required. "
                    "Case has been queued for priority clinical review."
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

            try:
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
            except Exception as e:
                print(f"Warning: Disease sub-model prediction failed: {e}")

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

    except Exception as exc:
        print(f"Warning: Health risk prediction encountered error: {exc}")
        return {
            "risk_score": None,
            "risk_level": "Unknown",
            "predicted_disease": (
                "AI assessment unavailable — veterinarian review required"
            ),
            "disease_confidence": None,
            "recommendation": (
                "AI assessment unavailable — veterinarian review required. "
                "Case has been queued for priority clinical review."
            ),
        }