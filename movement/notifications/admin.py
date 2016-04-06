from django.contrib import admin

from .models import Notification

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('status', 'id', 'title', 'message', 'time_created', 'cohort')
    model = Notification
admin.site.register(Notification, NotificationAdmin)
