from django.contrib import admin

from .models import LocationCategory, Location, CohortAssociation, UserReveal

class LocationCategoryAdmin(admin.ModelAdmin):
    model = LocationCategory
admin.site.register(LocationCategory, LocationCategoryAdmin)

class CohortAssociationAdmin(admin.TabularInline):
    model = CohortAssociation

class UserRevealAdmin(admin.TabularInline):
    model = UserReveal

class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'lat', 'lng', '_total_visits', '_total_reveals')
    list_display_links = ('name',)
    inlines = [
        LocationCategoryAdmin,
        CohortAssociationAdmin,
        UserRevealAdmin
    ]
    
    def _total_visits(self, obj):
        return obj.get_total_visits( )
    
    def _total_reveals(self, obj):
        return obj.get_total_reveals( )
    
admin.site.register(Location, LocationAdmin)