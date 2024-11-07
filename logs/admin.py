from django.contrib import admin
from django.db.models import Count, Max
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.utils.safestring import mark_safe
from .models import APILog
from datetime import timedelta
from django.utils.html import format_html
from django.urls import path
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models.functions import TruncDate, TruncWeek, TruncMonth, TruncHour
from collections import defaultdict

# Custom action to clear logs
def clear_logs(modeladmin, request, queryset):
    # This will delete all APILog entries
    count, _ = queryset.delete()
    modeladmin.message_user(request, f'{count} log(s) cleared.')

clear_logs.short_description = 'Clear selected logs'


class TimePeriodFilter(admin.SimpleListFilter):
    title = 'Time Period'
    parameter_name = 'time_period'

    def lookups(self, request, model_admin):
        return (
            ('today', 'Today'),
            ('week', 'This Week'),
            ('month', 'This Month'),
            ('year', 'This Year'),
        )

    def queryset(self, request, queryset):
        today = timezone.now()
        if self.value() == 'today':
            return queryset.filter(timestamp__date=today.date())
        elif self.value() == 'week':
            start_of_week = today - timedelta(days=today.weekday())
            return queryset.filter(timestamp__gte=start_of_week)
        elif self.value() == 'month':
            start_of_month = today.replace(day=1)
            return queryset.filter(timestamp__gte=start_of_month)
        elif self.value() == 'year':
            start_of_year = today.replace(month=1, day=1)
            return queryset.filter(timestamp__gte=start_of_year)
        return queryset


class APILogAdmin(admin.ModelAdmin):
    list_display = ('endpoint', 'has_chat_id', 'request_count', 'timestamp')
    list_filter = (TimePeriodFilter,)  # Added custom filter
    actions = [clear_logs]  # Added clear_logs action
    ordering = ('-request_count',)  # Order by request count (highest to lowest)
    search_fields = ['endpoint']  # Allow searching by endpoint

    # Exclude unwanted endpoints in the queryset
    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        # Exclude unwanted endpoints
        exclude_patterns = [
            '/admin/logs/apilog/', '/favicon.ico', '/admin/jsi18n/', '/admin/',
            '/api/health_check', '/api/token/refresh/', '/api/telegram_users/', 
            '/auth/token/login/', '/api/token/','/admin/api/logs/chart-data/',
        ]

        queryset = queryset.filter(endpoint__icontains='/api/')

        # Exclude the specific endpoints in the exclusion list
        queryset = queryset.exclude(endpoint__in=exclude_patterns)
        return queryset


    # Add the custom URL for clearing logs
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('clear_logs/', self.clear_all_logs, name='clear_logs'),
        ]
        return custom_urls + urls

    # Method to clear all logs
    def clear_all_logs(self, request):
        try:
            # Clear all logs
            APILog.objects.all().delete()
            messages.success(request, "All logs have been cleared successfully.")
        except Exception as e:
            messages.error(request, f"Error clearing logs: {str(e)}")

        return HttpResponseRedirect('/admin/logs/apilog/')  # Redirect back to the admin list view

    def request_count(self, obj):
        """
        Return the request count for each endpoint.
        """
        return obj.request_count

    def last_visited(self, obj):
        """
        Return the last visited timestamp for the endpoint.
        """
        last_visit = APILog.objects.filter(endpoint=obj.endpoint).aggregate(last_visited=Max('timestamp'))['last_visited']
        return last_visit if last_visit else 'Never'




    def get_charts_data(self, time_period):
        now = timezone.now()
        chart_data = {'labels': [], 'data': {'Telegram': [], 'Vercel': []}}

        # Define the patterns to exclude
        exclude_patterns = [
            '/favicon.ico', '/admin/', '/api/token/', '/auth/token/login/', 
            '/api/token/refresh/', '/admin/*', '/api/health_check', '/media/','/admin/api/logs/chart-data/',
        ]

        # Set date range and group data by appropriate intervals
        if time_period == 'day':
            date_range = [now - timedelta(hours=x) for x in range(23, -1, -1)]
            chart_data['labels'] = [hour.strftime('%H:%M') for hour in date_range]
            
            # Separate queries for Telegram and Vercel endpoints
            telegram_data = APILog.objects.filter(
                timestamp__date=now.date(),
                endpoint__icontains='by_chat_id'
            ).exclude(endpoint__in=exclude_patterns) \
            .annotate(hour=TruncHour('timestamp')).values('hour') \
            .annotate(telegram_count=Count('id'))
            
            vercel_data = APILog.objects.filter(
                timestamp__date=now.date(),
                endpoint__icontains='/api/'
            ).exclude(endpoint__icontains='by_chat_id') \
            .exclude(endpoint__in=exclude_patterns) \
            .annotate(hour=TruncHour('timestamp')).values('hour') \
            .annotate(vercel_count=Count('id'))
        
        elif time_period == 'week':
            date_range = [now - timedelta(days=x) for x in range(6, -1, -1)]
            chart_data['labels'] = [day.strftime('%A') for day in date_range]

            telegram_data = APILog.objects.filter(
                timestamp__gte=now - timedelta(days=now.weekday()),
                endpoint__icontains='by_chat_id'
            ).exclude(endpoint__in=exclude_patterns) \
            .annotate(day=TruncDate('timestamp')).values('day') \
            .annotate(telegram_count=Count('id'))
            
            vercel_data = APILog.objects.filter(
                timestamp__gte=now - timedelta(days=now.weekday()),
                endpoint__icontains='/api/'
            ).exclude(endpoint__icontains='by_chat_id') \
            .exclude(endpoint__in=exclude_patterns) \
            .annotate(day=TruncDate('timestamp')).values('day') \
            .annotate(vercel_count=Count('id'))
        
        elif time_period == 'month':
            days_in_month = (now.replace(day=28) + timedelta(days=4)).day
            date_range = [now - timedelta(days=x) for x in range(days_in_month - 1, -1, -1)]
            chart_data['labels'] = [day.strftime('%d') for day in date_range]

            telegram_data = APILog.objects.filter(
                timestamp__month=now.month,
                endpoint__icontains='by_chat_id'
            ).exclude(endpoint__in=exclude_patterns) \
            .annotate(day=TruncDate('timestamp')).values('day') \
            .annotate(telegram_count=Count('id'))
            
            vercel_data = APILog.objects.filter(
                timestamp__month=now.month,
                endpoint__icontains='/api/'
            ).exclude(endpoint__icontains='by_chat_id') \
            .exclude(endpoint__in=exclude_patterns) \
            .annotate(day=TruncDate('timestamp')).values('day') \
            .annotate(vercel_count=Count('id'))
        
        elif time_period == 'year':
            date_range = [now.replace(month=x, day=1) for x in range(1, 13)]
            chart_data['labels'] = [month.strftime('%b') for month in date_range]

            telegram_data = APILog.objects.filter(
                timestamp__year=now.year,
                endpoint__icontains='by_chat_id'
            ).exclude(endpoint__in=exclude_patterns) \
            .annotate(month=TruncMonth('timestamp')).values('month') \
            .annotate(telegram_count=Count('id'))
            
            vercel_data = APILog.objects.filter(
                timestamp__year=now.year,
                endpoint__icontains='/api/'
            ).exclude(endpoint__icontains='by_chat_id') \
            .exclude(endpoint__in=exclude_patterns) \
            .annotate(month=TruncMonth('timestamp')).values('month') \
            .annotate(vercel_count=Count('id'))

        # Fill chart data with separate counts for Telegram and Vercel
        telegram_counts_by_timestamp = {entry['hour' if time_period == 'day' else 'day' if time_period in ['week', 'month'] else 'month']: entry['telegram_count'] for entry in telegram_data}
        vercel_counts_by_timestamp = {entry['hour' if time_period == 'day' else 'day' if time_period in ['week', 'month'] else 'month']: entry['vercel_count'] for entry in vercel_data}

        for date in date_range:
            time_key = date.replace(minute=0, second=0, microsecond=0) if time_period == 'day' else date
            chart_data['data']['Telegram'].append(telegram_counts_by_timestamp.get(time_key, 0))
            chart_data['data']['Vercel'].append(vercel_counts_by_timestamp.get(time_key, 0))

        return chart_data

    @method_decorator(csrf_exempt)
    def get_chart_data_ajax(self, request):
        time_period = request.GET.get('time_period', 'day')
        chart_data = self.get_charts_data(time_period)
        return JsonResponse(chart_data)


    @method_decorator(csrf_exempt)
    def get_chart_data_ajax(self, request):
        time_period = request.GET.get('time_period', 'day')
        chart_data = self.get_charts_data(time_period)
        return JsonResponse(chart_data)

    def changelist_view(self, request, extra_context=None):
        # Default to daily view if no time period is selected
        time_period = request.GET.get('time_period', 'day')

        # Get the chart data based on the time period
        chart_data = self.get_charts_data(time_period)

        extra_context = extra_context or {}
        extra_context['chart_data'] = json.dumps(chart_data)

        extra_context['time_periods'] = {
            'day': 'Today',
            'week': 'This Week',
            'month': 'This Month',
            'year': 'This Year'
        }

        return super().changelist_view(request, extra_context=extra_context)

    def render_change_list(self, request, context, *args, **kwargs):
        context['chart_js'] = """
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <script>
                document.addEventListener('DOMContentLoaded', function() {
                    const ctx = document.getElementById('logChart').getContext('2d');
                    const chartData = JSON.parse('{{ chart_data|escapejs }}');
                    
                    new Chart(ctx, {
                        type: 'bar',
                        data: {
                            labels: chartData.labels,
                            datasets: [
                                {
                                    label: 'Vercel',
                                    data: chartData.data.Vercel,
                                    backgroundColor: 'rgba(255, 99, 132, 0.5)',
                                    borderColor: 'rgb(255, 99, 132)',
                                    borderWidth: 1
                                },
                                {
                                    label: 'Telegram',
                                    data: chartData.data.Telegram,
                                    backgroundColor: 'rgba(54, 162, 235, 0.5)', // Blue with transparency
                                    borderColor: 'rgba(54, 162, 235, 1)'
                                    borderWidth: 1
                                },
                                {
                                    label: 'Total',
                                    data: chartData.data.Total,
                                    backgroundColor: 'rgba(75, 192, 192, 0.5)',
                                    borderColor: 'rgb(75, 192, 192)',
                                    borderWidth: 1
                                }
                            ]
                        },
                        options: {
                            scales: {
                                x: { beginAtZero: true },
                                y: { beginAtZero: true }
                            }
                        }
                    });
                });
            </script>
        """
        return super().render_change_list(request, context, *args, **kwargs)

admin.site.register(APILog, APILogAdmin)
