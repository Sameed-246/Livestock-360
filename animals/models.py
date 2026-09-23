from django.db import models
from django.contrib.auth.models import User


class Animal(models.Model):
    ANIMAL_TYPES = [
        ('Cattle', 'Cattle'),
        ('Buffalo', 'Buffalo'),
        ('Goat', 'Goat'),
        ('Sheep', 'Sheep'),
        ('Other', 'Other'),
    ]

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    animal_id = models.CharField(max_length=50, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    animal_type = models.CharField(
        max_length=20,
        choices=ANIMAL_TYPES
    )

    breed = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    vaccination_status = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.animal_id} - {self.animal_type}"


class VaccinationRecord(models.Model):

    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name='vaccinations'
    )

    vaccine_name = models.CharField(
        max_length=150
    )

    date_given = models.DateField()

    next_due_date = models.DateField(
        null=True,
        blank=True
    )

    veterinarian_name = models.CharField(
        max_length=150,
        blank=True
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.animal.animal_id} - "
            f"{self.vaccine_name}"
        )