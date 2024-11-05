from django.contrib import admin
from django.db.models import Count
from .models import APILog

class APILogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'source', 'endpoint', 'method', 'chat_id', 'command')
    list_filter = ('source', 'method', 'timestamp')  # Allows filtering by source, method, and timestamp
    search_fields = ('endpoint', 'command', 'chat_id')  # Adds search functionality
    date_hierarchy = 'timestamp'

    def changelist_view(self, request, extra_context=None):
        # Group logs by day and source
        data_by_day_telegram = (
            APILog.objects
            .filter(source='telegram')  # Ensure this matches your logging source exactly
            .extra(select={'day': "date(timestamp)"})
            .values('day')
            .annotate(count=Count('id'))
            .order_by('-day')
        )

        data_by_day_vercel = (
            APILog.objects
            .filter(source='vercel')  # Ensure this matches your logging source exactly
            .extra(select={'day': "date(timestamp)"})
            .values('day')
            .annotate(count=Count('id'))
            .order_by('-day')
        )

        # Extract dates and counts for each source
        days_telegram = [entry['day'].strftime('%Y-%m-%d') for entry in data_by_day_telegram]
        counts_telegram = [entry['count'] for entry in data_by_day_telegram]

        days_vercel = [entry['day'].strftime('%Y-%m-%d') for entry in data_by_day_vercel]
        counts_vercel = [entry['count'] for entry in data_by_day_vercel]

        # Add data to context
        extra_context = extra_context or {}
        extra_context['days_telegram'] = days_telegram
        extra_context['counts_telegram'] = counts_telegram
        extra_context['days_vercel'] = days_vercel
        extra_context['counts_vercel'] = counts_vercel

        return super().changelist_view(request, extra_context=extra_context)

# Register the APILog model with the custom admin view
admin.site.register(APILog, APILogAdmin)
