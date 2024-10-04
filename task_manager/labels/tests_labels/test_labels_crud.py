from task_manager.labels.models import Label
from task_manager.tests.base_test_case import BaseCRUDTestCase


class LabelsCRUDTests(BaseCRUDTestCase):
    def setUp(self):
        super().setUp()
        self.label = Label.objects.create(name="Test Label")

    def test_label_create(self):
        """Test creating a label."""
        self.assert_create('label_create', Label, {'name': 'New Label'})

    def test_label_read(self):
        """Test reading label list."""
        self.assert_read('labels_index', None, 'name')

    def test_label_update(self):
        """Test updating a label."""
        self.assert_update(
            'label_update',
            self.label,
            {'name': 'Updated Label'}
        )

    def test_label_delete(self):
        """Test deleting a label."""
        self.assert_delete('label_delete', Label, self.label.id)
