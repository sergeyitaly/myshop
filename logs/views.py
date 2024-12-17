from django.http import JsonResponse
from django.db.models import Count
from django.views.decorators.cache import never_cache
from .models import APILog


@never_cache
def endpoint_statistics_view(request):
    endpoint = request.GET.get('endpoint')
    
    if endpoint:
        endpoint_data = APILog.objects.filter(endpoint=endpoint).values('endpoint').annotate(visit_count=Count('id')).order_by('-visit_count')
    else:
        endpoint_data = APILog.objects.values('endpoint').annotate(visit_count=Count('id')).order_by('-visit_count')

    # Prepare data for the chart
    data = {
        'labels': [entry['endpoint'] for entry in endpoint_data],  # Extract labels (endpoint names)
        'data': {
            'Visits': [entry['visit_count'] for entry in endpoint_data],  # Visits data for chart
        }
    }

    return JsonResponse(data)
