from django.urls import reverse
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from task_manager.tests.base_test_case import BaseCRUDTestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskFilterTests(BaseCRUDTestCase):

    def setUp(self):
        """Set up test data for tasks, users, statuses, and labels."""
        super().setUp()
        self.executor = User.objects.create_user(username="executor", password="password123")
        self.another_user = User.objects.create_user(username="another_user", password="password123")

        # Create statuses
        self.status_open = Status.objects.create(name="Open")
        self.status_in_progress = Status.objects.create(name="In Progress")

        # Create a label
        self.label_bug = Label.objects.create(name="Bug")

        # Create tasks
        self.task_data_1 = {
            'name': "Task 1",
            'description': "Description 1",
            'status': self.status_open,
            'executor': self.executor,
            'author': self.user
        }

        self.task1 = Task.objects.create(**self.task_data_1)
        self.task1.labels.add(self.label_bug)

        self.task_data_2 = {
            'name': "Task 2",
            'description': "Description 2",
            'status': self.status_in_progress,
            'executor': self.another_user,
            'author': self.another_user
        }

        self.task2 = Task.objects.create(**self.task_data_2)

    def assert_task_filter(self, field, value, task_included, task_excluded):
        """Helper method to test task filtering by different criteria."""
        response = self.client.get(reverse('tasks_index'), {field: value})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, task_included.name)
        self.assertNotContains(response, task_excluded.name)

    def test_filter_by_status(self):
        """Test filtering tasks by status."""
        self.assert_task_filter('status', self.status_open.id, self.task1, self.task2)

    def test_filter_by_executor(self):
        """Test filtering tasks by executor."""
        self.assert_task_filter('executor', self.executor.id, self.task1, self.task2)

    def test_filter_by_label(self):
        """Test filtering tasks by label."""
        self.assert_task_filter('labels', self.label_bug.id, self.task1, self.task2)

    def test_filter_by_author(self):
        """Test filtering tasks by author (own tasks)."""
        response = self.client.get(reverse('tasks_index'), {'own_tasks': 'on'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task1.name)
        self.assertNotContains(response, self.task2.name)
