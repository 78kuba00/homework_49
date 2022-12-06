from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import View
from webapp.models import Tracker, Project
from webapp.forms import TaskForm, SimpleSearchForm
from django.db.models import Q
from django.utils.http import urlencode

from django.views.generic import TemplateView, RedirectView, FormView, ListView, DetailView, CreateView
from .base_views import FormView as CustomFormView


class IndexViews(ListView):
    template_name = 'task/index.html'
    context_object_name = 'tasks'
    model = Tracker
    ordering = ('-updated_at',)
    paginate_by = 10
    paginate_orphans = 2

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_search_form(self):
        return SimpleSearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        # return None

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = Q(summary__icontains=self.search_value)| Q(description__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
            context['search'] = self.search_value
        return context

class TaskView(DetailView):
    template_name = 'task/task_view.html'
    model = Tracker
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # task = self.object
        # projects = task.project
        # context['projects'] = projects
        return context

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['task'] = get_object_or_404(Tracker, pk=kwargs['pk'])
    #     return context

class MyRedirectView(RedirectView):
    url = 'https://ccbv.co.uk/projects/Django/4.1/django.views.generic.base/RedirectView/'


class TrackerForm:
    pass


class CreateView(CreateView):
    template_name = 'task/create.html'
    model = Tracker
    form_class = TaskForm


class EditView(FormView):
    template_name = "task/task_edit.html"
    form_class = TaskForm
    task = None

    def dispatch(self, request, *args, **kwargs):
        self.task = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Tracker, pk=pk)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['task'] = self.task
    #     return context

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


class DeleteView(View):
    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Tracker, pk=kwargs['pk'])
        return render(request, 'task/task_delete.html', {'task': task})
    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Tracker, pk=kwargs['pk'])
        task.delete()
        return redirect('index')