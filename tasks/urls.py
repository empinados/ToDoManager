from django.urls import path
from . import views

app_name = "tasks"

urlpatterns = [
    path("", views.project_list, name="project_list"),
    path("projects/create/", views.create_project, name="create_project"),
    path("tasks/", views.all_tasks, name="all_tasks"),
    path("project/<int:project_id>/", views.project_detail, name="project_detail"),
    path("project/<int:project_id>/add-task/", views.add_task, name="add_task"),
    path("project/<int:project_id>/delete/", views.delete_project, name="delete_project"),
    path("task/<int:task_id>/toggle/", views.toggle_task, name="toggle_task"),
    path("task/<int:task_id>/delete/", views.delete_task, name="delete_task"),
]