from django.db import models
from django.utils import timezone


class StatusModel(models.Model):
    name = models.CharField(max_length=150)
    date_creation = models.DateTimeField(default=timezone.now)
