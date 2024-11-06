from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from django.contrib import admin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.utils.safestring import mark_safe
from .models import APILog

class TimePeriodFilter(admin.SimpleListFilter):
    title = 'Time Period'
    parameter_name = 'time_period'

    def lookups(self, request, model_admin):
        return (
            ('day', 'Today'),
            ('week', 'This Week'),
            ('month', 'This Month'),
            ('year', 'This Year'),
        )

    def queryset(self, request, queryset):
        time_period = self.value()
        if time_period:
            now = timezone.now()
            time_delta = {
                'day': timedelta(days=1),
                'week': timedelta(weeks=1),
                'month': timedelta(weeks=4),
                'year': timedelta(weeks=52)
            }
            start_date = now - time_delta.get(time_period, timedelta(days=1))
            return queryset.filter(timestamp__gte=start_date)
        return queryset

class APILogAdmin(admin.ModelAdmin):
    list_display = ('endpoint', 'request_count', 'has_chat_id', 'timestamp')
    list_filter = ('has_chat_id', TimePeriodFilter)  # Added custom filter
    actions = None  # Optional, to disable default actions if needed

def get_charts_data(self, time_period):
    now = timezone.now()
    time_delta = {
        'day': timedelta(days=1),
        'week': timedelta(weeks=1),
        'month': timedelta(weeks=4),
        'year': timedelta(weeks=52)
    }

    start_date = now - time_delta.get(time_period, timedelta(days=1))

    # Query the data based on `has_chat_id`
    data = APILog.objects.filter(timestamp__gte=start_date)

    # Generate chart data based on the selected time period
    if time_period == 'week':
        # Group data by each day of the week
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        data_grouped = data.extra(select={'day_of_week': 'EXTRACT(DOW FROM timestamp)'}).values('day_of_week').annotate(request_count=Count('id')).order_by('day_of_week')
        chart_data = {'labels': days_of_week, 'data': [0]*7}
        for entry in data_grouped:
            day_of_week = int(entry['day_of_week'])  # Ensure it's an integer
            chart_data['data'][day_of_week] = entry['request_count']
    
    elif time_period == 'month':
        # Group data by each day of the month
        chart_data = {'labels': [f'Day {i+1}' for i in range(31)], 'data': [0]*31}
        data_grouped = data.extra(select={'day_of_month': 'EXTRACT(DAY FROM timestamp)'}).values('day_of_month').annotate(request_count=Count('id')).order_by('day_of_month')
        for entry in data_grouped:
            day_of_month = int(entry['day_of_month'])  # Ensure it's an integer
            chart_data['data'][day_of_month - 1] = entry['request_count']

    elif time_period == 'year':
        # Group data by each month of the year
        months_of_year = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        chart_data = {'labels': months_of_year, 'data': [0]*12}
        data_grouped = data.extra(select={'month_of_year': 'EXTRACT(MONTH FROM timestamp)'}).values('month_of_year').annotate(request_count=Count('id')).order_by('month_of_year')
        for entry in data_grouped:
            month_of_year = int(entry['month_of_year'])  # Ensure it's an integer
            chart_data['data'][month_of_year - 1] = entry['request_count']

    else:
        # Default to day-wise data for any other time period
        chart_data = {'labels': ['Today'], 'data': [data.count()]}

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
            <canvas id="requestChart" width="400" height="200"></canvas>
        """)
        extra_context['current_time_period'] = request.GET.get('time_period', 'day')
        return super().change_list(request, extra_context=extra_context)

admin.site.register(APILog, APILogAdmin)
