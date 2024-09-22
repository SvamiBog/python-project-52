from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from task_manager.statuses.models import Status

User = get_user_model()


class StatusCRUDTestCase(TestCase):

    def setUp(self):
        # Создаем пользователя для тестирования,
        # чтобы защитить доступ к действиям.
        self.user = User.objects.create_user(
            username='testuser',
            password='password'
        )
        self.client.login(
            username='testuser',
            password='password'
        )

        # Создаем тестовый статус для проверки функций обновления и удаления.
        self.status = Status.objects.create(name='Initial Status')

    def test_create_status(self):
        # Тестируем создание нового статуса
        url = reverse('status_create')
        data = {'name': 'New Status'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='New Status').exists())

    def test_read_status(self):
        # Тестируем чтение списка статусов
        url = reverse('status_index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Initial Status')

    def test_update_status(self):
        # Тестируем обновление существующего статуса
        url = reverse('status_update', args=[self.status.id])
        data = {'name': 'Updated Status'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Updated Status')

    def test_delete_status(self):
        # Тестируем удаление статуса
        url = reverse('status_delete', args=[self.status.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(id=self.status.id).exists())
