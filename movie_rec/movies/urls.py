from django.urls import path
from .views import home, movie_detail, submit_rating, add_to_watchlist
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('search/', views.search, name='search'),
    path('all_movies/', views.all_movies, name='all_movies'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('movie/<int:movie_id>/submit_rating/', views.submit_rating, name='submit_rating'),
    path('movie/<int:movie_id>/add_to_watchlist/', add_to_watchlist, name='add_to_watchlist'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)