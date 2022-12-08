from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from webapp.models import Tracker, Project
from webapp.forms import TaskForm, SimpleSearchForm
from django.views.generic import TemplateView, View, DetailView, CreateView
from webapp.views import SearchView

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

class CreateView(CreateView):
    template_name = 'task/create.html'
    model = Tracker
    form_class = TaskForm

    def form_valid(self, form):
        form.instance.project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('project_view', kwargs={'pk': self.object.project.pk})


class EditView(View):
    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Tracker, pk=kwargs['pk'])
        form = TaskForm(instance=task)
        return render(request, 'task/task_edit.html', {'form': form, 'task': task})

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Tracker, pk=kwargs['pk'])
        form = TaskForm(instance=task, data=request.POST)
        if form.is_valid():
            task = form.save()
            return redirect('task_view', pk=task.pk)
        else:
            return render(request, 'task/task_edit.htmll', {'form': form, 'task': task})


class DeleteView(View):
    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Tracker, pk=kwargs['pk'])
        return render(request, 'task/task_delete.html', {'task': task})
    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Tracker, pk=kwargs['pk'])
        task.delete()
        return redirect('index')