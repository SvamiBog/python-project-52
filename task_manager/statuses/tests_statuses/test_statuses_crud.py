from task_manager.statuses.models import Status
from task_manager.tests.base_test_case import BaseCRUDTestCase


class StatusCRUDTests(BaseCRUDTestCase):

    def setUp(self):
        """Set up test data for status CRUD operations."""
        super().setUp()
        self.status = Status.objects.create(name='Initial Status')

    def test_create_status(self):
        """Test creating a new status."""
        self.assert_create('status_create', Status, {'name': 'New Status'})

    def test_read_status(self):
        """Test reading status list."""
        self.assert_read('status_index', None, 'name')

    def test_update_status(self):
        """Test updating a status."""
        self.assert_update('status_update', self.status, {'name': 'Updated Status'})

    def test_delete_status(self):
        """Test deleting a status."""
        self.assert_delete('status_delete', Status, self.status.id)
