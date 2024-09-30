from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

User = get_user_model()


class UserCRUDTests(TestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            username='testuser',
            first_name='Test',
            last_name='User',
            password='TestPass123'
        )
        self.client = Client()

    def test_user_registration(self):
        # Тест регистрации нового пользователя.
        user_data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'NewPass123',
            'password2': 'NewPass123',
        }
        response = self.client.post(reverse('users_create'), user_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_update(self):
        # Тест обновления данных существующего пользователя.
        self.client.force_login(self.user)
        updated_data = {
            'username': 'updateduser',
            'first_name': 'Updated',
            'last_name': 'User',
            'password1': 'UpdatedPass123',
            'password2': 'UpdatedPass123',
        }
        response = self.client.post(
            reverse('users_update', args=[self.user.id]), updated_data)
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertTrue(check_password('UpdatedPass123', self.user.password))

    def test_user_delete(self):
        # Тест удаления пользователя.
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('users_delete', args=[self.user.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(username='testuser').exists())
