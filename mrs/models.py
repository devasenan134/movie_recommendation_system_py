from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

# Create your models here.

class Genre(models.Model):
    genre = models.CharField(blank=False, max_length=30)
    
    def __str__(self):
        return self.genre
    
class Movie(models.Model):
    # movie_id = models.IntegerField(unique=True, primary_key=True, blank=False)
    title = models.CharField(max_length=50)
    language = models.CharField(max_length=50)
    year = models.PositiveIntegerField(default=None)
    runtime = models.PositiveIntegerField(blank=False)
    avg_rate = models.IntegerField(blank=True, default=1)
    no_votes = models.PositiveIntegerField(blank=True, default=0)
    genres = models.ManyToManyField(Genre, blank=True, related_name="genres")
    
    def __str__(self):
        str = f"{self.title} - {self.year}"
        return str
    
class Rating(models.Model):
    movie_id = models.ForeignKey(Movie, related_name="movie", on_delete=CASCADE)
    user_id = models.ForeignKey(User, related_name="user", on_delete=CASCADE)
    rate = models.IntegerField(blank=False)
     