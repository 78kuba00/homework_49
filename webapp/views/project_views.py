from django.core.paginator import Paginator
from django.urls import reverse

from webapp.models import Project
from django.views.generic import ListView, DetailView, CreateView
from webapp.forms import ProjectForm
from webapp.views import EditView


class ProjectListView(ListView):
    template_name = 'project/index.html'
    model = Project
    context_object_name = 'projects'
    ordering = '-start_at'

class ProjectDetail(DetailView):
    model = Project
    template_name = 'project/project_view.html'

    def get_context_data(self, **kwargs):
        projects = self.object.projects.all()
        paginator = Paginator(projects, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = super().get_context_data(**kwargs)
        context['page_obj'] = page_obj
        context['is_paginated'] = page_obj.has_other_pages()
        context['tasks'] = page_obj.object_list
        return context

class ProjectCreate(CreateView):
    model = Project
    template_name = 'project/create.html'
    form_class = ProjectForm

    def get_success_url(self):
        return reverse('project_view', kwargs={'pk': self.object.pk})

class ProjectEdit(EditView):
    model = Project
    template_name = 'project/project_edit.html'
    form_class = ProjectForm
    context_object_name = 'project'

    def get_success_url(self):
        return reverse('project_view', kwargs={'pk': self.object.pk})
