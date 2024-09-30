from .models import Task
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django_filters.views import FilterView
from task_manager.mixins import AuthRequiredMixin, AuthorPermissionMixin
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from .filters import TaskFilter
from .forms import TaskForm
from django.contrib.auth import get_user_model


User = get_user_model()


class TasksIndexView(AuthRequiredMixin, FilterView):
    model = Task
    template_name = 'tasks/task_index.html'
    filterset_class = TaskFilter
    context_object_name = 'tasks'
    extra_context = {
        'title': _('Tasks'),
        'button_text': _('Show'),
    }
    ordering = ["pk"]


class TasksCreateView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "form.html"
    success_url = reverse_lazy('tasks_index')
    success_message = _('Task added')
    extra_context = {
        "title": _("Create task"),
        "button_text": _("Create"),
    }

    def form_valid(self, form):
        user = self.request.user
        form.instance.author = User.objects.get(pk=user.id)
        return super().form_valid(form)


class TasksUpdateView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks_index')
    success_message = _('Task updated')
    template_name = 'form.html'
    extra_context = {
        "title": _("Update task"),
        "button_text": _("Update"),
    }


class TasksDeleteView(
    AuthRequiredMixin,
    AuthorPermissionMixin,
    SuccessMessageMixin,
    DeleteView
):
    model = Task
    success_url = reverse_lazy('tasks_index')
    success_message = _('Task deleted')
    template_name = 'tasks/task_delete.html'
    author_message = _('The task can be deleted only by its author')
    author_url = reverse_lazy('tasks_index')
    permission_denied_url = reverse_lazy("tasks_index")
    permission_denied_message = _("Only the author of the task can delete it")
    extra_context = {
        "title": _("Delete task"),
        'text': _('Are you sure you want to delete'),
        "button_text": _('Yes, delete'),
    }


class TasksDetailView(AuthRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_details.html'
    extra_context = {
        "title": _("Detail task"),
    }
