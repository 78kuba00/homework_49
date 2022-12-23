from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import redirect
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
    permission_required = "webapp.add_project"

    # def form_valid(self, form):
    #     form.instance.users = self.request.user
    #     # a2.publications.add(p1, p2)
    #     return super().form_valid(form)

    # def dispatch(self, request, *args, **kwargs):
    #     if not request.user.is_authenticated:
    #         return redirect('accounts:login')
    #     if not request.user.has_perm('webapp.add_project'):
    #         raise PermissionDenied
    #     return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.pk})


class ProjectEdit(PermissionRequiredMixin, UpdateView):
    model = Project
    template_name = 'project/project_edit.html'
    form_class = ProjectForm
    context_object_name = 'project'
    redirect_url = 'webapp:index'
    permission_required = 'webapp.change_project'

    def has_permission(self):
        return super().has_permission() or self.get_object().users == self.request.user

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.pk})

class ProjectDelete(PermissionRequiredMixin, DeleteView):
    model = Project
    permission_required = 'webapp.delete_project'

    def has_permission(self):
        return super().has_permission() or self.get_object().author == self.request.user

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('webapp:index')
