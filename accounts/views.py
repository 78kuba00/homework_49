from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse

from .forms import MyUserCreationForm
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.list import MultipleObjectMixin
from accounts.models import Profile
# Create your views here.

class RegisterView(CreateView):
    model = get_user_model()
    form_class = MyUserCreationForm
    template_name = 'user_create.html'

    def form_valid(self, form):
        user = form.save()
        Profile.objects.create(user=user)
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        next_url = self.request.POST.get('next')
        if next_url:
            return next_url
        return reverse('webapp:index')

class UserDetailView(LoginRequiredMixin, DetailView, MultipleObjectMixin):
    model = get_user_model()
    template_name = 'user_detail.html'
    context_object_name = 'user_obj'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        projects = self.get_object().projects.all()
        return super().get_context_data(object_list=projects, **kwargs)

class UsersListView(PermissionRequiredMixin, ListView):
    model = get_user_model()
    template_name = 'users.html'
    context_object_name = 'users_obj'
    paginate_by = 5

    def has_permission(self):
        return self.request.user.has_perm('accounts.can_view_all_users') and self.request.user in User.objects.all() or self.request.user.is_superuser


