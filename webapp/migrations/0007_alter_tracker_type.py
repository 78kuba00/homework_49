# Generated by Django 4.1.3 on 2022-11-22 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_tracker_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tracker',
            name='type',
            field=models.ManyToManyField(blank=True, related_name='tasks_new', to='webapp.trackertype'),
        ),
    ]
