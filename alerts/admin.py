from django.contrib import admin

from .models import HealthAlert


@admin.register(HealthAlert)
class HealthAlertAdmin(admin.ModelAdmin):

    list_display = (
        'recipient',
        'alert_type',
        'title',
        'is_read',
        'created_at',
    )

    list_filter = (
        'alert_type',
        'is_read',
        'created_at',
    )

    search_fields = (
        'recipient__username',
        'title',
        'message',
    )