from django.db import models
from django.contrib.auth.models import User
class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')

    def __str__(self):
        return str(self.id) + ' - ' + self.name

    def average_rating(self):
        """Calculate the average rating for this movie"""
        ratings = self.rating_set.all()
        if ratings:
            return sum(rating.rating for rating in ratings) / len(ratings)
        return 0

    def rating_count(self):
        """Get total number of ratings for this movie"""
        return self.rating_set.count()
class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    rating = models.IntegerField(default=5)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie,
        on_delete=models.CASCADE)
    user = models.ForeignKey(User,
        on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='liked_reviews', blank=True)
    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'movie')  # One rating per user per movie

    def __str__(self):
        return f'{self.user.username} - {self.movie.name} - {self.rating} stars'


# Create your models here.
