from django.db import models
from django.contrib.auth.models import User

from reports.models import DiseaseReport


class HealthAlert(models.Model):

    ALERT_TYPES = [
        ('High Risk', 'High Risk'),
        ('Medium Risk', 'Medium Risk'),
        ('Information', 'Information'),
    ]

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='health_alerts'
    )

    report = models.ForeignKey(
        DiseaseReport,
        on_delete=models.CASCADE,
        related_name='health_alerts'
    )

    alert_type = models.CharField(
        max_length=30,
        choices=ALERT_TYPES
    )

    title = models.CharField(
        max_length=200
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.alert_type} - {self.recipient.username}"