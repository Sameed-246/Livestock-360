from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

from .forms import FarmerRegistrationForm


def register(request):

    if request.method == 'POST':

        form = FarmerRegistrationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect('farmer_dashboard')

    else:

        form = FarmerRegistrationForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )


def vet_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            if user.groups.filter(
                name='Veterinarian'
            ).exists():

                login(request, user)

                return redirect('vet_dashboard')

            messages.error(
                request,
                'This account is not registered as a veterinarian.'
            )

        else:

            messages.error(
                request,
                'Invalid veterinarian ID or password.'
            )

    return render(
        request,
        'accounts/vet_login.html'
    )


def logout_view(request):

    is_veterinarian = (
        request.user.is_authenticated
        and request.user.groups.filter(
            name='Veterinarian'
        ).exists()
    )

    logout(request)

    if is_veterinarian:
        return redirect('vet_login')

    return redirect('farmer_login')
