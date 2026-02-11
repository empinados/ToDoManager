from rest_framework import serializers
from .models import Project, Task


class ProjectSerializer(serializers.ModelSerializer):
    total_tasks = serializers.IntegerField(read_only=True)
    done_tasks = serializers.IntegerField(read_only=True)

    class Meta:
        model = Project
        fields = ["id", "name", "created_at", "total_tasks", "done_tasks"]


class TaskSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source="project.name", read_only=True)

    class Meta:
        model = Task
        fields = ["id", "project", "project_name", "title", "is_done", "created_at"]