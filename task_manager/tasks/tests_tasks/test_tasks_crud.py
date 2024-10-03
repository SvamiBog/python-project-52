from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.tests.base_test_case import BaseCRUDTestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class TasksCRUDTests(BaseCRUDTestCase):
    def setUp(self):
        super().setUp()
        self.status = Status.objects.create(name='New')
        self.new_status = Status.objects.create(name='Updated Status')  # Создаем новый статус для теста обновления
        self.other_user = User.objects.create_user(username='otheruser', password='password')
        self.task_data = {
            'name': 'Test Task',
            'description': 'Test Description',
            'status': self.status,
            'executor': self.other_user,
            'author': self.user
        }
        self.task = Task.objects.create(**self.task_data)

    def test_task_create(self):
        """Test creating a task."""
        self.assert_create('task_create', Task, {
            'name': 'New Task',
            'description': 'New Task Description',
            'status': self.status.id,
            'executor': self.other_user.id,
            'author': self.user.id
        })

    def test_task_read(self):
        """Test reading task details."""
        self.assert_read('task_detail', self.task.pk, 'name')

    def test_task_update(self):
        """Test updating a task."""
        updated_data = {
            'name': 'Updated Task',
            'description': 'Updated Description',
            'status': self.new_status.id,
            'executor': self.other_user.id
        }
        self.assert_update('task_update', self.task, updated_data)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status.id, self.new_status.id)

    def test_task_delete(self):
        """Test deleting a task."""
        self.assert_delete('task_delete', Task, self.task.id)
