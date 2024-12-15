from django.contrib import admin
from django.db.models import Count, Max
from django.utils import timezone
from django.urls import path, reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from .models import APILog
from datetime import timedelta
import json
from django.db.models.functions import TruncHour, TruncDate, TruncMonth, TruncYear, TruncDay, TruncWeek
from django.utils.translation import gettext as _
from django.utils.dateparse import parse_datetime
from django.db.models import Count, Q
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta
from django.utils.html import format_html

def clear_logs(modeladmin, request, queryset):
    count, _ = queryset.delete()
    modeladmin.message_user(request, f'{count} log(s) cleared.')
clear_logs.short_description = 'Clear selected logs'

class TimePeriodFilter(admin.SimpleListFilter):

    title = _('Time Period')
    parameter_name = 'time_period'

    def lookups(self, request, model_admin):
        return (
            ('day', _('Day')),
            ('week', _('Week')),
            ('month', _('Month')),
            ('year', _('Year')),
        )

    def queryset(self, request, queryset):
        time_period = self.value()
        now = timezone.now()

        if time_period:
            if time_period == 'day':
                queryset = queryset.filter(timestamp__gte=now - timedelta(hours=24))
            elif time_period == 'week':
                queryset = queryset.filter(timestamp__gte=now - timedelta(days=7))
            elif time_period == 'month':
                queryset = queryset.filter(timestamp__gte=now - timedelta(days=30))
            elif time_period == 'year':
                queryset = queryset.filter(timestamp__gte=now - timedelta(days=365))
        return queryset

class EndpointFilter(admin.SimpleListFilter):
    title = _('Endpoint Type')
    parameter_name = 'endpoint_type'

    def lookups(self, request, model_admin):
        return (
            ('vercel', _('Vercel')),
            ('telegram', _('Telegram')),
        )

    def queryset(self, request, queryset):
        endpoint_types = request.GET.get(self.parameter_name)
        if not endpoint_types:
            return queryset

        endpoint_types = endpoint_types.split(',')
        filters = Q()

        # Apply the filters for both 'vercel' and 'telegram'
        if 'vercel' in endpoint_types:
            filters |= ~Q(endpoint__icontains='by_chat_id')  # Vercel doesn't contain 'by_chat_id'
        if 'telegram' in endpoint_types:
            filters |= Q(endpoint__icontains='by_chat_id')  # Telegram contains 'by_chat_id'
        
        return queryset.filter(filters)

class APILogAdmin(admin.ModelAdmin):
    list_display = ('clickable_endpoint', 'request_count', 'timestamp')
    list_filter = (TimePeriodFilter, EndpointFilter)
    actions = [clear_logs]
    ordering = ('-timestamp',)
    search_fields = ['endpoint']
    change_list_template = 'admin/logs/apilog/change_list.html'
    exclude_patterns = [
        '/admin/logs/apilog/', '/favicon.ico', '/admin/jsi18n/', '/admin/logs/','/admin/login/',
        '/api/health_check', '/api/token/refresh/', '/api/telegram_users/', '/api/logs/chart-data/',
        '/auth/token/login/', '/api/token/', '/admin/api/logs/chart-data/', '/admin/' ,'/'
    ]
    def delete_model(self, request, obj):
        endpoint = obj.endpoint
        super().delete_model(request, obj)
        self.recalculate_request_count(endpoint)

    def recalculate_request_count(self, endpoint):
        count = APILog.objects.filter(endpoint=endpoint).count()
        APILog.objects.filter(endpoint=endpoint).update(request_count=count)


    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if queryset is None:
            queryset = self.model.objects.none()
        endpoint_filter = EndpointFilter(request, {}, self.model, self)
        queryset = endpoint_filter.queryset(request, queryset)
        time_period = request.GET.get('time_period', None)
        if time_period:
            queryset = TimePeriodFilter(request, {}, self.model, self).queryset(request, queryset)
        if self.exclude_patterns:
            queryset = queryset.exclude(endpoint__in=self.exclude_patterns)
        return queryset

    def request_count(self, obj):
        request = self.request
        queryset = self.get_queryset(request)  # Use the combined get_queryset logic
        endpoint = request.GET.get('endpoint')
        if endpoint:
            if endpoint == 'telegram':
                queryset = queryset.filter(Q(endpoint__icontains='by_chat_id'))
            elif endpoint == 'vercel':
                queryset = queryset.filter(~Q(endpoint__icontains='by_chat_id'))
            else:
                queryset = queryset.filter(endpoint=endpoint)
        return queryset.count()

    request_count.short_description = "Request Count"

    def clickable_endpoint(self, obj):
        endpoint = obj.endpoint.lstrip('/') if obj.endpoint else None
        url = reverse('admin:logs_apilog_endpoint_timestamps', args=[endpoint])
        return format_html('<a href="{}">{}</a>', url, obj.endpoint)

    clickable_endpoint.allow_tags = True
    clickable_endpoint.short_description = "Endpoint"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('clear_logs/', self.admin_site.admin_view(self.clear_all_logs), name="clear_all_logs"),
            # Update the URL pattern to allow slashes in the endpoint
            path('endpoint_timestamps/<path:endpoint>/', self.admin_site.admin_view(self.endpoint_timestamps_view), name="logs_apilog_endpoint_timestamps")
        ]
        return custom_urls + urls

    def endpoint_timestamps_view(self, request, endpoint):
        logs = APILog.objects.filter(endpoint=endpoint).order_by('timestamp')
        timestamps = [{'timestamp': log.timestamp} for log in logs]
        context = {
            'title': f'Timestamps for {endpoint}',
            'timestamps': timestamps,
        }
        return self.render_change_form(request, context=context)

    def clear_all_logs(self, request):
        try:
            APILog.objects.all().delete()
            messages.success(request, "All logs have been cleared successfully.")
        except Exception as e:
            messages.error(request, f"Error clearing logs: {str(e)}")
        return HttpResponseRedirect('/admin/logs/apilog/')  # Redirect back to the admin list view


    def filter_logs_by_time_period(self, time_period):
        now = timezone.now()
        if time_period == 'day':
            trunc_field = TruncHour('timestamp')
            time_window = now - timedelta(hours=24)
        elif time_period == 'week':
            trunc_field = TruncHour('timestamp')
            time_window = now - timedelta(days=7)
        elif time_period == 'month':
            trunc_field = TruncHour('timestamp')  # Adjust if needed
            time_window = now - timedelta(days=30)
        elif time_period == 'year':
            trunc_field = TruncHour('timestamp')
            time_window = now - timedelta(days=365)

        logs = APILog.objects.filter(timestamp__gte=time_window).exclude(endpoint__in=self.exclude_patterns)
        if trunc_field:
            logs = logs.annotate(time_period_field=trunc_field)
        return logs


    def get_endpoint_data(self, logs, endpoint_filter, time_period):
        data = logs.filter(endpoint__icontains=endpoint_filter) \
                   .annotate(count=Count('id')) \
                   .values('time_period_field', 'count')

        return {entry['time_period_field']: entry['count'] for entry in data}
    

    def get_charts_data(self, request, time_period):
        selected_endpoints = request.GET.get('endpoint', '').split(',')
        endpoint_filter = EndpointFilter(request, {}, self.model, self)
        logs = self.filter_logs_by_time_period(time_period)
        filtered_logs = endpoint_filter.queryset(request, logs)

        # Separate logs by endpoints (Telegram and Vercel)
        telegram_logs = filtered_logs.filter(Q(endpoint__icontains='by_chat_id'))
        vercel_logs = filtered_logs.filter(~Q(endpoint__icontains='by_chat_id'))

        # Prepare the labels and data
        labels = []
        telegram_values = []
        vercel_values = []

        # Create a list of all timestamps in the filtered logs
        all_logs = list(telegram_logs) + list(vercel_logs)
        all_logs.sort(key=lambda log: log.timestamp)  # Sort by timestamp

        for log in all_logs:
            # Convert timestamp to local time and format it
            local_time = timezone.localtime(log.timestamp)  # Convert to local time
            timestamp_str = local_time.strftime('%Y-%m-%d %H:%M')  # Customize the date format
            labels.append(timestamp_str)

            if 'by_chat_id' in log.endpoint:
                telegram_values.append(1)  # Increment for each request
                vercel_values.append(0)
            else:
                telegram_values.append(0)
                vercel_values.append(1)

        chart_data = {
            "labels": labels,
            "data": {
                "Telegram": telegram_values,
                "Vercel": vercel_values,
            },
        }
        return chart_data

    def changelist_view(self, request, extra_context=None):
        time_period = request.GET.get("time_period", "day")

        # Initialize the EndpointFilter using the request and other necessary parameters
        endpoint_filter = EndpointFilter(request, {}, self.model, self)

        # Define time truncation based on the time period
        if time_period == "day":
            trunc_func = TruncHour  # Truncate by hour for 'day'
            start_time = timezone.localtime(timezone.now()) - relativedelta(hours=24)
            labels_count = 24  # 24 hours in a day
        elif time_period == "week":
            trunc_func = TruncHour  # Truncate by day for 'week'
            start_time = timezone.localtime(timezone.now()) - relativedelta(days=7)
            labels_count = 7  # 7 days in a week
        elif time_period == "month":
            trunc_func = TruncHour # Truncate by day for 'month'
            start_time = timezone.localtime(timezone.now()) - relativedelta(days=30)
            labels_count = 30  # Approximate 30 days in a month
        elif time_period == "year":
            trunc_func = TruncHour  # Truncate by month for 'year'
            start_time = timezone.localtime(timezone.now()) - relativedelta(years=1)
            labels_count = 12  # 12 months in a year

        logs = self.model.objects.all()  # Start with all logs; adjust if needed
        logs = endpoint_filter.queryset(request, logs)
        logs = (
            logs.annotate(period=trunc_func("timestamp"))
            .values("period")
            .annotate(
                Telegram=Count("id", filter=Q(endpoint__icontains="by_chat_id")),
                Vercel=Count("id", filter=~Q(endpoint__icontains="by_chat_id")),
            )
            .order_by("period")
        )

        # Prepare data for Chart.js
        labels = []
        telegram_data = []
        vercel_data = []

        # Generate labels and data based on time period
        if time_period == "day":
            # For 'day' we need to enumerate hours (24 hours)
            for hour in range(labels_count):
                current_hour = (timezone.localtime(timezone.now()) - relativedelta(hours=labels_count - hour - 1)).strftime('%H:%M')
                labels.append(current_hour)

                telegram_data.append(
                    logs.filter(period__hour=(timezone.localtime(timezone.now()) - relativedelta(hours=labels_count - hour + 1)).hour).aggregate(
                        telegram_count=Count("id", filter=Q(endpoint__icontains="by_chat_id"))
                    )["telegram_count"] or 0
                )

                vercel_data.append(
                    logs.filter(period__hour=(timezone.localtime(timezone.now()) - relativedelta(hours=labels_count - hour + 1)).hour).aggregate(
                        vercel_count=Count("id", filter=~Q(endpoint__icontains="by_chat_id"))
                    )["vercel_count"] or 0
                )

        elif time_period == "week":
            for day in range(labels_count):
                # Calculate the current day, starting from today and going back 'labels_count' days
                current_day = (timezone.localtime(timezone.now()) - relativedelta(days=labels_count - day - 1)).strftime('%Y-%m-%d')
                labels.append(current_day)

                # Filter logs for the correct day of the week (current_day)
                telegram_data.append(
                    logs.filter(period__date=(timezone.localtime(timezone.now()) - relativedelta(days=labels_count - day - 1)).date()).aggregate(
                        telegram_count=Count("id", filter=Q(endpoint__icontains="by_chat_id"))
                    )["telegram_count"] or 0
                )

                vercel_data.append(
                    logs.filter(period__date=(timezone.localtime(timezone.now()) - relativedelta(days=labels_count - day - 1)).date()).aggregate(
                        vercel_count=Count("id", filter=~Q(endpoint__icontains="by_chat_id"))
                    )["vercel_count"] or 0
                )


        elif time_period == "month":
            for day in range(labels_count):
                current_day = (timezone.localtime(timezone.now()) - relativedelta(days=labels_count - day - 1)).strftime('%Y-%m-%d')
                labels.append(current_day)
                telegram_data.append(
                    logs.filter(period__day=(timezone.localtime(timezone.now()) - relativedelta(days=labels_count - day - 1)).day).aggregate(
                        telegram_count=Count("id", filter=Q(endpoint__icontains="by_chat_id"))
                    )["telegram_count"] or 0
                )
                vercel_data.append(
                    logs.filter(period__day=(timezone.localtime(timezone.now()) - relativedelta(days=labels_count - day - 1)).day).aggregate(
                        vercel_count=Count("id", filter=~Q(endpoint__icontains="by_chat_id"))
                    )["vercel_count"] or 0
                )


        elif time_period == "year":
            # For 'year' we need to enumerate months of the year (12 months)
            for month in range(labels_count):
                current_month = (timezone.localtime(timezone.now()) - relativedelta(years=0, months=labels_count - month - 1)).strftime('%B')
                labels.append(current_month)

                telegram_data.append(
                    logs.filter(period__month=(timezone.localtime(timezone.now()) - relativedelta(years=0, months=labels_count - month - 1)).month).aggregate(
                        telegram_count=Count("id", filter=Q(endpoint__icontains="by_chat_id"))
                    )["telegram_count"] or 0
                )

                vercel_data.append(
                    logs.filter(period__month=(timezone.localtime(timezone.now()) - relativedelta(years=0, months=labels_count - month - 1)).month).aggregate(
                        vercel_count=Count("id", filter=~Q(endpoint__icontains="by_chat_id"))
                    )["vercel_count"] or 0
                )                                                                   

        # Prepare final chart data
        chart_data = {
            "labels": labels,
            "data": {
                "Telegram": telegram_data,
                "Vercel": vercel_data,
            },
        }

        extra_context = extra_context or {}
        extra_context["chart_js"] = chart_data

        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(APILog, APILogAdmin)
