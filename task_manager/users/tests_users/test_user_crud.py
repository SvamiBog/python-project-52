import uuid
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from task_manager.tests.base_test_case import BaseCRUDTestCase

User = get_user_model()

class UserCRUDTests(BaseCRUDTestCase):

    def setUp(self):
        """Set up test data for user CRUD operations."""
        super().setUp()
        unique_username = f'testuser_{uuid.uuid4()}'
        self.user_data = {
            'username': unique_username,
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'TestPass123'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_user_registration(self):
        """Test registering a new user."""
        new_user_data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'NewPass123',
            'password2': 'NewPass123',
        }
        response = self.client.post(reverse('users_create'), new_user_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_update(self):
        """Test updating user information."""
        self.client.force_login(self.user)
        updated_data = {
            'username': 'updateduser',
            'first_name': 'Updated',
            'last_name': 'User',
            'password1': 'UpdatedPass123',
            'password2': 'UpdatedPass123',
        }
        response = self.client.post(reverse('users_update', args=[self.user.id]), updated_data)
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertTrue(check_password('UpdatedPass123', self.user.password))

    def test_user_delete(self):
        """Test deleting a user."""
        self.client.force_login(self.user)
        self.assert_delete('users_delete', User, self.user.id)
