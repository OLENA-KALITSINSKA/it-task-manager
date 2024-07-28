from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from task_manager.models import Task, Worker, Position, TaskType, Project

INDEX_URL = reverse("task_manager:index")
TASK_LIST_URL = reverse("task_manager:task-list")
WORKER_LIST_URL = reverse("task_manager:worker-list")
POSITION_LIST_URL = reverse("task_manager:position-list")
TASK_TYPE_LIST_URL = reverse("task_manager:task-type-list")
USER_TASKS_URL = reverse("task_manager:user-tasks")


class PublicListViewTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_index_login_required(self):
        response = self.client.get(INDEX_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_task_list_login_required(self):
        response = self.client.get(TASK_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_worker_list_login_required(self):
        response = self.client.get(WORKER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_position_list_login_required(self):
        response = self.client.get(POSITION_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_task_type_list_login_required(self):
        response = self.client.get(TASK_TYPE_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_user_tasks_login_required(self):
        response = self.client.get(USER_TASKS_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateListViewTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.client.force_login(self.user)

    def test_index_view(self):
        response = self.client.get(INDEX_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "task_manager/index.html")

    def test_retrieve_tasks(self):
        task_type = TaskType.objects.create(name="Type A")
        project = Project.objects.create(name="Project A", description="Project Description")
        task = Task.objects.create(
            name="Test Task",
            description="Test Description",
            deadline="2024-12-31",
            is_completed=False,
            priority="High",
            task_type=task_type,
            project=project
        )
        response = self.client.get(TASK_LIST_URL)
        tasks = Task.objects.all().order_by('name')  # Ensure ordering
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["task_list"], tasks, ordered=True)
        self.assertTemplateUsed(response, "task_manager/task_list.html")

    def test_retrieve_workers(self):
        Worker.objects.create(username="worker1", password="password")
        Worker.objects.create(username="worker2", password="password")
        response = self.client.get(WORKER_LIST_URL)
        workers = Worker.objects.all().order_by('username')  # Ensure ordering
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["worker_list"], workers, ordered=False)
        self.assertTemplateUsed(response, "task_manager/worker_list.html")

    def test_retrieve_positions(self):
        Position.objects.create(name="Position A")
        Position.objects.create(name="Position B")
        response = self.client.get(POSITION_LIST_URL)
        positions = Position.objects.all() # Ensure ordering
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["positions"], positions, ordered=False)
        self.assertTemplateUsed(response, "task_manager/position_list.html")

    def test_retrieve_task_types(self):
        TaskType.objects.create(name="Type 1")
        TaskType.objects.create(name="Type 2")
        response = self.client.get(TASK_TYPE_LIST_URL)
        task_types = TaskType.objects.all().order_by('id')  # Ensure ordering
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["task_type"], task_types, ordered=False)
        self.assertTemplateUsed(response, "task_manager/task_type_list.html")

    def test_user_tasks(self):
        task_type = TaskType.objects.create(name="Type C")
        project = Project.objects.create(name="Project B", description="Another Project Description")
        task = Task.objects.create(
            name="User Task",
            description="Assigned to user",
            deadline=timezone.now() + timezone.timedelta(days=1),
            is_completed=False,
            priority="Medium",
            task_type=task_type,
            project=project
        )
        task.assignees.add(self.user)
        response = self.client.get(USER_TASKS_URL)
        user_tasks = Task.objects.filter(assignees=self.user).order_by('name')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["user_task_list"], user_tasks, ordered=False)
        self.assertTemplateUsed(response, "task_manager/user_tasks.html")
