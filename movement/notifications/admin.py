from django.contrib import admin

from .models import Notification

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'message', 'time_created', 'cohort')
    list_display_links = ('title',)
    model = Notification
admin.site.register(Notification, NotificationAdmin)
