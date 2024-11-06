from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib import admin
from django.utils import timezone
from datetime import timedelta
from .models import APILog  # Assuming APILog is a model
from django.db.models import Count
import json
from django.utils.safestring import mark_safe

class APILogAdmin(admin.ModelAdmin):
    list_display = ('endpoint', 'request_count', 'has_chat_id', 'timestamp')
    list_filter = ('has_chat_id',)

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

        # Group data by `has_chat_id` and count the requests
        grouped_data = data.values('has_chat_id').annotate(request_count=Count('id'))

        # Prepare the response data for the chart
        chart_data = {
            'labels': ['Telegram Bot (has_chat_id)', 'Vercel (no_chat_id)'],
            'data': [0, 0]  # Default counts for both groups
        }

        for entry in grouped_data:
            if entry['has_chat_id']:  # Telegram bot data
                chart_data['data'][0] = entry['request_count']
            else:  # Vercel data
                chart_data['data'][1] = entry['request_count']

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
                                backgroundColor: ['#4CAF50', '#FFC107'],
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
