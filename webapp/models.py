from django.db import models

# Create your models here.
class TrackerStatus(models.Model):
    title = models.CharField(max_length=60, verbose_name="Название")

    def __str__(self):
        return f'{self.pk}. {self.title}'

class TrackerType(models.Model):
    title = models.CharField(max_length=60, verbose_name="Название")

    def __str__(self):
        return f'{self.pk}. {self.title}'

class Tracker(models.Model):
    summary = models.CharField(max_length=200, null=False, blank=False, verbose_name='Краткое описание')
    description = models.TextField(max_length=3000, null=True, blank=True, verbose_name='Полное описание')
    status = models.ForeignKey(TrackerStatus, on_delete=models.PROTECT, verbose_name='Статус', null=True)
    type = models.ForeignKey(TrackerType, on_delete=models.PROTECT, verbose_name='Тип', null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время изменения')

    def __str__(self):
        return f'{self.pk}. {self.summary}'