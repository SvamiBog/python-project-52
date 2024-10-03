from django.urls import reverse
from django.contrib.auth import get_user_model
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from task_manager.tests.base_test_case import BaseCRUDTestCase

User = get_user_model()

class TaskFilterTests(BaseCRUDTestCase):

    def setUp(self):
        """Set up test data for tasks, users, statuses, and labels."""
        super().setUp()  # Используем setup родительского класса для создания пользователя
        self.executor = User.objects.create_user(username="executor", password="password123")
        self.another_user = User.objects.create_user(username="another_user", password="password123")

        # Создаем статусы
        self.status_open = Status.objects.create(name="Open")
        self.status_in_progress = Status.objects.create(name="In Progress")

        # Создаем метку
        self.label_bug = Label.objects.create(name="Bug")

        # Создаем задачи
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

    def test_filter_by_status(self):
        """Test filtering tasks by status."""
        filter_data_status = {
            'field': 'status',
            'value': self.status_open.id,
            'task_included': self.task1,
            'task_excluded': self.task2
        }
        self.assert_task_filter(filter_data_status)

    def test_filter_by_executor(self):
        """Test filtering tasks by executor."""
        filter_data_executor = {
            'field': 'executor',
            'value': self.executor.id,
            'task_included': self.task1,
            'task_excluded': self.task2
        }
        self.assert_task_filter(filter_data_executor)

    def test_filter_by_label(self):
        """Test filtering tasks by label."""
        filter_data_label = {
            'field': 'labels',
            'value': self.label_bug.id,
            'task_included': self.task1,
            'task_excluded': self.task2
        }
        self.assert_task_filter(filter_data_label)

    def test_filter_by_author(self):
        """Test filtering tasks by author (own tasks)."""
        response = self.client.get(reverse('tasks_index'), {'own_tasks': 'on'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task1.name)
        self.assertNotContains(response, self.task2.name)

    def assert_task_filter(self, filter_data):
        """Helper method to test task filtering by different criteria."""
        response = self.client.get(
            reverse('tasks_index'), {filter_data['field']: filter_data['value']}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, filter_data['task_included'].name)
        self.assertNotContains(response, filter_data['task_excluded'].name)
