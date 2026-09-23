from django.urls import path

from . import views


urlpatterns = [

    path(
        '',
        views.notification_center,
        name='notification_center'
    ),

    path(
        'read/<int:alert_id>/',
        views.mark_alert_read,
        name='mark_alert_read'
    ),

]