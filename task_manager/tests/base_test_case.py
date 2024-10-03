from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class BaseCRUDTestCase(TestCase):
    def setUp(self):
        """Set up common user data and login for all CRUD tests."""
        self.user = User.objects.create_user(
            username="testuser",
            password="password123"
        )
        self.client.login(username="testuser", password="password123")

    def assert_create(self, url_name, model_class, data):
        """Helper method to test object creation."""
        response = self.client.post(reverse(url_name), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(model_class.objects.filter(**data).exists())

    def assert_read(self, url_name, obj_pk, field_name):
        """Helper method to test read actions."""
        if obj_pk:
            response = self.client.get(reverse(url_name, args=[obj_pk]))
        else:
            response = self.client.get(reverse(url_name))

        self.assertEqual(response.status_code, 200)

    def assert_update(self, url_name, model_instance, updated_data):
        response = self.client.post(reverse(url_name, args=[model_instance.pk]), updated_data)
        self.assertEqual(response.status_code, 302)
        model_instance.refresh_from_db()

        for field, value in updated_data.items():
            if field == 'status':
                self.assertEqual(getattr(model_instance, field).id, value)
            elif field == 'executor':
                self.assertEqual(getattr(model_instance, field).id, value)
            else:
                self.assertEqual(getattr(model_instance, field), value)

    def assert_delete(self, url_name, model_class, obj_id):
        """Helper method to test object deletion."""
        response = self.client.post(reverse(url_name, args=[obj_id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(model_class.objects.filter(id=obj_id).exists())
