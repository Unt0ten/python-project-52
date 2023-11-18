from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class StatusModel(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        error_messages={
            "unique": _("Task status with such Name already exist."),
        }
    )
    date_creation = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
