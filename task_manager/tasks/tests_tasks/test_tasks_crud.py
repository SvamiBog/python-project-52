from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task

User = get_user_model()


class TasksCRUDTests(TestCase):

    def setUp(self):
        """Создаем пользователей, статус и задачу для тестов."""
        self.user = User.objects.create_user(username='testuser', password='password')
        self.other_user = User.objects.create_user(username='otheruser', password='password')
        self.status = Status.objects.create(name='New')
        self.client.login(username='testuser', password='password')

        # Создаем задачу
        self.task = Task.objects.create(
            name='Test Task',
            description='Test Description',
            author=self.user,
            status=self.status,
            executor=self.other_user
        )

    def test_task_create(self):
        """Тестируем создание новой задачи."""
        response = self.client.post(reverse('task_create'), {
            'name': 'New Task',
            'description': 'New Task Description',
            'status': self.status.id,
            'executor': self.other_user.id
        })
        self.assertEqual(response.status_code, 302)  # Успешное создание задачи
        self.assertEqual(Task.objects.count(), 2)  # Всего должно быть 2 задачи
        self.assertTrue(Task.objects.filter(name='New Task').exists())

    def test_task_read(self):
        """Тестируем отображение задачи."""
        response = self.client.get(reverse('task_detail', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')  # Проверяем, что задача отображается
        self.assertContains(response, 'Test Description')

    def test_task_update(self):
        """Тестируем обновление задачи."""
        response = self.client.post(reverse('task_update', args=[self.task.id]), {
            'name': 'Updated Task',
            'description': 'Updated Description',
            'status': self.status.id,
            'executor': self.other_user.id
        })
        self.assertEqual(response.status_code, 302)  # Успешное обновление
        self.task.refresh_from_db()  # Обновляем объект задачи
        self.assertEqual(self.task.name, 'Updated Task')
        self.assertEqual(self.task.description, 'Updated Description')

    def test_task_delete(self):
        """Тестируем удаление задачи."""
        response = self.client.post(reverse('task_delete', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)  # Успешное удаление
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())  # Задачи больше нет
