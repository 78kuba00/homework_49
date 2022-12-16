from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy

from webapp.models import Tracker, Project
from webapp.forms import TaskForm, SimpleSearchForm
from django.views.generic import DetailView, CreateView
from webapp.views import SearchView, EditView, DeleteView


class IndexViews(SearchView):
    template_name = 'task/index.html'
    context_object_name = 'tasks'
    model = Tracker
    ordering = ('-updated_at',)
    paginate_by = 10
    paginate_orphans = 2
    search_form_class = SimpleSearchForm
    search_fields = ['summary__icontains', 'description__icontains']

    def post(self, request, *args, **kwargs):
        for task_pk in request.POST.getlist('tasks', []):
            self.model.objects.get(pk=task_pk).delete()
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class TaskView(DetailView):
    template_name = 'task/task_view.html'
    model = Tracker

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = get_object_or_404(Tracker, pk=self.kwargs.get('pk'))
        return context

class TaskCreate(LoginRequiredMixin, CreateView):
    template_name = 'task/create.html'
    model = Tracker
    form_class = TaskForm
    # context_object_name = 'tasks'
    # redirect_url = reverse_lazy('webapp:index')

    def form_valid(self, form):
        print(self.kwargs.get('pk'))
        form.instance.project = get_object_or_404(Tracker, pk=self.kwargs.get('pk'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('webapp:index', kwargs={'pk': self.object.pk})

class TaskEdit(LoginRequiredMixin, EditView):
    form_class = TaskForm
    template_name = 'task/task_edit.html'
    model = Tracker
    task = None
    context_object_name = 'tasks'
    redirect_url = 'webapp:index'


class TaskDelete(LoginRequiredMixin, DeleteView):
    template_name = 'task/task_delete.html'
    model = Tracker
    context_key = 'task'
    redirect_url = reverse_lazy('webapp:index')