from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.db.models import Count
from .models import APILog  # Replace with actual model
from django.utils import timezone
from datetime import timedelta

def index(request):
    return HttpResponse("Hello, this is the logs app!")

def endpoint_statistics_view(request):
    endpoint_data = APILog.objects.values('endpoint').annotate(visit_count=Count('id')).order_by('-visit_count')
    
    context = {
        'endpoint_statistics': endpoint_data
    }
    return render(request, 'admin/logs/apilog/change_list.html', context)

