from django.db import models
from animals.models import Animal


class DiseaseReport(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Reviewed', 'Reviewed'),
        ('Resolved', 'Resolved'),
    ]

    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name='disease_reports'
    )

    symptoms = models.TextField()

    temperature = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    image = models.ImageField(
        upload_to='animal_reports/',
        null=True,
        blank=True
    )

    latitude = models.DecimalField(
        max_digits=12,
        decimal_places=7,
        null=True,
        blank=True
    )

    longitude = models.DecimalField(
        max_digits=12,
        decimal_places=7,
        null=True,
        blank=True
    )

    location_address = models.CharField(
        max_length=500,
        null=True,
        blank=True
    )

    risk_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    risk_level = models.CharField(
    max_length=20,
    null=True,
    blank=True
)
    predicted_disease = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    disease_confidence = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Report for {self.animal.animal_id}"