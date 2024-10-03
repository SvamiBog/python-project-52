from .forms import LabelForm
from django.urls import reverse_lazy
from task_manager.labels.models import Label
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.mixins import AuthRequiredMixin, DeleteProtectionMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


class LabelIndexView(AuthRequiredMixin, ListView):
    model = Label
    context_object_name = 'labels'
    template_name = 'labels/labels_index.html'
    ordering = ['pk']


class LabelFormBaseView(AuthRequiredMixin, SuccessMessageMixin):
    model = Label
    form_class = LabelForm
    template_name = 'form.html'
    success_url = reverse_lazy('labels_index')


class LabelCreateView(LabelFormBaseView, CreateView):
    success_message = _('Successfully created label')
    extra_context = {
        'title': _('Create new label'),
        'button_text': _('Create'),
    }


class LabelUpdateView(LabelFormBaseView, UpdateView):
    success_message = _('Successfully updated label')
    extra_context = {
        'title': _('Update label'),
        'button_text': _('Update'),
    }


class LabelDeleteView(
    AuthRequiredMixin,
    DeleteProtectionMixin,
    SuccessMessageMixin,
    DeleteView
):
    model = Label
    template_name = 'labels/labels_delete.html'
    success_url = reverse_lazy('labels_index')
    success_message = _('Successfully deleted label')
    protected_message = _('You are not allowed to delete this label')
    protected_url = reverse_lazy('labels_index')
    extra_context = {
        'title': _('Delete label'),
        'text': _('Are you sure you want to delete'),
        'button_text': _('Yes, delete'),
    }
