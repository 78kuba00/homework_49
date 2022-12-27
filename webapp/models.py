from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


# Create your models here.
class TrackerStatus(models.Model):
    title = models.CharField(max_length=60, verbose_name="Название")

    def __str__(self):
        return self.title

class TrackerType(models.Model):
    title = models.CharField(max_length=60, verbose_name="Название")

    def __str__(self):
        return self.title

class Tracker(models.Model):
    summary = models.CharField(max_length=200, null=False, blank=False, verbose_name='Краткое описание')
    description = models.TextField(max_length=3000, null=True, blank=True, verbose_name='Полное описание')
    status = models.ForeignKey('webapp.TrackerStatus', related_name='tasks', on_delete=models.PROTECT, verbose_name='Статус', null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    type = models.ManyToManyField('webapp.TrackerType', related_name='tasks_new')
    project = models.ForeignKey('webapp.Project', related_name='projects', on_delete=models.CASCADE, default=1, verbose_name='Проект')

    def get_absolute_url(self):
        return reverse('webapp:index', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.pk}. {self.summary}'

class Project(models.Model):
    start_at = models.DateField(null=True, blank=True, verbose_name="Дата начала")
    end_at = models.DateField(null=True, blank=True, verbose_name="Дата окончания")
    title = models.CharField(max_length=60, verbose_name="Название")
    description = models.TextField(max_length=3000, null=True, blank=True, verbose_name='Описание')
    users = models.ManyToManyField(get_user_model(), related_name='projects', default=1, verbose_name='Пользователь')

    class Meta:
        db_table = "webapp_project"
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
        permissions = [
            ('can_add_users_to_the_project', 'Can add users to project'),
            ('can_delete_users_to_the_project', 'Can delete users in projects'),
            ('can_view_all_users', 'Can view all users')
        ]

    def __str__(self):
        return f'{self.id}. {self.title}'