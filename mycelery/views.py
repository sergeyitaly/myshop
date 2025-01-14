from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from mycelery.models import ScheduledTask

class RunScheduledTasks(APIView):
    permission_classes = [AllowAny]  
    def get(self, request):
        tasks = ScheduledTask.objects.all()
        for task in tasks:
            task.run_task()
        return Response({"status": "Tasks checked and updated"})
