# Generated by Django 4.1.3 on 2022-12-15 17:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0011_project_tracker_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tracker',
            name='project',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='webapp.project', verbose_name='Проект'),
        ),
    ]
