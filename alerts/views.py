from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import HealthAlert


@login_required
def notification_center(request):

    alerts = HealthAlert.objects.filter(
        recipient=request.user
    ).select_related(
        'report',
        'report__animal'
    ).order_by('-created_at')

    unread_count = alerts.filter(
        is_read=False
    ).count()

    return render(
        request,
        'alerts/notification_center.html',
        {
            'alerts': alerts,
            'unread_count': unread_count,
        }
    )


@login_required
def mark_alert_read(request, alert_id):

    alert = get_object_or_404(
        HealthAlert,
        id=alert_id,
        recipient=request.user
    )

    alert.is_read = True
    alert.save(update_fields=['is_read'])

    return redirect(
        'notification_center'
    )