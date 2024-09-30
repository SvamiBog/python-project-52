from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from task_manager.labels.models import Label

User = get_user_model()


class LabelsCRUDTests(TestCase):
    def setUp(self):
        # Создание тестового пользователя и метки
        self.user = User.objects.create_user(
            username="testuser",
            password="password123"
        )
        self.label = Label.objects.create(name="Test Label")

        # Аутентификация пользователя
        self.client.login(username="testuser", password="password123")

    def test_label_create(self):
        """Тест создания метки."""
        response = self.client.post(reverse('label_create'), {
            'name': 'New Label'
        })
        self.assertEqual(response.status_code, 302)  # редирект после создания
        self.assertTrue(Label.objects.filter(name='New Label').exists())

    def test_label_read(self):
        """Тест отображения списка меток."""
        response = self.client.get(reverse('labels_index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.label.name)

    def test_label_update(self):
        """Тест обновления метки."""
        response = self.client.post(reverse(
            'label_update',
            args=[self.label.id]
        ),
            {'name': 'Updated Label'}
        )
        self.assertEqual(response.status_code, 302)
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Updated Label')

    def test_label_delete(self):
        """Тест удаления метки."""
        response = self.client.post(
            reverse(
                'label_delete',
                args=[self.label.id]
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Label.objects.filter(id=self.label.id).exists())
