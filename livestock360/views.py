from django.shortcuts import render


def home(request):
    """
    Main entrance page for Livestock 360°.

    This page allows the user to choose between:
    - Farmer Portal
    - Veterinarian Portal

    The actual login URLs are handled by accounts/urls.py.
    """

    return render(
        request,
        'dashboard/home.html'
    )