# Generated by Django 4.1.3 on 2022-11-22 10:23

from django.db import migrations

# def transfer_tags(apps, schema_editor):
#     Tracker = apps.get_model('webapp.Tracker')
#     for tracker in Tracker.objects.all():
#         tracker.type.set(tracker.type_old.all())
#
#
# def rollback_transfer(apps, schema_editor):
#     Tracker = apps.get_model('webapp.Tracker')
#     for tracker in Tracker.objects.all():
#         tracker.type_old.set(tracker.type.all())

class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0007_alter_tracker_type'),
    ]

    operations = [
        # migrations.RunPython(transfer_tags, rollback_transfer)
    ]
