from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class LabelModel(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        error_messages={
            "unique": _("Task status with such Name already exist.")
        },
        verbose_name=_('Name')
    )
    created_at = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('labels')

    def __str__(self):
        return self.name
