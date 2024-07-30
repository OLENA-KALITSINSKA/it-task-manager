# Standard library imports
from datetime import datetime, timedelta

# Django imports
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

# Local application imports
from task_manager.forms import (
    TaskForm,
    WorkerCreationForm,
    WorkerSearchForm,
    TaskSearchForm,
    TeamForm
)
from task_manager.models import (
    Task,
    TaskType,
    Position,
    Worker,
    Project,
    Team
)


@login_required
def index(request):
    """View function for the home page of the site."""
    num_task = Task.objects.count()
    num_worker = Worker.objects.count()
    num_position = Position.objects.count()
    num_projects = Project.objects.count()
    num_completed_tasks = Task.objects.filter(is_completed=True).count()
    num_incomplete_tasks = Task.objects.filter(is_completed=False).count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_task": num_task,
        "num_worker": num_worker,
        "num_position": num_position,
        "num_projects": num_projects,
        "num_completed_tasks": num_completed_tasks,
        "num_incomplete_tasks": num_incomplete_tasks,
        "num_visits": num_visits + 1,
    }

    return render(request, "task_manager/index.html", context=context)


class UserTaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "task_manager/user_tasks.html"
    context_object_name = "user_task_list"

    def get_queryset(self):
        return Task.objects.filter(assignees=self.request.user).order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        deadline_warning_date = datetime.now().date() + timedelta(days=3)

        context["deadline_warning_date"] = deadline_warning_date
        return context


def calculate_completed_percentage():
    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(is_completed=True).count()

    if total_tasks > 0:
        percentage = (completed_tasks / total_tasks) * 100
    else:
        percentage = 0

    return int(percentage)


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "task_manager/task_list.html"
    context_object_name = "task_list"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        completed_percentage = calculate_completed_percentage()
        context["completed_percentage"] = completed_percentage

        name = self.request.GET.get("name", "")
        context["search_form"] = TaskSearchForm(initial={"name": name})

        return context

    def get_queryset(self):
        queryset = Task.objects.all().order_by("-id")
        form = TaskSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    template_name = "task_manager/task_confirm_delete.html"
    success_url = reverse_lazy("task_manager:task-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        context["related_workers"] = task.assignees.all()
        return context


class CompletedTaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "task_manager/completed_task_list.html"
    context_object_name = "completed_tasks"
    paginate_by = 10

    def get_queryset(self):
        return Task.objects.filter(is_completed=True)


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = WorkerSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        queryset = Worker.objects.all().order_by("username")
        form = WorkerSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return queryset


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        worker = self.get_object()

        context["assigned_tasks"] = worker.task_set.filter(is_completed=False)
        context["completed_tasks"] = worker.task_set.filter(is_completed=True)

        context["team"] = worker.team
        if worker.team:
            context["team_members"] = worker.team.members.all()
            context["projects"] = worker.team.projects.all()
        else:
            context["team_members"] = []
            context["projects"] = Project.objects.none()

        return context


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("task_manager:worker-list")


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    template_name = "task_manager/worker_form.html"
    fields = [
        "username",
        "first_name",
        "last_name",
        "email",
        "position",
        "team",
    ]
    success_url = reverse_lazy("task_manager:worker-list")


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    template_name = "task_manager/worker_confirm_delete.html"
    success_url = reverse_lazy("worker-list")


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    template_name = "task_manager/position_list.html"
    context_object_name = "positions"


class PositionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Position
    template_name = "task_manager/position_detail.html"
    context_object_name = "position"


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task_manager:position-list")


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    template_name = "task_manager/position_form.html"
    fields = ["name"]


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    template_name = "task_manager/position_confirm_delete.html"
    success_url = reverse_lazy("task_manager:position-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        position = self.get_object()
        context["related_position"] = Worker.objects.filter(position=position)
        return context


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    template_name = "task_manager/task_type_list.html"
    context_object_name = "task_type"


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-type-list")
    template_name = "task_manager/task_type_form.html"


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    template_name = "task_manager/task_type_confirm_delete.html"
    success_url = reverse_lazy("task_manager:task-type-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_type = self.get_object()
        context["related_tasks"] = Task.objects.filter(task_type=task_type)
        return context


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = Project
    fields = "__all__"
    success_url = reverse_lazy("task_manager:task-list")
    template_name = "task_manager/project_form.html"


class TeamCreateView(LoginRequiredMixin, generic.CreateView):
    model = Team
    form_class = TeamForm
    success_url = reverse_lazy("task_manager:index")
    template_name = "task_manager/team_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        members = form.cleaned_data["members"]
        for member in members:
            member.team = self.object
            member.save()
        return response
