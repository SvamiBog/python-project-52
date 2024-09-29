from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label

User = get_user_model()

class TaskFilterTests(TestCase):

    def setUp(self):
        # Создание тестовых пользователей
        self.author = User.objects.create_user(username="author", password="password123")
        self.executor = User.objects.create_user(username="executor", password="password123")
        self.another_user = User.objects.create_user(username="another_user", password="password123")

        # Создание статусов
        self.status_open = Status.objects.create(name="Open")
        self.status_in_progress = Status.objects.create(name="In Progress")

        # Создание метки
        self.label_bug = Label.objects.create(name="Bug")

        # Создание задач
        self.task1 = Task.objects.create(
            name="Task 1",
            description="Description 1",
            status=self.status_open,
            executor=self.executor,
            author=self.author
        )
        self.task1.labels.add(self.label_bug)

        self.task2 = Task.objects.create(
            name="Task 2",
            description="Description 2",
            status=self.status_in_progress,
            executor=self.another_user,
            author=self.another_user
        )

        self.client.login(username="author", password="password123")

    def test_filter_by_status(self):
        """Тест фильтрации по статусу."""
        response = self.client.get(reverse('tasks_index'), {'status': self.status_open.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task1.name)
        self.assertNotContains(response, self.task2.name)

    def test_filter_by_executor(self):
        """Тест фильтрации по исполнителю."""
        response = self.client.get(reverse('tasks_index'), {'executor': self.executor.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task1.name)
        self.assertNotContains(response, self.task2.name)

    def test_filter_by_label(self):
        """Тест фильтрации по метке."""
        response = self.client.get(reverse('tasks_index'), {'labels': self.label_bug.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task1.name)
        self.assertNotContains(response, self.task2.name)

    def test_filter_by_author(self):
        """Тест фильтрации задач, созданных автором."""
        response = self.client.get(reverse('tasks_index'), {'own_tasks': 'on'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task1.name)
        self.assertNotContains(response, self.task2.name)
