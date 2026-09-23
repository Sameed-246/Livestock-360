from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [

    # =========================
    # FARMER LOGIN
    # =========================

    path(
        'farmer-login/',
        auth_views.LoginView.as_view(
            template_name='accounts/farmer_login.html',
            next_page='/dashboard/'
        ),
        name='farmer_login'
    ),


    # =========================
    # VETERINARIAN LOGIN
    # =========================

    path(
        'vet-login/',
        views.vet_login,
        name='vet_login'
    ),


    # =========================
    # FARMER REGISTRATION
    # =========================

    path(
        'register/',
        views.register,
        name='register'
    ),


    # =========================
    # LOGOUT
    # =========================

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

]