from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import Profile


class Movie(models.Model):
    ADVENTURE = 'Adventure'
    HORROR = 'Horror'
    ROMANCE = 'Romance'
    ACTION = 'Action'
    COMEDY = 'Comedy'

    GENRE_CHOICES = [
        (ADVENTURE, 'Adventure'),
        (HORROR, 'Horror'),
        (ROMANCE, 'Romance'),
        (ACTION, 'Action'),
        (COMEDY, 'Comedy'),
    ]

    STATUS_CHOICES = (
        ('T', 'Trending'),
        ('N', 'Not Trending'),
    )

    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='T')
    movie_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    release_year = models.IntegerField()
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES)
    director = models.CharField(max_length=255)
    cast = models.CharField(max_length=255)
    movie_poster = models.ImageField(upload_to='movie_posters/')

    def __str__(self):
        return self.title


class Rating(models.Model):
    rating_id = models.AutoField(primary_key=True)
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)], null=False)

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.movie.title} - {self.rating}"


class Watchlist(models.Model):
    watchlist_id = models.AutoField(primary_key=True)
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.movie.title} Watchlist"


class Recommendation(models.Model):
    recommendation_id = models.AutoField(primary_key=True)
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.movie.title} Recommendation"
