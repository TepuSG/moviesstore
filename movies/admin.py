from django.contrib import admin
from .models import Movie, Review, Rating


class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']


class RatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'movie__name']
    readonly_fields = ['created_at', 'updated_at']


admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)
admin.site.register(Rating, RatingAdmin)
# Register your models here.
