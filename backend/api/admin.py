from django.contrib import admin
from .models import Developer
from .models import Game

@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    list_display = ('name', 'experience_years', 'available_to_hire')

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'platform', 'release_date')
    list_filter = ('platform',)
    search_fields = ('title',)
