from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from .models import Movie, Recommendation, Watchlist, Rating
from users.models import Profile
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from .models import Recommendation

def home(request):
    trending_movies = Movie.objects.filter(status='T').order_by('-release_year')
    watchlist_movies = []
    recommended_movies = []

    if request.user.is_authenticated:
        user_profile = request.user.profile

        watchlist_entries = Watchlist.objects.filter(
            user_profile=user_profile).select_related('movie')
        watchlist_movies = [
            watchlist_entry.movie for watchlist_entry in watchlist_entries]

        highly_rated_movies = Rating.objects.filter(
            user_profile=user_profile, rating__gt=6).select_related('movie')
        highly_rated_movies = [
            rating.movie for rating in highly_rated_movies]

        all_reference_movies = watchlist_movies + highly_rated_movies

        reference_directors = set(movie.director for movie in all_reference_movies)
        reference_genres = set(movie.genre for movie in all_reference_movies)

        recommended_movies = Movie.objects.filter(
            ~Q(pk__in=[movie.pk for movie in watchlist_movies]),
            Q(director__in=reference_directors) | Q(genre__in=reference_genres)
        ).exclude(pk__in=[movie.pk for movie in highly_rated_movies])

        for movie in recommended_movies:
            Recommendation.objects.get_or_create(user_profile=user_profile, movie=movie)
        Recommendation.objects.filter(
            user_profile=user_profile, movie__in=highly_rated_movies
        ).exclude(movie__in=recommended_movies).delete()



        context = {
            'trending_movies': trending_movies,
            'recommended_movies': recommended_movies,
            'watchlist_movies': watchlist_movies,
        }

    else:
        context = {
            'trending_movies': trending_movies,
            'recommended_movies': [],
            'watchlist_movies': [],
        }

    return render(request, 'movies/home.html', context)


def all_movies(request):
    all_movies = Movie.objects.all()

    context = {
        'all_movies': all_movies,
    }

    return render(request, 'movies/all_movies.html', context)



def search(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = Movie.objects.filter(title__icontains=query)

    return render(request, 'movies/search_results.html', {'results': results, 'query': query})


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    user_profile = request.user.profile
    user_rating = Rating.objects.filter(user_profile=user_profile, movie=movie).first()
    in_watchlist = Watchlist.objects.filter(user_profile=user_profile, movie=movie).exists()

    if request.method == 'POST':
        if 'rating' in request.POST:
            rating_value = float(request.POST.get('rating'))
            rating, created = Rating.objects.get_or_create(
                user_profile=user_profile, movie=movie)
            rating.rating = rating_value
            rating.save()
            messages.success(
                request, f'Your rating ({rating_value}) has been saved!')
        elif 'add_watchlist' in request.POST:
            Watchlist.objects.get_or_create(user_profile=user_profile, movie=movie)
            messages.success(request, f'{movie.title} has been added to your watchlist!')
        elif 'remove_watchlist' in request.POST:
            Watchlist.objects.filter(user_profile=user_profile, movie=movie).delete()
            messages.success(request, f'{movie.title} has been removed from your watchlist!')

        return redirect('movie_detail', movie_id=movie_id)

    return render(request, 'movies/movie_detail.html', {'movie': movie, 'in_watchlist': in_watchlist, 'user_rating': user_rating})


def submit_rating(request, movie_id):
    if request.method == 'POST' and request.user.is_authenticated:
        user_profile = request.user.profile
        movie = get_object_or_404(Movie, pk=movie_id)
        rating_value = float(request.POST.get('rating'))

        existing_rating = Rating.objects.filter(
            user_profile=user_profile, movie=movie).first()

        if existing_rating:
            existing_rating.rating = rating_value
            existing_rating.save()
        else:
            Rating.objects.create(user_profile=user_profile,
                                  movie=movie, rating=rating_value)

        # Redirect back to the movie_detail view
        return redirect('movie_detail', movie_id=movie_id)

    return JsonResponse({'success': False, 'message': 'Failed to submit rating.'})


def add_to_watchlist(request, movie_id):
    if request.method == 'POST' and request.user.is_authenticated:
        user_profile = request.user.profile
        movie = get_object_or_404(Movie, pk=movie_id)

        # Check if the movie is already in the user's watchlist
        existing_watchlist_entry = Watchlist.objects.filter(
            user_profile=user_profile, movie=movie).first()

        if not existing_watchlist_entry:
            # Add the movie to the watchlist
            Watchlist.objects.create(user_profile=user_profile, movie=movie)

        return JsonResponse({'success': True, 'message': f'{movie.title} has been added to your watchlist!'})

    return JsonResponse({'success': False, 'message': 'Failed to add to watchlist.'})