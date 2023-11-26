from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from task_manager.statuses.models import StatusModel
from task_manager.labels.models import LabelModel
from task_manager.users.models import Person


class TaskModel(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        error_messages={
            "unique": _("Task with such Name already exist."),
        },
        verbose_name=_('Name'),
        help_text=_('Obligatory field.')
    )
    description = models.TextField(
        max_length=1000,
        verbose_name=_('Description'),
        null=True,
        blank=True,
        help_text=_('Describe the task.')
    )
    status = models.ForeignKey(
        StatusModel,
        on_delete=models.PROTECT,
        verbose_name=_('Status'),
        help_text=_('Obligatory field. Select one of the task statuses.')
    )
    executor = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        verbose_name=_('Executor'),
        related_name='executor',
        null=True,
        blank=True,
        help_text=_('Select the task executor.'),
    )
    author = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        verbose_name=_('Author'),
        related_name='author'
    )
    labels = models.ManyToManyField(
        LabelModel,
        blank=True,
        verbose_name=_('Labels'),
        help_text=_('Select one or more tags.')
    )
    created_at = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('tasks')

    def __str__(self):
        return self.name
