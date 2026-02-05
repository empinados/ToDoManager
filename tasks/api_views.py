from rest_framework.viewsets import ModelViewSet
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer

class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all().order_by("id")
    serializer_class = ProjectSerializer

class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all().order_by("id")
    serializer_class = TaskSerializer
