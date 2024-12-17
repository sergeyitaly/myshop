from django.urls import path
from . import views
from .views import *

urlpatterns = [
#    path('admin/logs/apilog/chart-data/', get_chart_data, name='chart-data'),
    path('endpoint_statistics/', views.endpoint_statistics_view, name='endpoint_statistics'),
]