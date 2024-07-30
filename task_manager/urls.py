from django.urls import path

from task_manager.views import (
    index,
    TaskCreateView,
    TaskListView,
    TaskDetailView,
    TaskUpdateView,
    WorkerListView,
    WorkerDetailView,
    WorkerCreateView,
    PositionListView,
    PositionDetailView,
    PositionCreateView,
    PositionUpdateView,
    PositionDeleteView,
    WorkerUpdateView,
    WorkerDeleteView,
    CompletedTaskListView,
    TaskTypeListView,
    TaskTypeCreateView,
    TaskDeleteView,
    UserTaskListView,
    TaskTypeDeleteView,
    ProjectCreateView,
    TeamCreateView
)

urlpatterns = [
    path("", index, name="index"),
    path("tasks/assigned/", UserTaskListView.as_view(), name="user-tasks"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path(
        "tasks/<int:pk>/update/",
        TaskUpdateView.as_view(),
        name="task-update"
    ),
    path(
        "tasks/<int:pk>/delete/",
        TaskDeleteView.as_view(),
        name="task-delete"
    ),
    path(
        "completed-tasks/",
        CompletedTaskListView.as_view(),
        name="completed-task-list"
    ),

    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path(
        "workers/<int:pk>/",
        WorkerDetailView.as_view(),
        name="worker-detail"
    ),
    path("workers/create/", WorkerCreateView.as_view(), name="worker-create"),
    path(
        "workers/<int:pk>/update/",
        WorkerUpdateView.as_view(),
        name="worker-update"
    ),
    path(
        "workers/<int:pk>/delete/",
        WorkerDeleteView.as_view(),
        name="worker-delete"
    ),

    path("positions/", PositionListView.as_view(), name="position-list"),
    path(
        "positions/<int:pk>/",
        PositionDetailView.as_view(),
        name="position-detail"
    ),
    path(
        "positions/create/",
        PositionCreateView.as_view(),
        name="position-create"
    ),
    path(
        "positions/<int:pk>/update/",
        PositionUpdateView.as_view(),
        name="position-update"
    ),
    path(
        "positions/<int:pk>/delete/",
        PositionDeleteView.as_view(),
        name="position-delete"
    ),

    path("task_types/", TaskTypeListView.as_view(), name="task-type-list"),
    path(
        "task_types/create/",
        TaskTypeCreateView.as_view(),
        name="task-type-create"
    ),
    path(
        "task_types/<int:pk>/delete/",
        TaskTypeDeleteView.as_view(),
        name="task-type-delete"),

    path(
        "project/create/",
        ProjectCreateView.as_view(),
        name="project-create"
    ),
    path("team/create/", TeamCreateView.as_view(), name="team-create"),
]

app_name = "task_manager"
