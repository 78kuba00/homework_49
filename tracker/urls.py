from django.contrib import admin
from django.urls import path
from webapp.views import IndexViews, TaskView, CreateView, EditView, DeleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexViews.as_view(), name='index'),
    path('task/<int:pk>/', TaskView.as_view(), name='task_view'),
    path('task/add/', CreateView.as_view(), name='task_add'),
    path('task/<int:pk>/edit/', EditView.as_view(), name='task_edit'),
    path('task/<int:pk>/delete/', DeleteView.as_view(), name='task_delete')
]
