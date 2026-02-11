from django.db.models import Count, Q
from rest_framework.viewsets import ModelViewSet

from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.annotate(
        total_tasks=Count("tasks"),
        done_tasks=Count("tasks", filter=Q(tasks__is_done=True)),
    ).order_by("-created_at", "id")
    serializer_class = ProjectSerializer


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.select_related("project").order_by("is_done", "-created_at", "id")
    serializer_class = TaskSerializer