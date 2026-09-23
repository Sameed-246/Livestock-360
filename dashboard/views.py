from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from animals.models import Animal
from reports.models import DiseaseReport


def home(request):
    return render(request, 'dashboard/home.html')


@login_required
def farmer_dashboard(request):

    # Get only animals belonging to the logged-in farmer
    animals = Animal.objects.filter(
        owner=request.user
    ).order_by('-created_at')

    # Get reports belonging to the farmer's animals
    reports = DiseaseReport.objects.filter(
        animal__owner=request.user
    ).select_related(
        'animal'
    ).order_by('-created_at')

    # Count pending reports
    pending_reports = reports.filter(
        status='Pending'
    ).count()

    context = {
        'animals': animals,
        'animal_count': animals.count(),
        'report_count': reports.count(),
        'pending_count': pending_reports,
        'recent_reports': reports[:5],
    }

    return render(
        request,
        'dashboard/farmer_dashboard.html',
        context
    )