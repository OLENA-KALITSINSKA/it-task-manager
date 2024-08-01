from django.test import TestCase
from django.contrib.auth import get_user_model
from task_manager.models import Tag, Team, TaskType, Project, Position
from task_manager.forms import (
    LoginForm,
    TeamForm,
    TaskForm,
    WorkerCreationForm,
    TaskSearchForm,
    WorkerSearchForm
)

User = get_user_model()


class FormTest(TestCase):

    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.team = Team.objects.create(name="Development Team")
        self.user = User.objects.create_user(username="testuser", password="securepassword")
        self.tag = Tag.objects.create(name="Urgent")
        self.task_type = TaskType.objects.create(name="Development")
        self.project = Project.objects.create(name="Project X")

    def test_login_form_valid(self):
        form_data = {
            "username": "testuser",
            "password": "securepassword"
        }
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_login_form_invalid(self):
        form_data = {
            "username": "",
            "password": ""
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('password', form.errors)

    def test_team_form_valid(self):
        form_data = {
            "name": "Team A",
            "members": [self.user.pk]
        }
        form = TeamForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_task_form_valid(self):
        form_data = {
            "name": "Test Task",
            "description": "Task description",
            "deadline": "2024-12-31",
            "priority": "Urgent",
            "task_type": self.task_type.pk,
            "assignees": [self.user.pk],
            "tags": [self.tag.pk],
            "project": self.project.pk
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_worker_creation_form_valid(self):
        form_data = {
            "username": "new_worker",
            "email": "newworker@example.com",
            "password1": "validpassword123",
            "password2": "validpassword123",
            "position": self.position.pk,
            "first_name": "First",
            "last_name": "Last",
            "team": self.team.pk
        }
        form = WorkerCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_worker_creation_form_invalid_password_mismatch(self):
        form_data = {
            "username": "workeruser",
            "email": "workeruser@example.com",
            "password1": "securepassword",
            "password2": "differentpassword",
            "position": self.position.pk,
            "first_name": "John",
            "last_name": "Doe",
            "team": self.team.pk
        }
        form = WorkerCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_task_search_form_valid(self):
        form = TaskSearchForm(data={"name": "Test Task"})
        self.assertTrue(form.is_valid())

    def test_task_search_form_empty(self):
        form = TaskSearchForm(data={"name": ""})
        self.assertTrue(form.is_valid())

    def test_worker_search_form_valid(self):
        form = WorkerSearchForm(data={"username": "testuser"})
        self.assertTrue(form.is_valid())

    def test_worker_search_form_empty(self):
        form = WorkerSearchForm(data={"username": ""})
        self.assertTrue(form.is_valid())
