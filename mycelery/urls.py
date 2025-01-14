from django.urls import include, path
from mycelery.views import *

urlpatterns = [
    path('mycelery/', RunScheduledTasks.as_view(), name='mycelery-tasks'),
]
