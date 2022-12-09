from django.contrib import admin
from django.urls import path
from webapp.views import IndexViews, TaskView, TaskCreate, TaskEdit, TaskDelete, ProjectListView, ProjectDetail, \
    ProjectCreate, ProjectEdit, ProjectDelete

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ProjectListView.as_view(), name='index'),
    path('project/<int:pk>/', ProjectDetail.as_view(), name='project_view'),
    path('project/add/', ProjectCreate.as_view(), name='project_add'),
    path('project/<int:pk>/edit/', ProjectEdit.as_view(), name='project_edit'),
    path('project/<int:pk>/delete/', ProjectDelete.as_view(), name='project_delete'),
    path('task/<int:pk>/', TaskView.as_view(), name='task_view'),
    path('task/<int:pk>/add/', TaskCreate.as_view(), name='task_add'),
    path('task/', IndexViews.as_view(), name='tasks_list'),
    path('task/<int:pk>/edit/', TaskEdit.as_view(), name='task_edit'),
    path('task/<int:pk>/delete/', TaskDelete.as_view(), name='task_delete')
]
