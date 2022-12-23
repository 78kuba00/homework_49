from django.contrib import admin
from webapp.models import Tracker, TrackerType, TrackerStatus, Project
# Register your models here.
class TrackerAdmin(admin.ModelAdmin):
    list_display = ['id', 'summary', 'description']
    list_filter = ['summary']
    exclude = []
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

class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'start_at']
    list_display_links = ['title']
    list_filter = ['title']
    # fields = ['title', 'description', 'users', 'start_at', 'updated_at']

class TypeAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_display_links = ['title']
    list_filter = ['title']
    search_fields = ['title']
    fields = ['title']

class StatusAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_display_links = ['title']
    list_filter = ['title']
    search_fields = ['title']
    fields = ['title']


admin.site.register(Tracker)
admin.site.register(TrackerStatus, StatusAdmin)
admin.site.register(TrackerType, TypeAdmin)
admin.site.register(Project, ProjectAdmin)
