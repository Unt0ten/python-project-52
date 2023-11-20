from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.utils.translation import gettext as _

from .models import LabelModel
from .forms import LabelModelForm
from task_manager.mixins_login import CustomLoginRequiredMixin
from task_manager.tasks.models import TaskModel


class LabelsView(CustomLoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        labels = LabelModel.objects.all()
        return render(request, 'labels/labels.html', {'labels': labels})


class CreateLabel(CustomLoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return render(request, 'labels/create.html')

    def post(self, request, *args, **kwargs):
        form = LabelModelForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request, _('Label successfully created')
            )
            return redirect('labels')

        return render(request, 'statuses/create.html', {'form': form})


class UpdateLabel(CustomLoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        label_pk = kwargs.get('pk')
        label = get_object_or_404(LabelModel, id=label_pk)
        form = LabelModelForm(instance=label)
        return render(
            request,
            'labels/update.html',
            {'form': form, 'label_pk': label_pk, 'label': label}
        )

    def post(self, request, *args, **kwargs):
        label_pk = kwargs.get('pk')
        label = get_object_or_404(LabelModel, id=label_pk)
        form = LabelModelForm(request.POST, instance=label)
        if form.is_valid():
            form.save()
            messages.success(request, _('Label successfully changed'))
            return redirect('labels')

        return render(
            request,
            'labels/update.html',
            {'form': form, 'label_pk': label_pk}
        )


class DeleteLabel(CustomLoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        label_pk = kwargs.get('pk')
        label = get_object_or_404(LabelModel, id=label_pk)
        return render(
            request,
            'labels/delete.html',
            {'label_pk': label_pk, 'label': label}
        )

    def post(self, request, *args, **kwargs):
        label_pk = kwargs.get('pk')
        label = get_object_or_404(LabelModel, id=label_pk)
        tasks = TaskModel.objects.filter(labels=label_pk)
        if tasks:
            messages.warning(
                request,
                _('Cannot remove label because it is in use')
            )
            return redirect('labels')
        label.delete()
        messages.success(
            request,
            _('Label deleted successfully!')
        )
        return redirect('labels')
