from django.urls import path
from . import views

urlpatterns = [
    path('', views.report_list, name='report_list'),

    path(
        'report/',
        views.report_problem,
        name='report_problem'
    ),

    path(
        'success/<int:report_id>/',
        views.report_success,
        name='report_success'
    ),
]