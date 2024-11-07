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
from django.db.models.functions import TruncDate, TruncWeek, TruncMonth

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
            '/auth/token/login/', '/api/token/',

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
        time_delta = {
            'day': timedelta(days=1),
            'week': timedelta(weeks=1),
            'month': timedelta(weeks=4),
            'year': timedelta(weeks=52)
        }

        start_date = now - time_delta.get(time_period, timedelta(days=1))
        data = APILog.objects.filter(timestamp__gte=start_date)

        # Exclude non-API endpoints and unwanted specific endpoints
        exclude_patterns = [
            '/favicon.ico', '/admin/', '/api/token/', '/auth/token/login/', '/api/token/refresh/', '/admin/logs/apilog/',
            '/api/health_check', '/media/', '/admin/jsi18n/'
        ]
        
        # Only include /api/ endpoints and exclude the unwanted ones
        data = data.filter(endpoint__icontains='/api/').exclude(endpoint__in=exclude_patterns)

        # Group by the appropriate time period
        if time_period == 'day':
            data_grouped = data.annotate(day=TruncDate('timestamp')).values('day', 'endpoint').annotate(request_count=Count('id')).order_by('day')
        elif time_period == 'week':
            data_grouped = data.annotate(week=TruncWeek('timestamp')).values('week', 'endpoint').annotate(request_count=Count('id')).order_by('week')
        elif time_period == 'month':
            data_grouped = data.annotate(month=TruncMonth('timestamp')).values('month', 'endpoint').annotate(request_count=Count('id')).order_by('month')
        elif time_period == 'year':
            data_grouped = data.annotate(year=TruncDate('timestamp')).values('year', 'endpoint').annotate(request_count=Count('id')).order_by('year')
        else:
            data_grouped = data.annotate(day=TruncDate('timestamp')).values('day', 'endpoint').annotate(request_count=Count('id')).order_by('day')

        # Initialize chart data
        chart_data = {
            'labels': [],
            'data': {
                'Vercel': [],
                'Telegram': [],
                'Total': []
            }
        }

        # Aggregation logic based on time period
        if time_period == 'week':
            days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            chart_data['labels'] = days_of_week
            for entry in data_grouped:
                day = entry['week'].weekday()  # Extract the day of the week
                endpoint = entry['endpoint']
                
                # Classify endpoints as Vercel or Telegram
                if '/by_chat_id' in endpoint:
                    chart_data['data']['Telegram'].append(entry['request_count'])
                else:
                    chart_data['data']['Vercel'].append(entry['request_count'])

            # Total bar for the week (sum of Vercel and Telegram)
            chart_data['data']['Total'] = [sum(x) for x in zip(chart_data['data']['Vercel'], chart_data['data']['Telegram'])]

        elif time_period == 'month':
            chart_data['labels'] = [f'Day {i+1}' for i in range(31)]
            for entry in data_grouped:
                day = entry.get('month').day - 1  # Adjust to 0-indexed for the chart
                endpoint = entry['endpoint']
                
                # Classify endpoints as Vercel or Telegram
                if '/by_chat_id' in endpoint:
                    chart_data['data']['Telegram'].append(entry['request_count'])
                else:
                    chart_data['data']['Vercel'].append(entry['request_count'])

            # Total bar for the month (sum of Vercel and Telegram)
            chart_data['data']['Total'] = [sum(x) for x in zip(chart_data['data']['Vercel'], chart_data['data']['Telegram'])]

        elif time_period == 'year':
            months_of_year = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            chart_data['labels'] = months_of_year
            for entry in data_grouped:
                month = entry.get('year').month - 1  # Adjust to 0-indexed for the chart
                endpoint = entry['endpoint']
                
                # Classify endpoints as Vercel or Telegram
                if '/by_chat_id' in endpoint:
                    chart_data['data']['Telegram'].append(entry['request_count'])
                else:
                    chart_data['data']['Vercel'].append(entry['request_count'])

            # Total bar for the year (sum of Vercel and Telegram)
            chart_data['data']['Total'] = [sum(x) for x in zip(chart_data['data']['Vercel'], chart_data['data']['Telegram'])]

        else:
            chart_data['labels'] = ['Today']
            chart_data['data']['Vercel'] = [data.exclude(endpoint__icontains='by_chat_id').count()]
            chart_data['data']['Telegram'] = [data.filter(endpoint__icontains='by_chat_id').count()]
            chart_data['data']['Total'] = [data.count()]

        return chart_data

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
                    const chart = new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: chartData.labels,
                            datasets: Object.keys(chartData.data).map(function(label) {
                                let borderColor;
                                if (label === 'Telegram') {
                                    borderColor = 'rgb(54, 162, 235)'; // Blue for Telegram
                                } else if (label === 'Vercel') {
                                    borderColor = 'rgb(255, 99, 132)'; // Red for Vercel
                                } else {
                                    borderColor = 'rgb(75, 192, 192)'; // Green for Total
                                }
                                return {
                                    label: label,
                                    data: chartData.data[label],
                                    borderColor: borderColor,
                                    fill: false
                                };
                            })
                        }
                    });
                });
            </script>
        """
        return super().render_change_list(request, context, *args, **kwargs)

admin.site.register(APILog, APILogAdmin)
