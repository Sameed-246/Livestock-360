from django.urls import path
from . import views


urlpatterns = [

    path(
        '',
        views.animal_list,
        name='animal_list'
    ),

    path(
        'add/',
        views.add_animal,
        name='add_animal'
    ),

    path(
        'detail/<int:animal_id>/',
        views.animal_detail,
        name='animal_detail'
    ),

    path(
        'delete/<int:animal_id>/',
        views.delete_animal,
        name='delete_animal'
    ),
    path(
    'detail/<int:animal_id>/vaccination/add/',
    views.add_vaccination,
    name='add_vaccination'
),
]