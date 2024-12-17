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
from django.db.models import Min, Max, F, OuterRef, Subquery, Sum

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
        if 'vercel' in endpoint_types:
            filters |= ~Q(endpoint__icontains='by_chat_id')  # Vercel doesn't contain 'by_chat_id'
        if 'telegram' in endpoint_types:
            filters |= Q(endpoint__icontains='by_chat_id')  # Telegram contains 'by_chat_id'
        
        return queryset.filter(filters)

class APILogAdmin(admin.ModelAdmin):
    list_display = ('clickable_endpoint', 'request_sum', 'timestamp')
    list_filter = (TimePeriodFilter, EndpointFilter)
    actions = [clear_logs, 'delete_last_log', 'delete_all_logs']
    ordering = ('-timestamp',)
    search_fields = ['endpoint']
    change_list_template = 'admin/logs/apilog/change_list.html'
    exclude_patterns = [
        '/admin/logs/apilog/', '/favicon.ico', '/admin/jsi18n/', '/admin/logs/','/admin/login/',
        '/api/health_check', '/api/token/refresh/', '/api/telegram_users','/api/telegram_users/', '/api/telegram_user/',
        '/api/logs/chart-data/', '/auth/token/login/', '/api/token/', '/admin/api/logs/chart-data/', '/', '/admin/'
    ]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        endpoint_filter = EndpointFilter(request, {}, self.model, self)
        queryset = endpoint_filter.queryset(request, queryset)
        time_period_filter = TimePeriodFilter(request, {}, self.model, self)
        queryset = time_period_filter.queryset(request, queryset)
        if self.exclude_patterns:
            exclude_q = ~Q(endpoint__in=self.exclude_patterns)
            queryset = queryset.filter(exclude_q)
        latest_timestamps = APILog.objects.filter(
            endpoint=OuterRef('endpoint')
        ).order_by('-timestamp')
        queryset = queryset.annotate(
            total_requests=Sum('request_count'),
            latest_timestamp=Subquery(latest_timestamps.values('timestamp')[:1]),
            max_timestamp=Max('timestamp')
        ).order_by('endpoint') 

        
        return queryset

    def latest_timestamp(self, obj):
        return obj.latest_timestamp
    def request_sum(self, obj): 
        return obj.total_requests
    
    def get_chart_queryset(self, request):
        queryset = super().get_queryset(request)
        time_period = request.GET.get('time_period', None)
        if time_period:
            queryset = TimePeriodFilter(request, {}, self.model, self).queryset(request, queryset)
        if self.exclude_patterns:
            exclude_q = ~Q(endpoint__in=self.exclude_patterns)
            queryset = queryset.filter(exclude_q)
        queryset = queryset.annotate(
            total_requests=Sum('request_count'),
            latest_timestamp=Max('timestamp')
        ).order_by('-latest_timestamp')
        endpoint_filter = EndpointFilter(request, {}, self.model, self)
        filtered_queryset = endpoint_filter.queryset(request, queryset)
        return filtered_queryset
    
    def delete_last_log(self, request, queryset):
        endpoints = queryset.values_list('endpoint', flat=True).distinct()
        rows_deleted = 0
        for endpoint in endpoints:
            latest_log = queryset.filter(endpoint=endpoint).order_by('-timestamp').first()
            if latest_log:
                latest_log.delete()
                rows_deleted += 1
                self.recalculate_request_count(endpoint)
        self.message_user(request, f'{rows_deleted} logs were successfully deleted.')

    def delete_all_logs(self, request, queryset):
        endpoints = queryset.values_list('endpoint', flat=True).distinct()
        rows_deleted = 0
        for endpoint in endpoints:
            rows_deleted += APILog.objects.filter(endpoint=endpoint).delete()[0]
        for endpoint in endpoints:
            self.recalculate_request_count(endpoint)
        self.message_user(request, f'{rows_deleted} logs were successfully deleted.')

    def recalculate_request_count(self, endpoint):
        count = APILog.objects.filter(endpoint=endpoint).count()
        APILog.objects.filter(endpoint=endpoint).update(request_count=count)

    def clickable_endpoint(self, obj):
        url = reverse('admin:logs_apilog_changelist') + f'?endpoint={obj.endpoint}'
        return format_html('<a href="{}">{}</a>', url, obj.endpoint)
    clickable_endpoint.allow_tags = True
    clickable_endpoint.short_description = "Endpoint"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('clear_logs/', self.admin_site.admin_view(self.clear_all_logs), name="clear_all_logs")
        ]
        return custom_urls + urls

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
        logs = self.get_queryset(request)
        labels, telegram_data, vercel_data = [], [], []
        now = timezone.localtime(timezone.now())

        if time_period == "day":
            trunc_func = TruncDay  # Truncate by hour for 'day'
            start_time = now - relativedelta(hours=24)
            labels_count = 24  # 24 hours in a day
        elif time_period == "week":
            trunc_func = TruncHour  # Truncate by date for 'week'
            start_time = now - relativedelta(weeks=1)
            labels_count = 7  # 7 days in a week
        elif time_period == "month":
            trunc_func = TruncHour  # Truncate by date for 'month'
            start_time = now - relativedelta(days=30)  # Approximate 30 days in a month
            labels_count = 30  # Approximate 30 days in a month
        elif time_period == "year":
            trunc_func = TruncHour  # Truncate by month for 'year'
            start_time = now - relativedelta(years=1)
            labels_count = 12  # 12 months in a year
        logs = logs.annotate(period=trunc_func("timestamp"))
        
        if time_period == "day":
            for hour in range(labels_count):
                current_hour = (now - timedelta(hours=labels_count - hour - 1)).strftime('%H:%M')
                labels.append(current_hour)

                # Filter logs by hour for Telegram data
                telegram_data.append(
                    logs.filter(
                        timestamp__gte=start_time,
                        timestamp__hour=(now - timedelta(hours=labels_count - hour - 1)).hour
                    ).aggregate(
                        telegram_count=Count("id", filter=Q(endpoint__icontains="by_chat_id"))
                    )["telegram_count"] or 0
                )
                vercel_data.append(
                    logs.filter(
                        timestamp__gte=start_time,
                        timestamp__hour=(now - timedelta(hours=labels_count - hour - 1)).hour
                    ).aggregate(
                        vercel_count=Count("id", filter=~Q(endpoint__icontains="by_chat_id"))
                    )["vercel_count"] or 0
                )

        elif time_period == "week":
            for day in range(labels_count):
                current_day = (now - relativedelta(days=labels_count - day - 1)).strftime('%Y-%m-%d')
                labels.append(current_day)

                # Filter logs by day for Telegram data
                telegram_data.append(
                    logs.filter(period__date=(now - relativedelta(days=labels_count - day - 1)).date()).aggregate(
                        telegram_count=Count("id", filter=Q(endpoint__icontains="by_chat_id"))
                    )["telegram_count"] or 0
                )
                vercel_data.append(
                    logs.filter(period__date=(now - relativedelta(days=labels_count - day - 1)).date()).aggregate(
                        vercel_count=Count("id", filter=~Q(endpoint__icontains="by_chat_id"))
                    )["vercel_count"] or 0
                )

        elif time_period == "month":
            for day in range(labels_count):
                current_day = (now - relativedelta(days=labels_count - day - 1)).strftime('%Y-%m-%d')
                labels.append(current_day)
                telegram_data.append(
                    logs.filter(period__day=(now - relativedelta(days=labels_count - day - 1)).day).aggregate(
                        telegram_count=Count("id", filter=Q(endpoint__icontains="by_chat_id"))
                    )["telegram_count"] or 0
                )
                vercel_data.append(
                    logs.filter(period__day=(now - relativedelta(days=labels_count - day - 1)).day).aggregate(
                        vercel_count=Count("id", filter=~Q(endpoint__icontains="by_chat_id"))
                    )["vercel_count"] or 0
                )

        elif time_period == "year":
            for month in range(labels_count):
                current_month = (now - relativedelta(months=labels_count - month - 1)).strftime('%B')
                labels.append(current_month)
                telegram_data.append(
                    logs.filter(period__month=(now - relativedelta(months=labels_count - month - 1)).month).aggregate(
                        telegram_count=Count("id", filter=Q(endpoint__icontains="by_chat_id"))
                    )["telegram_count"] or 0
                )
                vercel_data.append(
                    logs.filter(period__month=(now - relativedelta(months=labels_count - month - 1)).month).aggregate(
                        vercel_count=Count("id", filter=~Q(endpoint__icontains="by_chat_id"))
                    )["vercel_count"] or 0
                )

        chart_data = {
            "labels": labels,
            "data": {
                "Telegram": telegram_data,
                "Vercel": vercel_data,
            },
        }
        return chart_data


    def changelist_view(self, request, extra_context=None):
        time_period = request.GET.get("time_period", "day")
        chart_data = self.get_charts_data(request, time_period)
        extra_context = extra_context or {}
        extra_context["chart_js"] = chart_data
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(APILog, APILogAdmin)
