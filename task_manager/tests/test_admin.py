from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from task_manager.models import Position, Team


class AdminSiteTests(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="test123"
        )
        self.client.force_login(self.admin_user)
        self.position = Position.objects.create(name="Developer")
        self.team = Team.objects.create(name="Development Team")
        self.worker = get_user_model().objects.create_user(
            username="worker",
            password="test1234",
            email="worker@example.com",
            position=self.position,
            team=self.team
        )

    def test_worker_position_listed(self):
        """
        Test that worker's position is in list_display
        on worker admin page
        """
        url = reverse("admin:task_manager_worker_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.worker.position.name)

    def test_worker_team_listed(self):
        """
        Test that worker's team is in list_display
        on worker admin page
        """
        url = reverse("admin:task_manager_worker_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.worker.team.name)

    def test_worker_email_listed(self):
        """
        Test that worker's email is in list_display
        on worker admin page
        """
        url = reverse("admin:task_manager_worker_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.worker.email)

    def test_worker_detail_position_listed(self):
        """
        Test that worker's position is on worker detail admin page
        """
        url = reverse("admin:task_manager_worker_change", args=[self.worker.id])
        res = self.client.get(url)
        self.assertContains(res, self.worker.position.name)

    def test_worker_detail_team_listed(self):
        """
        Test that worker's team is on worker detail admin page
        """
        url = reverse("admin:task_manager_worker_change", args=[self.worker.id])
        res = self.client.get(url)
        self.assertContains(res, self.worker.team.name)

    def test_worker_detail_email_listed(self):
        """
        Test that worker's email is on worker detail admin page
        """
        url = reverse("admin:task_manager_worker_change", args=[self.worker.id])
        res = self.client.get(url)
        self.assertContains(res, self.worker.email)

    def test_worker_add_position_listed(self):
        """
        Test that worker's position is on worker add admin page
        """
        url = reverse("admin:task_manager_worker_add")
        res = self.client.get(url)
        self.assertContains(res, "position")

    def test_worker_add_team_listed(self):
        """
        Test that worker's team is on worker add admin page
        """
        url = reverse("admin:task_manager_worker_add")
        res = self.client.get(url)
        self.assertContains(res, "team")
