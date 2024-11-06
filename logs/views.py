from django.shortcuts import render
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from .models import APILog

def get_charts_data(time_period):
    # Filter APILog based on the time period
    now = timezone.now()
    time_delta = {
        'day': timedelta(days=1),
        'week': timedelta(weeks=1),
        'month': timedelta(weeks=4),
        'year': timedelta(weeks=52)
    }

    # Get the start date based on the selected time period
    start_date = now - time_delta.get(time_period, timedelta(days=1))

    # Query the data based on `has_chat_id` (Telegram) and `no_chat_id` (Vercel)
    telegram_requests = APILog.objects.filter(timestamp__gte=start_date, has_chat_id=True).count()
    vercel_requests = APILog.objects.filter(timestamp__gte=start_date, has_chat_id=False).count()

    return {
        'telegram_requests_count': telegram_requests,
        'vercel_requests_count': vercel_requests
    }

def api_logs_view(request):
    # Default to daily view if no time period is selected
    time_period = request.GET.get('time_period', 'day')

    # Get the chart data based on the time period
    chart_data = get_charts_data(time_period)

    # Pass the chart data to the template
    return render(request, 'api_logs_chart.html', {
        'telegram_requests_count': chart_data['telegram_requests_count'],
        'vercel_requests_count': chart_data['vercel_requests_count'],
        'time_period': time_period
    })
