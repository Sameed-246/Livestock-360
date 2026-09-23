from django.contrib.auth.models import User

from .models import HealthAlert


def create_health_alerts(report):
    """
    Create alerts when a disease report has a high AI risk score.
    """

    if report.risk_score is None:
        return

    risk_score = float(report.risk_score)

    # Only create an urgent alert for high-risk cases.
    if risk_score < 70:
        return

    animal = report.animal

    title = "🚨 High-Risk Livestock Health Alert"

    message = (
        f"Animal {animal.animal_id} ({animal.animal_type}) "
        f"has been classified as high risk with an AI risk score "
        f"of {risk_score:.1f}%. "
        f"Possible condition: "
        f"{report.predicted_disease or 'Under veterinary review'}. "
        f"Veterinary attention is recommended."
    )

    # Alert the farmer who owns the animal.
    HealthAlert.objects.create(
        recipient=animal.owner,
        report=report,
        alert_type='High Risk',
        title=title,
        message=message,
    )

    # Alert all registered veterinarians.
    veterinarians = User.objects.filter(
        groups__name='Veterinarian'
    ).distinct()

    for veterinarian in veterinarians:

        HealthAlert.objects.create(
            recipient=veterinarian,
            report=report,
            alert_type='High Risk',
            title=title,
            message=message,
        )