from django.contrib import admin
from .models import DiseaseReport


@admin.register(DiseaseReport)
class DiseaseReportAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'animal',
        'risk_level',
        'risk_score',
        'predicted_disease',
        'status',
        'created_at',
    )

    list_filter = (
        'status',
        'risk_level',
        'created_at',
    )

    search_fields = (
        'animal__animal_id',
        'symptoms',
        'predicted_disease',
        'location_address',
    )

    readonly_fields = (
        'created_at',
    )

    ordering = ('-created_at',)
