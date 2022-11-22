from django.contrib import admin
from webapp.models import Tracker, TrackerType, TrackerStatus
# Register your models here.
# class TrackerAdmin(admin.ModelAdmin):
#     list_display = ['id', 'summary', 'description']
#     list_filter = ['summary']
#     exclude = []
#
# class TrackerStatusAdmin(admin.ModelAdmin):
#     list_display = ['id', 'title']
#     list_filter = ['title']
#     exclude = []
#
# class TrackerTypeAdmin(admin.ModelAdmin):
#     list_display = ['id', 'title']
#     list_filter = ['title']
#     exclude = []

admin.site.register(Tracker)
admin.site.register(TrackerStatus)
admin.site.register(TrackerType)