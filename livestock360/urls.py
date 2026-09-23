from django.contrib import admin
from django.urls import path, include
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