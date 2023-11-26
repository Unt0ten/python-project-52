import django_filters
from django.utils.translation import gettext_lazy as _
from django import forms

from .models import TaskModel
from task_manager.statuses.models import StatusModel
from task_manager.labels.models import LabelModel
from task_manager.users.models import Person


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        label=_('Status'),
        queryset=StatusModel.objects.all(),
    )
    executor = django_filters.ModelChoiceFilter(
        label=_('Executor'),
        queryset=Person.objects.all()
    )
    labels = django_filters.ModelChoiceFilter(
        label=_('Label'),
        queryset=LabelModel.objects.all()
    )
    author = django_filters.BooleanFilter(
        label=_('Only my tasks'),
        method='filter_author',
        widget=forms.CheckboxInput(),
    )

    class Meta:
        model = TaskModel
        fields = ['status', 'executor']

    def filter_author(self, queryset, name, value):
        if value:
            return queryset.filter(**{'author__id': self.request.user.id})
        return queryset
