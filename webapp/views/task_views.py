from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy

from webapp.models import Tracker, Project
from webapp.forms import TaskForm, SimpleSearchForm
from django.views.generic import View, DetailView, CreateView
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

class TaskCreate(CreateView):
    template_name = 'task/create.html'
    model = Tracker
    form_class = TaskForm

    # def form_valid(self, form):
    #     form.instance.project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
    #     return super().form_valid(form)

    # def get_success_url(self):
    #     return reverse('project_view', kwargs={'pk': self.object.project.pk})


# class TaskEdit(EditView):
    # def get(self, request, *args, **kwargs):
    #     task = get_object_or_404(Tracker, pk=kwargs['pk'])
    #     form = TaskForm(instance=task)
    #     return render(request, 'task/task_edit.html', {'form': form, 'task': task})
    #
    # def post(self, request, *args, **kwargs):
    #     task = get_object_or_404(Tracker, pk=kwargs['pk'])
    #     form = TaskForm(instance=task, data=request.POST)
    #     if form.is_valid():
    #         task = form.save()
    #         return redirect('task_view', pk=task.pk)
    #     else:
    #         return render(request, 'task/task_edit.html', {'form': form, 'task': task})
class TaskEdit(EditView):
    form_class = TaskForm
    template_name = 'task/task_edit.html'
    model = Tracker
    task = None
    context_object_name = 'tasks'
    redirect_url = 'index'


    # def dispatch(self, request, *args, **kwargs):
    #     self.task = self.get_object()
    #     return super().dispatch(request, *args, **kwargs)

    # def get_success_url(self):
    #     return reverse('task/task_view.html', kwargs={'pk': self.object.pk})

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs['instance'] = self.task
    #     return kwargs

    # def form_valid(self, form):
    #     self.task = form.save()
    #     return super().form_valid(form)

    # def get_object(self):
    #     return get_object_or_404(Tracker, pk=self.kwargs.get('pk'))

class TaskDelete(DeleteView):
    template_name = 'task/task_delete.html'
    model = Tracker
    context_key = 'task'
    redirect_url = reverse_lazy('index')
    # def get(self, request, *args, **kwargs):
    #     task = get_object_or_404(Tracker, pk=kwargs['pk'])
    #     return render(request, 'task/task_delete.html', {'task': task})
    # def post(self, request, *args, **kwargs):
    #     task = get_object_or_404(Tracker, pk=kwargs['pk'])
    #     task.delete()
    #     return redirect('index')