from django.contrib import admin

from .models import Location


class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'lat', 'lng', 'total_visits')
    list_display_links = ('name',)
    
admin.site.register(Location, LocationAdmin)
