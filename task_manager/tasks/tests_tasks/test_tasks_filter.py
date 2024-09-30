from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label

User = get_user_model()

class TaskFilterTests(TestCase):

    def setUp(self):
        """Set up test data for tasks, users, statuses, and labels."""
        # Create test users
        self.author = User.objects.create_user(username="author", password="password123")
        self.executor = User.objects.create_user(username="executor", password="password123")
        self.another_user = User.objects.create_user(username="another_user", password="password123")

        # Create statuses
        self.status_open = Status.objects.create(name="Open")
        self.status_in_progress = Status.objects.create(name="In Progress")

        # Create a label
        self.label_bug = Label.objects.create(name="Bug")

        # Create tasks
        self.task1 = self.create_task("Task 1", "Description 1", self.status_open, self.executor, self.author, self.label_bug)
        self.task2 = self.create_task("Task 2", "Description 2", self.status_in_progress, self.another_user, self.another_user)

        # Log in as the author
        self.client.login(username="author", password="password123")

    def create_task(self, name, description, status, executor, author, label=None):
        """Helper method to create a task and optionally add a label."""
        task = Task.objects.create(
            name=name,
            description=description,
            status=status,
            executor=executor,
            author=author
        )
        if label:
            task.labels.add(label)
        return task

    def assert_task_filter(self, filter_field, filter_value, task_included, task_excluded):
        """Helper method to test task filtering by different criteria."""
        response = self.client.get(reverse('tasks_index'), {filter_field: filter_value})
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
