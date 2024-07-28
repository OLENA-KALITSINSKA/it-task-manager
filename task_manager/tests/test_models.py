from django.test import TestCase
from datetime import date

from task_manager.models import Position, TaskType, Tag, Team, Project, Worker, Task


class ModelTests(TestCase):

    def test_position_str(self):
        position = Position.objects.create(name="Developer")
        self.assertEqual(str(position), "Developer")

    def test_task_type_str(self):
        task_type = TaskType.objects.create(name="Bug")
        self.assertEqual(str(task_type), "Bug")

    def test_tag_str(self):
        tag = Tag.objects.create(name="Urgent")
        self.assertEqual(str(tag), "Urgent")

    def test_team_str(self):
        team = Team.objects.create(name="Backend")
        self.assertEqual(str(team), "Backend")

    def test_project_str(self):
        team = Team.objects.create(name="Frontend")
        project = Project.objects.create(name="Website Redesign", description="Redesign the company website")
        project.teams.add(team)
        self.assertEqual(str(project), "Website Redesign")

    def test_worker_str(self):
        position = Position.objects.create(name="Manager")
        team = Team.objects.create(name="Operations")
        worker = Worker.objects.create(
            username="john_doe",
            password="password123",
            first_name="John",
            last_name="Doe",
            position=position,
            team=team
        )
        self.assertEqual(str(worker), "john_doe")

    def test_task_str(self):
        position = Position.objects.create(name="Developer")
        team = Team.objects.create(name="Backend")
        worker = Worker.objects.create(
            username="jane_doe",
            password="password123",
            first_name="Jane",
            last_name="Doe",
            position=position,
            team=team
        )
        task_type = TaskType.objects.create(name="Feature")
        tag = Tag.objects.create(name="Important")
        project = Project.objects.create(name="Website Redesign", description="Redesign the company website")
        task = Task.objects.create(
            name="Implement new feature",
            description="Add a new feature to the website",
            deadline=date(2024, 7, 21),
            is_completed=False,
            priority="High",
            task_type=task_type,
            project=project
        )
        task.assignees.add(worker)
        task.tags.add(tag)
        self.assertEqual(str(task), "Implement new feature (High, due 2024-07-21) - In Progress")

    def test_task_formatted_deadline(self):
        task = Task.objects.create(
            name="Submit report",
            description="Submit the annual report",
            deadline=date(2024, 7, 21),
            is_completed=False,
            priority="Medium"
        )
        self.assertEqual(task.formatted_deadline(), '21-07-2024')
