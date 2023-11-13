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
    status = models.CharField(max_length=255)
    author = models.CharField(max_length=255, null=True,  editable=False)
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
    )
    created_at = models.DateTimeField(default=timezone.now)

    def set_author(self, author):
        self.author = author
        self._author = author
