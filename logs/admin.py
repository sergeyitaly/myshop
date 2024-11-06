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
    actions = None  # Optional, to disable default actions if needed
    ordering = ('-request_count',)  # Order by request count (highest to lowest)
    search_fields = ['endpoint']  # Allow searching by endpoint

    # Add the clear_logs action to the list of available actions
    actions = [clear_logs]

    # Add a custom URL to clear logs
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


    # Add a button to the top of the changelist page
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['clear_logs_button'] = True
        return super().changelist_view(request, extra_context=extra_context)

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
        time_delta = {
            'day': timedelta(days=1),
            'week': timedelta(weeks=1),
            'month': timedelta(weeks=4),
            'year': timedelta(weeks=52)
        }

        start_date = now - time_delta.get(time_period, timedelta(days=1))

        # Query the data based on `has_chat_id` (for Telegram endpoint)
        data = APILog.objects.filter(timestamp__gte=start_date)

        # Treat "by_chat_id" the same as "Telegram"
        endpoints = ['Vercel', 'Telegram']  # Consider 'Telegram' and 'by_chat_id' as one group

        # Initialize chart data
        chart_data = {
            'labels': [],
            'data': {endpoint: [] for endpoint in endpoints}  # Count for each endpoint
        }

        if time_period == 'week':
            days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            chart_data['labels'] = days_of_week
            data_grouped = data.extra(select={'day_of_week': 'EXTRACT(DOW FROM timestamp)'}).values('day_of_week', 'endpoint').annotate(request_count=Count('id')).order_by('day_of_week')

            for entry in data_grouped:
                day = entry['day_of_week']
                endpoint = entry['endpoint'] if entry['endpoint'] != 'by_chat_id' else 'Telegram'  # Group 'by_chat_id' as 'Telegram'
                chart_data['data'].setdefault(endpoint, [0]*7)
                chart_data['data'][endpoint][day] = entry['request_count']
                chart_data['data']['Total'][day] += entry['request_count']

        elif time_period == 'month':
            chart_data['labels'] = [f'Day {i+1}' for i in range(31)]
            data_grouped = data.extra(select={'day_of_month': 'EXTRACT(DAY FROM timestamp)'}).values('day_of_month', 'endpoint').annotate(request_count=Count('id')).order_by('day_of_month')

            for entry in data_grouped:
                day = entry['day_of_month'] - 1  # Adjust to 0-indexed for the chart
                endpoint = entry['endpoint'] if entry['endpoint'] != 'by_chat_id' else 'Telegram'  # Group 'by_chat_id' as 'Telegram'
                chart_data['data'].setdefault(endpoint, [0]*31)
                chart_data['data'][endpoint][day] = entry['request_count']
                chart_data['data']['Total'][day] += entry['request_count']

        elif time_period == 'year':
            months_of_year = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            chart_data['labels'] = months_of_year
            data_grouped = data.extra(select={'month_of_year': 'EXTRACT(MONTH FROM timestamp)'}).values('month_of_year', 'endpoint').annotate(request_count=Count('id')).order_by('month_of_year')

            for entry in data_grouped:
                month = entry['month_of_year'] - 1  # Adjust to 0-indexed for the chart
                endpoint = entry['endpoint'] if entry['endpoint'] != 'by_chat_id' else 'Telegram'  # Group 'by_chat_id' as 'Telegram'
                chart_data['data'].setdefault(endpoint, [0]*12)
                chart_data['data'][endpoint][month] = entry['request_count']
                chart_data['data']['Total'][month] += entry['request_count']

        else:
            # Default to daily data (today)
            chart_data['labels'] = ['Today']
            chart_data['data'] = {'Vercel': [data.filter(endpoint='Vercel').count()], 'Telegram': [data.filter(endpoint='by_chat_id').count()], 'Total': [data.count()]}

        return chart_data

    # Handle AJAX requests for chart data
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
                    const ctx = document.getElementById('requestChart').getContext('2d');
                    let chartData = {{ chart_data|safe }};
                    const requestChart = new Chart(ctx, {
                        type: 'bar',
                        data: {
                            labels: chartData.labels,
                            datasets: [{
                                label: 'Request Count',
                                data: chartData.data,
                                backgroundColor: ['#4CAF50', '#FFC107', '#2196F3'],
                            }]
                        },
                        options: {
                            responsive: true,
                            plugins: {
                                legend: { position: 'top' },
                            },
                            scales: {
                                y: {
                                    beginAtZero: true,
                                }
                            }
                        }
                    });

                    // Fetch new data when the time period changes
                    const timePeriodSelect = document.getElementById('time_period');
                    timePeriodSelect.addEventListener('change', function() {
                        const timePeriod = timePeriodSelect.value;
                        fetch(`/admin/api/logs/chart-data/?time_period=${timePeriod}`)
                            .then(response => response.json())
                            .then(data => {
                                requestChart.data.labels = data.labels;
                                requestChart.data.datasets[0].data = data.data;
                                requestChart.update();  // Update the chart with new data
                            });
                    });
                });
            </script>
        """
        return super().render_change_list(request, context, *args, **kwargs)

    def change_list(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['chart_html'] = mark_safe("""
            <canvas id="requestChart"></canvas>
        """)
        return super().change_list(request, extra_context=extra_context)

# Register the admin class
admin.site.register(APILog, APILogAdmin)
