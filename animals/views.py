from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Animal
from .forms import AnimalForm, VaccinationRecordForm


@login_required
def animal_list(request):

    animals = Animal.objects.filter(
        owner=request.user
    ).order_by('-created_at')

    return render(
        request,
        'animals/animal_list.html',
        {
            'animals': animals
        }
    )


@login_required
def add_animal(request):

    if request.method == 'POST':

        form = AnimalForm(request.POST)

        if form.is_valid():

            animal = form.save(commit=False)

            animal.owner = request.user

            animal.save()

            return redirect('animal_list')

    else:

        form = AnimalForm()

    return render(
        request,
        'animals/add_animal.html',
        {
            'form': form
        }
    )


@login_required
def animal_detail(request, animal_id):

    animal = get_object_or_404(
        Animal,
        id=animal_id,
        owner=request.user
    )

    reports = animal.disease_reports.order_by(
        '-created_at'
    )

    vaccinations = animal.vaccinations.order_by(
        '-date_given'
    )

    return render(
        request,
        'animals/animal_detail.html',
        {
            'animal': animal,
            'reports': reports,
            'vaccinations': vaccinations,
        }
    )


@login_required
def delete_animal(request, animal_id):

    animal = get_object_or_404(
        Animal,
        id=animal_id,
        owner=request.user
    )

    if request.method == 'POST':

        animal.delete()

        return redirect('animal_list')

    return render(
        request,
        'animals/delete_animal.html',
        {
            'animal': animal
        }
    )


@login_required
def add_vaccination(request, animal_id):

    animal = get_object_or_404(
        Animal,
        id=animal_id,
        owner=request.user
    )

    if request.method == 'POST':

        form = VaccinationRecordForm(
            request.POST
        )

        if form.is_valid():

            vaccination = form.save(
                commit=False
            )

            vaccination.animal = animal

            vaccination.save()

            animal.vaccination_status = True

            animal.save(
                update_fields=[
                    'vaccination_status'
                ]
            )

            return redirect(
                'animal_detail',
                animal_id=animal.id
            )

    else:

        form = VaccinationRecordForm()

    return render(
        request,
        'animals/add_vaccination.html',
        {
            'form': form,
            'animal': animal,
        }
    )