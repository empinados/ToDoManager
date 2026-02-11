from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.http import HttpResponse

from .models import Project, Task


def project_list(request):
    projects = (
        Project.objects.annotate(
            total_tasks=Count("tasks"),
            done_tasks=Count("tasks", filter=Q(tasks__is_done=True)),
        )
        .all()
    )
    return render(request, "tasks/project_list.html", {"projects": projects})


@require_POST
def create_project(request):
    name = request.POST.get("name", "").strip()
    if name:
        Project.objects.create(name=name)
    return redirect("tasks:project_list")


def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    tasks = project.tasks.all()
    done_count = project.tasks.filter(is_done=True).count()
    total_count = project.tasks.count()
    progress = int((done_count / total_count) * 100) if total_count else 0

    return render(
        request,
        "tasks/project_detail.html",
        {
            "project": project,
            "tasks": tasks,
            "done_count": done_count,
            "total_count": total_count,
            "progress": progress,
        },
    )


def all_tasks(request):
    tasks = Task.objects.select_related("project").all()
    done_count = Task.objects.filter(is_done=True).count()
    total_count = Task.objects.count()
    progress = int((done_count / total_count) * 100) if total_count else 0

    return render(
        request,
        "tasks/all_tasks.html",
        {"tasks": tasks, "done_count": done_count, "total_count": total_count, "progress": progress},
    )


@require_POST
def add_task(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    title = request.POST.get("title", "").strip()
    if title:
        Task.objects.create(project=project, title=title, is_done=False)
    return redirect("tasks:project_detail", project_id=project.id)


@require_POST
def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.is_done = not task.is_done
    task.save()
    return redirect("tasks:project_detail", project_id=task.project.id)


@require_POST
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    project_id = task.project.id
    task.delete()
    return redirect("tasks:project_detail", project_id=project_id)


@require_POST
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.delete()
    return redirect("tasks:project_list")

