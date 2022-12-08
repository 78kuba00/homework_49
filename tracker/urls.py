from django.contrib import admin
from django.urls import path
from webapp.views import IndexViews, TaskView, CreateView, EditView, DeleteView, ProjectListView, ProjectDetail, ProjectCreate



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ProjectListView.as_view(), name='index'),
    path('project/<int:pk>/', ProjectDetail.as_view(), name='project_view'),
    path('project/add/', ProjectCreate.as_view(), name='project_add'),
    path('task/<int:pk>/', TaskView.as_view(), name='task_view'),
    path('task/<int:pk>/add/', CreateView.as_view(), name='task_add'),
    path('task/', IndexViews.as_view(), name='tasks_list'),
    path('task/<int:pk>/edit/', EditView.as_view(), name='task_edit'),
    path('task/<int:pk>/delete/', DeleteView.as_view(), name='task_delete')
]
