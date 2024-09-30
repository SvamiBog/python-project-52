from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task

User = get_user_model()


class TasksCRUDTests(TestCase):

    def setUp(self):
        """Set up common data for all tests."""
        self.user = self.create_user('testuser', 'password')
        self.other_user = self.create_user('otheruser', 'password')
        self.status = self.create_status('New')
        self.client.login(username='testuser', password='password')

        # Create a task for testing
        self.task = self.create_task(
            name='Test Task',
            description='Test Description',
            author=self.user,
            status=self.status,
            executor=self.other_user
        )

    def create_user(self, username, password):
        """Create and return a user."""
        return User.objects.create_user(username=username, password=password)

    def create_status(self, name):
        """Create and return a status."""
        return Status.objects.create(name=name)

    def create_task(self, name, description, author, status, executor):
        """Create and return a task."""
        return Task.objects.create(
            name=name,
            description=description,
            author=author,
            status=status,
            executor=executor
        )

    def test_task_create(self):
        """Test creating a new task."""
        response = self.client.post(reverse('task_create'), {
            'name': 'New Task',
            'description': 'New Task Description',
            'status': self.status.id,
            'executor': self.other_user.id
        })
        # Check for successful redirect after creation
        self.assertEqual(response.status_code, 302)
        # There should be 2 tasks in total
        self.assertEqual(Task.objects.count(), 2)
        # Verify the new task was created
        self.assertTrue(Task.objects.filter(name='New Task').exists())

    def test_task_read(self):
        """Test displaying a task's details."""
        response = self.client.get(reverse('task_detail', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        # Check that the task's name is displayed
        self.assertContains(response, 'Test Task')
        # Check that the task's description is displayed
        self.assertContains(response, 'Test Description')

    def test_task_update(self):
        """Test updating an existing task."""
        response = self.client.post(reverse(
            'task_update',
            args=[self.task.id]
        ), {
            'name': 'Updated Task',
            'description': 'Updated Description',
            'status': self.status.id,
            'executor': self.other_user.id
        })
        # Check for successful redirect after update
        self.assertEqual(response.status_code, 302)
        # Refresh task data from the database
        self.task.refresh_from_db()
        # Verify the task name was updated
        self.assertEqual(self.task.name, 'Updated Task')
        # Verify the task description was updated
        self.assertEqual(self.task.description, 'Updated Description')

    def test_task_delete(self):
        """Test deleting a task."""
        response = self.client.post(reverse(
            'task_delete',
            args=[self.task.id]
        ))
        # Check for successful redirect after deletion
        self.assertEqual(response.status_code, 302)
        # Verify the task no longer exists
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())
