from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from reports.models import DiseaseReport


def veterinarian_required(request):
    if not request.user.groups.filter(
        name='Veterinarian'
    ).exists():
        raise PermissionDenied


@login_required
def vet_dashboard(request):

    veterinarian_required(request)

    reports = DiseaseReport.objects.select_related(
        'animal',
        'animal__owner'
    ).order_by('-created_at')

    # Risk counts use the stored AI risk_level
    high_risk = reports.filter(
        risk_level='High'
    ).count()

    medium_risk = reports.filter(
        risk_level='Medium'
    ).count()

    low_risk = reports.filter(
        risk_level='Low'
    ).count()

    # Case status counts
    pending = reports.filter(
        status='Pending'
    ).count()

    reviewed = reports.filter(
        status='Reviewed'
    ).count()

    resolved = reports.filter(
        status='Resolved'
    ).count()

    context = {
        'reports': reports,
        'total_reports': reports.count(),
        'high_risk': high_risk,
        'medium_risk': medium_risk,
        'low_risk': low_risk,
        'pending': pending,
        'reviewed': reviewed,
        'resolved': resolved,
    }

    return render(
        request,
        'veterinarian/vet_dashboard.html',
        context
    )


@login_required
def vet_case_detail(request, report_id):

    veterinarian_required(request)

    report = get_object_or_404(
        DiseaseReport.objects.select_related(
            'animal',
            'animal__owner'
        ),
        id=report_id
    )

    return render(
        request,
        'veterinarian/vet_case_detail.html',
        {'report': report}
    )


@login_required
def update_case_status(request, report_id):

    veterinarian_required(request)

    report = get_object_or_404(
        DiseaseReport,
        id=report_id
    )

    if request.method == 'POST':

        new_status = request.POST.get('status')

        allowed_statuses = [
            'Pending',
            'Reviewed',
            'Resolved'
        ]

        if new_status in allowed_statuses:

            report.status = new_status

            report.save(
                update_fields=['status']
            )

            messages.success(
                request,
                f'Case status updated to {new_status}.'
            )

    return redirect(
        'vet_case_detail',
        report_id=report.id
    )


@login_required
def vet_surveillance_map(request):

    veterinarian_required(request)

    reports = DiseaseReport.objects.filter(
        latitude__isnull=False,
        longitude__isnull=False
    ).select_related(
        'animal'
    ).order_by('-created_at')

    return render(
        request,
        'veterinarian/vet_map.html',
        {'reports': reports}
    )