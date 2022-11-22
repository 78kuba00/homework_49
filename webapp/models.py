from django.db import models

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

# class TrackerTypeTag(models.Model):
#     tag = models.ForeignKey('webapp.TrackerType', related_name='tag_types', on_delete=models.CASCADE, verbose_name='Тег')
#


class Tracker(models.Model):
    summary = models.CharField(max_length=200, null=False, blank=False, verbose_name='Краткое описание')
    description = models.TextField(max_length=3000, null=True, blank=True, verbose_name='Полное описание')
    status = models.ForeignKey('webapp.TrackerStatus', related_name='tasks', on_delete=models.PROTECT, verbose_name='Статус', null=True)
    # type_old = models.ForeignKey('webapp.TrackerType', related_name='tasks_set', on_delete=models.PROTECT, verbose_name='Тип')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    type = models.ManyToManyField('webapp.TrackerType', related_name='tasks_new', blank=True)

    def __str__(self):
        return f'{self.pk}. {self.summary}'