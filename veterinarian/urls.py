from django.urls import path

from . import views


urlpatterns = [

    path(
        '',
        views.vet_dashboard,
        name='vet_dashboard'
    ),

    path(
        'case/<int:report_id>/',
        views.vet_case_detail,
        name='vet_case_detail'
    ),

    path(
        'case/<int:report_id>/status/',
        views.update_case_status,
        name='update_case_status'
    ),

    path(
        'map/',
        views.vet_surveillance_map,
        name='vet_surveillance_map'
    ),

]