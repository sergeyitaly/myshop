from django.contrib import admin
from django.db.models import Count, Max
from django.utils import timezone
from django.urls import path, reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from logs.models import APILog, IgnoreEndpoint
from datetime import timedelta
from django.db.models.functions import TruncHour, TruncDate, TruncMonth, TruncYear, TruncDay, TruncWeek
from django.utils.translation import gettext as _
from django.utils.dateparse import parse_datetime
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta
from django.utils.html import format_html
from django.db.models import Min, Max, F, OuterRef, Subquery, Sum
from django.conf import settings
from django.db.models import Case, When, Value, F, Q, Count
from django.db.models.functions import Substr, Length
import re


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
            ('localhost', _('Localhost')),
            ('docker', _('Docker')),
            ('android', _('Android')),
        )

    def queryset(self, request, queryset):
        endpoint_types = request.GET.get(self.parameter_name)
        if not endpoint_types:
            return queryset

        endpoint_types = set(endpoint_types.split(','))  # Use a set for efficient checks
        filters = Q()
        android_domain = re.sub(r'^https?://', '', settings.VERCEL_DOMAIN).lower() if hasattr(settings, "VERCEL_DOMAIN") else ""
        vercel_domain = settings.VERCEL_DOMAIN if hasattr(settings, "VERCEL_DOMAIN") else ""

        type_conditions = {
            'vercel': Q(endpoint__icontains=vercel_domain) & ~Q(endpoint__icontains="by_chat_id"),
            'localhost': Q(endpoint__icontains=':8000') & ~Q(endpoint__icontains="by_chat_id"),
            'docker': Q(endpoint__icontains=':8010') & ~Q(endpoint__icontains="by_chat_id"),
            'telegram': Q(endpoint__icontains='by_chat_id'),
            'android': Q(endpoint__icontains=android_domain) & ~Q(endpoint__icontains="by_chat_id")&~Q(endpoint__icontains=vercel_domain),
        }

        # Add filters for all selected endpoint types
        for endpoint_type, condition in type_conditions.items():
            if endpoint_type in endpoint_types:
                filters |= condition

        return queryset.filter(filters)


class IgnoreEndpointAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active_display')  # Display name and a clickable "is_active" toggle
    search_fields = ('name',)

    def is_active_display(self, obj):
        """Displays the is_active field as clickable toggle links."""
        if obj.is_active:
            return format_html(
                '<a href="{}" style="color: green;">Active</a>',
                f"{obj.id}/toggle_active/"
            )
        else:
            return format_html(
                '<a href="{}" style="color: red;">Inactive</a>',
                f"{obj.id}/toggle_active/"
            )

    is_active_display.short_description = "Active Status"
    is_active_display.admin_order_field = 'is_active'

    def get_urls(self):
        """Add custom admin URLs for toggling the is_active status."""
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:pk>/toggle_active/',
                self.admin_site.admin_view(self.toggle_active),
                name='toggle_active',
            ),
        ]
        return custom_urls + urls

    def toggle_active(self, request, pk):
        """Toggle the is_active field for a specific IgnoreEndpoint instance."""
        obj = self.get_object(request, pk)
        if obj:
            obj.is_active = not obj.is_active
            obj.save()
            self.message_user(
                request,
                f"Successfully updated {obj.name}'s status to {'Active' if obj.is_active else 'Inactive'}."
            )
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/admin/'))


class APILogAdmin(admin.ModelAdmin):
    list_display = ('id','clickable_endpoint', 'host_type', 'request_sum', 'timestamp')
    list_filter = (TimePeriodFilter, EndpointFilter)
    actions = [clear_logs, 'add_to_ignore_list','delete_last_log', 'delete_all_logs']
    ordering = ('-timestamp',)
    search_fields = ('endpoint',)
    change_list_template = 'admin/logs/apilog/change_list.html'


    def host_type(self, obj):
        endpoint = obj.endpoint.lower()
        android_domain = re.sub(r'^https?://', '', settings.VERCEL_DOMAIN).lower() if hasattr(settings, "VERCEL_DOMAIN") else ""
        vercel_domain = settings.VERCEL_DOMAIN if hasattr(settings, "VERCEL_DOMAIN") else ""

        if vercel_domain in endpoint and 'by_chat_id' not in endpoint:
            return 'Vercel'
        elif 'by_chat_id' in endpoint:
            return 'Telegram'
        elif ':8000' in endpoint and 'by_chat_id' not in endpoint:
            return 'Localhost'
        elif ':8010' in endpoint and 'by_chat_id' not in endpoint:
            return 'Docker'
        elif android_domain in endpoint and vercel_domain not in endpoint:
            return 'Android'
        return 'Unknown'  # Default if no pattern matches

    host_type.short_description = "Host Type"


    def get_queryset(self, request):
        # Get a list of endpoint patterns to exclude (active ignore patterns)
        exclude_patterns = list(IgnoreEndpoint.objects.filter(is_active=True).values_list('name', flat=True))

        # Get the initial queryset
        queryset = super().get_queryset(request)

        # Apply any endpoint filters
        endpoint_filter = EndpointFilter(request, {}, self.model, self)
        queryset = endpoint_filter.queryset(request, queryset)

        # Apply time period filters
        time_period_filter = TimePeriodFilter(request, {}, self.model, self)
        queryset = time_period_filter.queryset(request, queryset)

        # Apply exclusions based on the ignore patterns
        if exclude_patterns:
            exclude_q = Q()
            for pattern in exclude_patterns:
                if pattern == '/':
                    exclude_q |= Q(endpoint='/')
                else:
                    exclude_q |= Q(endpoint__icontains=pattern)
            queryset = queryset.exclude(exclude_q)
        #queryset.values('endpoint').distinct('endpoint').order_by('endpoint', '-timestamp')
        return queryset
    
    def get_chart_queryset(self, request):
        exclude_patterns = list(IgnoreEndpoint.objects.filter(is_active=True).values_list('name', flat=True))
        queryset = super().get_queryset(request)
        endpoint_filter = EndpointFilter(request, {}, self.model, self)
        queryset = endpoint_filter.queryset(request, queryset)
        time_period_filter = TimePeriodFilter(request, {}, self.model, self)
        queryset = time_period_filter.queryset(request, queryset)
        if exclude_patterns:
            exclude_q = Q()
            for pattern in exclude_patterns:
                if pattern == '/':
                    exclude_q |= Q(endpoint='/')
                else:
                    exclude_q |= Q(endpoint__icontains=pattern)
            queryset = queryset.exclude(exclude_q)
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
#    def request_sum(self, obj): 
#        return obj.total_requests
#        return obj.request_count
    
    def add_to_ignore_list(self, request, queryset):
        endpoints = queryset.values_list('endpoint', flat=True).distinct()
        added_endpoints = 0
        for endpoint in endpoints:
            if not IgnoreEndpoint.objects.filter(name=endpoint).exists():
                IgnoreEndpoint.objects.create(name=endpoint, is_active=True)
                added_endpoints += 1

        self.message_user(request, f'{added_endpoints} endpoints were successfully added to the Ignore list.')

    add_to_ignore_list.short_description = "Add selected endpoints to Ignore list"

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
        APILog.objects.filter(endpoint=endpoint).update(request_sum=count)

    def clickable_endpoint(self, obj):
        # Normalize the domain from settings (remove scheme like http:// or https://)
        android_domain = re.sub(r'^https?://', '', settings.VERCEL_DOMAIN).lower() if hasattr(settings, "VERCEL_DOMAIN") else ""
        vercel_domain = settings.VERCEL_DOMAIN if hasattr(settings, "VERCEL_DOMAIN") else ""
        base_url_patterns = [
            vercel_domain,
            android_domain,
            'localhost:8000',
            'localhost:8010',
            '127.0.0.1:8000',
            '127.0.0.1:8010',            
        ]

        # Normalize the endpoint by stripping the base URL
        endpoint = obj.endpoint
        for base_url in base_url_patterns:
            if base_url and endpoint.startswith(base_url):  # Ensure base_url is not empty
                endpoint = endpoint[len(base_url):]  # Strip the base URL from the endpoint
                break

        # Generate the admin URL with a query filter for the endpoint
        url = reverse('admin:logs_apilog_changelist') + f'?endpoint={obj.endpoint}'
        return format_html('<a href="{}">{}</a>', url, endpoint)

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
        logs = self.get_chart_queryset(request)
        labels, telegram_data, vercel_data, localhost_data, docker_data, android_data = [], [], [], [], [], []
        now = timezone.localtime(timezone.now())
        endpoint_filter = request.GET.get('endpoint', '')
        android_domain = re.sub(r'^https?://', '', settings.VERCEL_DOMAIN).lower() if hasattr(settings, "VERCEL_DOMAIN") else ""
        vercel_domain = settings.VERCEL_DOMAIN if hasattr(settings, "VERCEL_DOMAIN") else ""

        if time_period == "day":
            trunc_func = TruncHour  # Truncate by hour for 'day'
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
        if endpoint_filter:
            logs = logs.filter(endpoint__icontains=endpoint_filter)  # Apply endpoint filter
        else:
            logs = logs

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
                        vercel_count=Count("id", filter=Q(endpoint__icontains=vercel_domain)& ~Q(endpoint__icontains="by_chat_id"))
                    )["vercel_count"] or 0
                )
                localhost_data.append(
                    logs.filter(
                        timestamp__gte=start_time,
                        timestamp__hour=(now - timedelta(hours=labels_count - hour - 1)).hour
                    ).aggregate(
                        localhost_count=Count("id", filter=Q(endpoint__icontains=":8000")&~Q(endpoint__icontains="by_chat_id"))
                    )["localhost_count"] or 0
                )
                docker_data.append(
                    logs.filter(
                        timestamp__gte=start_time,
                        timestamp__hour=(now - timedelta(hours=labels_count - hour - 1)).hour
                    ).aggregate(
                        docker_count=Count("id", filter=Q(endpoint__icontains=":8010")&~Q(endpoint__icontains="by_chat_id"))
                    )["docker_count"] or 0
                )
                android_data.append(
                    logs.filter(
                        timestamp__gte=start_time,
                        timestamp__hour=(now - timedelta(hours=labels_count - hour - 1)).hour
                    ).aggregate(
                        android_count=Count("id", filter=Q(endpoint__icontains=android_domain)&~Q(endpoint__icontains=vercel_domain)&~Q(endpoint__icontains="by_chat_id"))
                    )["android_count"] or 0
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
                        vercel_count=Count("id", filter=Q(endpoint__icontains=vercel_domain)& ~Q(endpoint__icontains="by_chat_id"))
                    )["vercel_count"] or 0
                )
                localhost_data.append(
                    logs.filter(period__date=(now - relativedelta(days=labels_count - day - 1)).date()).aggregate(
                        localhost_count=Count("id", filter=Q(endpoint__icontains=":8000")&~Q(endpoint__icontains="by_chat_id"))
                    )["localhost_count"] or 0
                )
                docker_data.append(
                    logs.filter(period__date=(now - relativedelta(days=labels_count - day - 1)).date()).aggregate(
                        docker_count=Count("id", filter=Q(endpoint__icontains=":8010")&~Q(endpoint__icontains="by_chat_id"))
                    )["docker_count"] or 0
                )
                android_data.append(
                    logs.filter(period__date=(now - relativedelta(days=labels_count - day - 1)).date()).aggregate(
                        android_count=Count("id", filter=Q(endpoint__icontains=android_domain)&~Q(endpoint__icontains=vercel_domain)&~Q(endpoint__icontains="by_chat_id"))
                    )["android_count"] or 0
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
                        vercel_count=Count("id", filter=Q(endpoint__icontains=vercel_domain)& ~Q(endpoint__icontains="by_chat_id"))
                    )["vercel_count"] or 0
                )
                localhost_data.append(
                    logs.filter(period__day=(now - relativedelta(days=labels_count - day - 1)).day).aggregate(
                        localhost_count=Count("id", filter=Q(endpoint__icontains=":8000")&~Q(endpoint__icontains="by_chat_id"))
                    )["localhost_count"] or 0
                )
                docker_data.append(
                    logs.filter(period__day=(now - relativedelta(days=labels_count - day - 1)).day).aggregate(
                        docker_count=Count("id", filter=Q(endpoint__icontains=":8010")&~Q(endpoint__icontains="by_chat_id"))
                    )["docker_count"] or 0
                )
                android_data.append(
                    logs.filter(period__day=(now - relativedelta(days=labels_count - day - 1)).day).aggregate(
                        android_count=Count("id", filter=Q(endpoint__icontains=android_domain)&~Q(endpoint__icontains=vercel_domain)&~Q(endpoint__icontains="by_chat_id"))
                    )["android_count"] or 0
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
                        vercel_count=Count("id", filter=Q(endpoint__icontains=vercel_domain)& ~Q(endpoint__icontains="by_chat_id"))
                    )["vercel_count"] or 0
                )
                localhost_data.append(
                    logs.filter(period__month=(now - relativedelta(months=labels_count - month - 1)).month).aggregate(
                        localhost_count=Count("id", filter=Q(endpoint__icontains=":8000")&~Q(endpoint__icontains="by_chat_id"))
                    )["localhost_count"] or 0
                )
                docker_data.append(
                    logs.filter(period__month=(now - relativedelta(months=labels_count - month - 1)).month).aggregate(
                        docker_count=Count("id", filter=Q(endpoint__icontains=":8010")&~Q(endpoint__icontains="by_chat_id"))
                    )["docker_count"] or 0
                )
                android_data.append(
                    logs.filter(period__month=(now - relativedelta(months=labels_count - month - 1)).month).aggregate(
                        android_count=Count("id", filter=Q(endpoint__icontains=android_domain)&~Q(endpoint__icontains=vercel_domain)&~Q(endpoint__icontains="by_chat_id"))
                    )["android_count"] or 0
                )
                
        chart_data = {
            "labels": labels,
            "data": {
                "Telegram": telegram_data,
                "Vercel": vercel_data,
                "Localhost": localhost_data,
                "Docker": docker_data,
                "Android": android_data,

            },
        }
        return chart_data


    def changelist_view(self, request, extra_context=None):
        time_period = request.GET.get("time_period", "day")
        chart_data = self.get_charts_data(request, time_period)
        extra_context = extra_context or {}
        extra_context["chart_js"] = chart_data
        extra_context["selected_endpoint"] = request.GET.get("endpoint", "")  # Add selected endpoint to context

        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(APILog, APILogAdmin)
admin.site.register(IgnoreEndpoint, IgnoreEndpointAdmin)
