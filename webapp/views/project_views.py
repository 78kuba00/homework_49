from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.urls import reverse

from webapp.models import Project
from django.views.generic import ListView, DetailView, CreateView, DeleteView, RedirectView, UpdateView
from webapp.forms import ProjectForm



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

class MyRedirectView(RedirectView):
    url = 'https://ccbv.co.uk/projects/Django/4.1/django.views.generic.base/RedirectView/'


class ProjectCreate(LoginRequiredMixin, CreateView):
    model = Project
    template_name = 'project/create.html'
    form_class = ProjectForm

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.pk})
    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         return super().dispatch(request, *args, **kwargs)
    #     return redirect('accounts:login')
    #
    # def get_success_url(self):
    #     return reverse('webapp:project_view', kwargs={'pk': self.object.pk})

class ProjectEdit(LoginRequiredMixin, UpdateView):
    model = Project
    template_name = 'project/project_edit.html'
    form_class = ProjectForm
    context_object_name = 'project'
    redirect_url = 'webapp:index'

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.pk})

class ProjectDelete(LoginRequiredMixin, DeleteView):
    model = Project
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('webapp:index')
