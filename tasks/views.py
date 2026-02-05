from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .models import Project, Task


def project_list(request):
    projects = Project.objects.all()
    return render(request, "tasks/project_list.html", {"projects": projects})


def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    tasks = project.tasks.all().order_by("is_done", "id")
    done_count = project.tasks.filter(is_done=True).count()
    total_count = project.tasks.count()

    return render(
        request,
        "tasks/project_detail.html",
        {"project": project, "tasks": tasks, "done_count": done_count, "total_count": total_count},
    )


def all_tasks(request):
    tasks = Task.objects.select_related("project").all().order_by("is_done", "id")
    return render(request, "tasks/all_tasks.html", {"tasks": tasks})


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
