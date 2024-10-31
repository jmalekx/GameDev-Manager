from django.contrib import admin
from .models import Developer, Game, GameDeveloper

@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    list_display = ('name', 'experience_years', 'available_to_hire')
    ordering = ('-join_date',)

class GameDeveloperInline(admin.TabularInline):
    model = Game.developer.through
    extra = 2

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'platform', 'release_date')
    list_filter = ('platform',)
    search_fields = ('title',)
    inlines = (GameDeveloperInline,)
    ordering = ('-release_date',)
