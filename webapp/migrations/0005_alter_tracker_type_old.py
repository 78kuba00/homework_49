# Generated by Django 4.1.3 on 2022-11-22 10:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_remove_tracker_type_tracker_type_old'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tracker',
            name='type_old',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tasks_set', to='webapp.trackertype', verbose_name='Тип'),
        ),
    ]