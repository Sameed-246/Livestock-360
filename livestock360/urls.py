from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from dashboard import views


urlpatterns = [

    # Home / Landing Page
    path(
        '',
        views.home,
        name='home'
    ),

    # Django Admin
    path(
        'admin/',
        admin.site.urls
    ),

    # Authentication
    path(
        'accounts/',
        include('accounts.urls')
    ),

    # Farmer Dashboard
    path(
        'dashboard/',
        include('dashboard.urls')
    ),

    # Animals
    path(
        'animals/',
        include('animals.urls')
    ),

    # Health Reports
    path(
        'reports/',
        include('reports.urls')
    ),

    # Veterinarian
    path(
        'veterinarian/',
        include('veterinarian.urls')
    ),

    # Alerts / Notifications
    path(
        'alerts/',
        include('alerts.urls')
    ),

]

# Serve uploaded media files during local development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
