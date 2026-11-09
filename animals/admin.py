from django.contrib import admin
from .models import Animal, VaccinationRecord


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):

    list_display = (
        'animal_id',
        'animal_type',
        'breed',
        'gender',
        'age',
        'vaccination_status',
        'owner',
        'created_at',
    )

    list_filter = (
        'animal_type',
        'gender',
        'vaccination_status',
        'created_at',
    )

    search_fields = (
        'animal_id',
        'breed',
        'owner__username',
    )

    ordering = ('-created_at',)


@admin.register(VaccinationRecord)
class VaccinationRecordAdmin(admin.ModelAdmin):

    list_display = (
        'animal',
        'vaccine_name',
        'date_given',
        'next_due_date',
        'veterinarian_name',
        'created_at',
    )

    list_filter = (
        'date_given',
        'next_due_date',
    )

    search_fields = (
        'animal__animal_id',
        'vaccine_name',
        'veterinarian_name',
    )

    ordering = ('-date_given',)
