from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from task_manager.statuses.models import StatusModel


class TaskModel(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        error_messages={
            "unique": _("Task with such Name already exist."),
        }
    )
    description = models.TextField(max_length=1000)
    status = models.ForeignKey(
        StatusModel,
        on_delete=models.PROTECT,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='author',
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='executor'
    )
    created_at = models.DateTimeField(default=timezone.now)
