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
from django.urls import reverse
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

# Custom action to clear logs
def clear_logs(modeladmin, request, queryset):
    # This will delete all APILog entries
    count, _ = queryset.delete()
    modeladmin.message_user(request, f'{count} log(s) cleared.')

clear_logs.short_description = 'Clear selected logs'

class TimePeriodFilter(admin.SimpleListFilter):
    title = _('Time Period')
    parameter_name = 'time_period'

    # Define the options available in the dropdown
    def lookups(self, request, model_admin):
        return (
            ('today', _('Today')),
            ('week', _('This Week')),
            ('month', _('This Month')),
            ('year', _('This Year')),
        )

    def queryset(self, request, queryset):
        time_period = request.GET.get(self.parameter_name)

        # Handle filtering based on selected time period
        if time_period:
            now = timezone.now()
            if time_period == 'today':
                return queryset.filter(timestamp__date=now.date())
            elif time_period == 'week':
                start_of_week = now - timedelta(days=now.weekday())  # start of this week
                return queryset.filter(timestamp__date__gte=start_of_week.date())
            elif time_period == 'month':
                start_of_month = now.replace(day=1)
                return queryset.filter(timestamp__date__gte=start_of_month.date())
            elif time_period == 'year':
                start_of_year = now.replace(month=1, day=1)
                return queryset.filter(timestamp__date__gte=start_of_year.date())
        return queryset
        
class EndpointFilter(admin.SimpleListFilter):
    title = 'Endpoint'
    parameter_name = 'endpoint'

    def lookups(self, request, model_admin):
        # Get all distinct endpoints
        endpoints = APILog.objects.values('endpoint').distinct()
        return [(endpoint['endpoint'], endpoint['endpoint']) for endpoint in endpoints]

    def queryset(self, request, queryset):
        endpoint_filter = self.value()  # The selected endpoint value from the filter
        if endpoint_filter:
            return queryset.filter(endpoint=endpoint_filter)
        return queryset


class APILogAdmin(admin.ModelAdmin):
    list_display = ('clickable_endpoint', 'has_chat_id', 'request_count', 'timestamp')
    list_filter = (TimePeriodFilter, EndpointFilter)
    actions = [clear_logs]
    ordering = ('-request_count',)
    search_fields = ['endpoint']
    change_list_template = 'admin/logs/apilog/change_list.html'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        # Exclude unwanted endpoints
        exclude_patterns = [
            '/admin/logs/apilog/', '/favicon.ico', '/admin/jsi18n/', '/admin/*', '/admin/', '/admin/login/',                                                             
            '/api/health_check', '/api/token/refresh/', '/api/telegram_users/', '/api/logs/chart-data/',
            '/auth/token/login/', '/api/token/', '/admin/api/logs/chart-data/',
        ]

        # Filter by endpoint if it's passed in the GET request
        endpoint_filter = request.GET.get('endpoint', '')
        if endpoint_filter:
            queryset = queryset.filter(endpoint=endpoint_filter)

        # Exclude specific unwanted endpoints
        queryset = queryset.exclude(endpoint__in=exclude_patterns)

        return queryset
    # Add the custom URL for clearing logs
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('clear_logs/', self.clear_all_logs, name='clear_logs'),
            path('filter_by_endpoint/', self.filter_by_endpoint, name='filter_by_endpoint'),

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


    def filter_by_endpoint(self, request):
        endpoint = request.GET.get('endpoint', '')
        if endpoint:
            # Filter logs by the selected endpoint
            logs = APILog.objects.filter(endpoint=endpoint)
            # Return a JSON response with the filtered data
            logs_data = list(logs.values())
            return JsonResponse({'logs': logs_data})
        return JsonResponse({'error': 'Endpoint not provided'}, status=400)

    def clickable_endpoint(self, obj):
        """
        Display the endpoint as a clickable link in the admin list view.
        """
        # Add a timestamp to the query to prevent the browser from using cached results
        timestamp = timezone.now().timestamp()
        endpoint_url = reverse('admin:logs_apilog_changelist') + f'?endpoint={obj.endpoint}&_={timestamp}'
        return format_html('<a href="{}">{}</a>', endpoint_url, obj.endpoint)


    clickable_endpoint.short_description = 'Endpoint'  # Set the column name
    clickable_endpoint.admin_order_field = 'endpoint'


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
            '/favicon.ico', '/admin/', '/api/token/', '/auth/token/login/', '/api/logs/chart-data/',
            '/api/token/refresh/', '/admin/*', '/api/health_check', '/media/','/admin/api/logs/chart-data/',
        ]

        # Set date range and group data by appropriate intervals
        if time_period == 'day':
            date_range = [now - timedelta(hours=x) for x in range(23, -1, -1)]
            chart_data['labels'] = [hour.strftime('%H:%M') for hour in date_range]
            telegram_data = APILog.objects.filter(
                timestamp__date=now.date(),
                endpoint__icontains='by_chat_id'
            ).exclude(endpoint__in=exclude_patterns) \
                .annotate(hour=TruncHour('timestamp')).values('hour') \
                .annotate(telegram_count=Count('id'))
            
            vercel_data = APILog.objects.filter(
                timestamp__date=now.date(),
                endpoint__icontains='/'
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
                endpoint__icontains='/'
                #endpoint__icontains='/api/'

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
                endpoint__icontains='/'
                #endpoint__icontains='/api/'
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
                endpoint__icontains='/'
                #endpoint__icontains='/api/'

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

    def changelist_view(self, request, extra_context=None):
        time_period = request.GET.get('time_period', 'day')
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
        # Including Chart.js and configuring the chart
        context['chart_js'] = """
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <script>
                document.addEventListener('DOMContentLoaded', function () {
                    const timePeriodSelect = document.getElementById('time_period_select');
                    const chartCanvas = document.getElementById('chart_canvas');
                    const ctx = chartCanvas.getContext('2d');
                    let chart;

                    // Initialize the chart with default data
                    function createChart(data) {
                        if (chart) {
                            chart.destroy();
                        }
                        chart = new Chart(ctx, {
                            type: 'line',
                            data: {
                                labels: data.labels,
                                datasets: [
                                    {
                                        label: 'Telegram',
                                        data: data.data.Telegram,
                                        borderColor: 'rgba(75, 192, 192, 1)',
                                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                                        fill: true,
                                    },
                                    {
                                        label: 'Vercel',
                                        data: data.data.Vercel,
                                        borderColor: 'rgba(153, 102, 255, 1)',
                                        backgroundColor: 'rgba(153, 102, 255, 0.2)',
                                        fill: true,
                                    }
                                ]
                            },
                            options: {
                                responsive: true,
                                scales: {
                                    x: { 
                                        beginAtZero: true 
                                    },
                                    y: { 
                                        beginAtZero: true 
                                    }
                                }
                            }
                        });
                    }

                    // Function to update the chart data dynamically
                    function updateChart(timePeriod) {
                        fetch(`/admin/logs/apilog/chart-data/?time_period=${timePeriod}`)
                            .then(response => response.json())
                            .then(data => {
                                createChart(data);  // Update the chart with new data
                            })
                            .catch(error => console.error('Error fetching chart data:', error));
                    }

                    // Event listener for time period change
                    timePeriodSelect.addEventListener('change', function() {
                        const selectedTimePeriod = timePeriodSelect.value;
                        updateChart(selectedTimePeriod);
                    });

                    // Initialize the chart with default 'day' data
                    updateChart('day');
                });
            </script>
        """
        
        # Pass context variables for the select options
        context['time_periods'] = {
            'day': 'Today',
            'week': 'This Week',
            'month': 'This Month',
            'year': 'This Year'
        }

        return super().render_change_list(request, context, *args, **kwargs)


admin.site.register(APILog, APILogAdmin)
