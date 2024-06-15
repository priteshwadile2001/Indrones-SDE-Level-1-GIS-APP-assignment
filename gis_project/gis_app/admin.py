from django.contrib import admin
from .models import Location, Boundary

class AdminLocation(admin.ModelAdmin):
    list_display = ('name', 'coordinates', 'description', 'created_at', 'updated_at')

class AdminBoundary(admin.ModelAdmin):
    list_display = ('name', 'area', 'created_at', 'updated_at')

admin.site.register(Location, AdminLocation)
admin.site.register(Boundary, AdminBoundary)
