from django.urls import path
from . import views

urlpatterns = [
    path(
        '',
        views.farmer_dashboard,
        name='farmer_dashboard'
    ),
]