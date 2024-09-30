from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from task_manager.mixins import AuthRequiredMixin, DeleteProtectionMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from .forms import StatusForm
from .models import Status


class StatusIndexView(AuthRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'
    ordering = ["pk"]
    extra_context = {
        'title': _('Statuses')
    }


class StatusCreateView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'form.html'
    form_class = StatusForm
    login_url = reverse_lazy('login')
    success_message = _('Your status has been created.')
    success_url = reverse_lazy('status_index')
    extra_context = {
        'title': _('Create Status'),
        'button_text': _('Create'),
    }


class StatusUpdateView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'form.html'
    model = Status
    form_class = StatusForm
    success_url = reverse_lazy('status_index')
    success_message = _('Your status has been updated.')
    extra_context = {
        'title': _('Update Status'),
        'button_text': _('Update'),
    }


class StatusDeleteView(
    AuthRequiredMixin,
    DeleteProtectionMixin,
    SuccessMessageMixin,
    DeleteView
):
    template_name = 'statuses/delete.html'
    model = Status
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('status_index')
    success_message = _('Your status has been deleted.')
    protected_message = _('You are not allowed to delete this status.')
    protected_url = reverse_lazy('status_index')
    extra_context = {
        'title': _('Delete Status'),
        'text': _('Are you sure you want to delete'),
        'button_text': _('Yes, delete'),
    }
