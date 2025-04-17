# admin.py
from django.contrib import admin
from .models import Profile, Blog

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'birth_date')
    search_fields = ('user__username', 'location')
    list_filter = ('birth_date',)

admin.site.register(Profile, ProfileAdmin)

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'is_trending']  # Add is_trending here