from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.utils.translation import gettext as _

from .models import StatusModel
from .forms import StatusModelForm
from .mixins import CustomLoginRequiredMixin


class StatusesView(CustomLoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        statuses = StatusModel.objects.all()
        return render(request, 'statuses/statuses.html', {'statuses': statuses})


class CreateStatus(CustomLoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return render(request, 'statuses/create.html')

    def post(self, request, *args, **kwargs):
        status_form = StatusModelForm(request.POST)

        if status_form.is_valid():
            status_form.save()
            messages.success(
                request, _('Status successfully created')
            )
            return redirect('statuses')

        return render(request, 'statuses/create.html', {'form': status_form})


class UpdateStatus(CustomLoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        status_pk = kwargs.get('pk')
        status = get_object_or_404(StatusModel, id=status_pk)
        form = StatusModelForm(instance=status)
        return render(
            request,
            'statuses/update.html',
            {'form': form, 'status_pk': status_pk, 'status': status}
        )

    def post(self, request, *args, **kwargs):
        status_pk = kwargs.get('pk')
        status = get_object_or_404(StatusModel, id=status_pk)
        form = StatusModelForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            messages.success(request, _('Status successfully changed'))
            return redirect('statuses')

        return render(
            request,
            'statuses/update.html',
            {'form': form, 'status_pk': status_pk}
        )


class DeleteStatus(CustomLoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        status_pk = kwargs.get('pk')
        status = get_object_or_404(StatusModel, id=status_pk)
        return render(
            request,
            'statuses/delete.html',
            {'status_pk': status_pk, 'status': status}
        )

    def post(self, request, *args, **kwargs):
        status_pk = kwargs.get('pk')
        status = get_object_or_404(StatusModel, id=status_pk)
        status.delete()
        messages.success(
            request,
            _('Status deleted successfully!')
        )
        return redirect('statuses')
