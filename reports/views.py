from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import DiseaseReportForm
from .models import DiseaseReport

from ai_engine.predictor import predict_health_risk
from alerts.services import create_health_alerts


@login_required
def report_problem(request):

    if request.method == 'POST':

        form = DiseaseReportForm(
            request.POST,
            request.FILES,
            user=request.user
        )

        if form.is_valid():

            report = form.save(commit=False)

            ai_data = {
                'animal_type': report.animal.animal_type,
                'age': report.animal.age,
                'gender': report.animal.gender,
                'vaccination_status': report.animal.vaccination_status,
                'symptoms': report.symptoms,
                'temperature': report.temperature,
            }
            print("\n========== AI INPUT ==========")
            print(ai_data)
            print("==============================\n")

            result = predict_health_risk(ai_data)

            report.risk_score = result.get('risk_score')
            report.risk_level = result.get('risk_level')
            report.predicted_disease = result.get(
                'predicted_disease'
            )
            report.disease_confidence = result.get(
                'disease_confidence'
            )

            report.save()

            create_health_alerts(report)

            return redirect(
                'report_success',
                report_id=report.id
            )

        else:
            print("FORM ERRORS:", form.errors)

    else:

        form = DiseaseReportForm(
            user=request.user
        )

    return render(
        request,
        'reports/report_problem.html',
        {'form': form}
    )


@login_required
def report_success(request, report_id):

    report = get_object_or_404(
        DiseaseReport,
        id=report_id,
        animal__owner=request.user
    )

    return render(
        request,
        'reports/report_success.html',
        {'report': report}
    )


@login_required
def report_list(request):

    reports = DiseaseReport.objects.filter(
        animal__owner=request.user
    ).select_related(
        'animal'
    ).order_by('-created_at')

    return render(
        request,
        'reports/report_list.html',
        {
            'reports': reports,
        }
    )