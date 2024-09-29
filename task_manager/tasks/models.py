from django.db import models
from django.contrib.auth import get_user_model
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Task(models.Model):
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=150,
        unique=True
    )
    description = models.TextField(
        verbose_name=_('Description'),
        blank=True
    )
    date_created = models.DateTimeField(
        verbose_name=_('Date Created'),
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='tasks_authored',
        verbose_name=_('Author')
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='statuses',
        verbose_name=_('Status')
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='tasks_executed',
        verbose_name=_('Executor')
    )
    labels = models.ManyToManyField(
        Label,
        through="TaskLabelRelation",
        through_fields=("task", "label"),
        blank=True,
        related_name="labels",
        verbose_name=_("Labels"),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')


class TaskLabelRelation(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)
