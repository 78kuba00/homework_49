# Generated by Django 4.1.3 on 2022-11-22 12:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0008_auto_20221122_1023'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tracker',
            name='type_old',
        ),
    ]