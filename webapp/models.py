from django.db import models
from webapp.validate import at_least_10, MinLengthValidator
from django.core.validators import MaxLengthValidator

# Create your models here.
class TrackerStatus(models.Model):
    title = models.CharField(max_length=60, verbose_name="Название")

    def __str__(self):
        return self.title

class TrackerType(models.Model):
    title = models.CharField(max_length=60, verbose_name="Название")
    # tracker = models.ForeignKey('webapp.Tracker', related_name='tracker_types', on_delete=models.CASCADE, verbose_name='Трекер')

    def __str__(self):
        return self.title

class Tracker(models.Model):
    summary = models.CharField(max_length=200, null=False, blank=False, verbose_name='Краткое описание', validators=(MinLengthValidator(6),))
    description = models.TextField(max_length=3000, null=True, blank=True, verbose_name='Полное описание', validators=(at_least_10, ))
    status = models.ManyToManyField('webapp.TrackerStatus', related_name='tasks', verbose_name='Статус', null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    type = models.ManyToManyField('webapp.TrackerType', related_name='tasks_new', null=True)

    def __str__(self):
        return f'{self.pk}. {self.summary}'