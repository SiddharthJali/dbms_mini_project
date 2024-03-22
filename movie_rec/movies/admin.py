from django.contrib import admin
from .models import Movie, Rating, Watchlist, Recommendation

class MovieAdmin(admin.ModelAdmin):
    list_display = ('movie_id', 'title', 'release_year', 'genre', 'director', 'cast', 'status', 'movie_poster')
    list_filter = ('status', 'genre')
    search_fields = ('title', 'director', 'cast')
    list_per_page = 20

class RatingAdmin(admin.ModelAdmin):
    list_display = ('rating_id', 'user_profile', 'movie', 'rating')
    list_filter = ('rating',)
    search_fields = ('user_profile__user__username', 'movie__title')
    list_per_page = 20

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('watchlist_id', 'user_profile', 'movie')
    list_filter = ('user_profile__user__username',)
    search_fields = ('user_profile__user__username', 'movie__title')
    list_per_page = 20

class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('recommendation_id', 'user_profile', 'movie')
    list_filter = ('user_profile__user__username',)
    search_fields = ('user_profile__user__username', 'movie__title')
    list_per_page = 20

admin.site.register(Movie, MovieAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(Recommendation, RecommendationAdmin)

