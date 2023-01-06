from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse

from webapp.models import Project
from django.views.generic import ListView, DetailView, CreateView, DeleteView, RedirectView, UpdateView
from webapp.forms import ProjectForm, ChangeUsersInProjectsForm



class ProjectListView(ListView):
    template_name = 'project/index.html'
    model = Project
    context_object_name = 'projects'
    ordering = '-start_at'
    paginate_by = 4

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


class ProjectCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Project
    template_name = 'project/create.html'
    form_class = ProjectForm
    permission_required = "webapp.add_project"

    def form_valid(self, form):
        self.object = form.save()
        self.object.users.add(self.request.user)
        return super().form_valid(form)

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
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        # return super().has_permission() or self.get_object().users == self.request.user
        return super().has_permission() and self.request.user in project.users.all()

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.pk})

class ProjectDelete(PermissionRequiredMixin, DeleteView):
    model = Project
    permission_required = 'webapp.delete_project'

    def has_permission(self):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        return super().has_permission() and self.request.user in project.users.all()

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('webapp:index')

class ChangeUsersInProjectView(PermissionRequiredMixin, UpdateView):
    model = Project
    form_class = ChangeUsersInProjectsForm
    template_name = 'project/change_user.html'
    permission_required = 'webapp.can_add_users_to_the_project'

    def has_permission(self):
        return super().has_permission() and self.request.user in self.get_object().users.all()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['users'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.pk})
