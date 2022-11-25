from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import View, TemplateView
from webapp.models import TrackerType, Tracker, TrackerStatus
from webapp.forms import TaskForm

from django.views.generic import TemplateView, RedirectView, FormView
from webapp.base_views import FormView as CustomFormView

class IndexView(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Tracker.objects.all()
        return context
    def post(self, request, *args, **kwargs):
        for task_pk in request.POST.getlist('tasks', []):
            Tracker.objects.get(pk=task_pk).delete()
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

class TaskView(TemplateView):
    template_name = 'task_view.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = get_object_or_404(Tracker, pk=kwargs['pk'])
        return context

class MyRedirectView(RedirectView):
    url = 'https://ccbv.co.uk/projects/Django/4.1/django.views.generic.base/RedirectView/'

class CreateView(CustomFormView):
    template_name = 'create.html'
    form_class = TaskForm

    def get_redirect_url(self):
        return reverse('task_view', kwargs={'pk': self.task.pk})

    def form_valid(self, form):
        self.task = form.save()
        return super().form_valid(form)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['form'] = TaskForm()
    #     return context
    # def post(self, request, *args, **kwargs):
    #     form = TaskForm(data=request.POST)
    #     if form.is_valid():
    #         types = form.cleaned_data.pop('type')
    #         task = Tracker.objects.create(**form.cleaned_data)
    #         task.type.set(types)
    #         return redirect('task_view', pk=task.pk)
    #     else:
    #         context = self.get_context_data(**kwargs)
    #         context['form'] = form
    #         return self.render_to_response(context)

class EditView(FormView):
    template_name = "task_edit.html"
    form_class = TaskForm

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Tracker, pk=pk)

    def dispatch(self, request, *args, **kwargs):
        self.task = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = self.task
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.task
        return kwargs

    def form_valid(self, form):
        self.task = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('task_view', kwargs={'pk': self.task.pk})

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Tracker, pk=pk)

    #
    # def get(self, request, *args, **kwargs):
    #     task = get_object_or_404(Tracker, pk=kwargs['pk'])
    #     form = TaskForm(initial={
    #         'summary': task.summary,
    #         'description': task.description,
    #         'status': task.status,
    #         'type': task.type.all()
    #     })
    #     return render(request, 'task_edit.html', {'form': form})
    #
    # def post (self, request, *args, **kwargs):
    #     task = get_object_or_404(Tracker, pk=kwargs['pk'])
    #     form = TaskForm(data=request.POST)
    #     if form.is_valid():
    #         task.summary = form.cleaned_data['summary']
    #         task.description = form.cleaned_data['description']
    #         task.status = form.cleaned_data['status']
    #         task.save()
    #         task.type.set(form.cleaned_data['type'])
    #         return redirect('task_view', pk=task.pk)
    #     else:
    #         return render(request, 'task_edit.html', {'form': form})

class DeleteView(View):
   def get(self, request, *args, **kwargs):
       task = get_object_or_404(Tracker, pk=kwargs['pk'])
       return render(request, 'task_delete.html', {'task': task})
   def post(self, request, *args, **kwargs):
       task = get_object_or_404(Tracker, pk=kwargs['pk'])
       task.delete()
       return redirect('index')