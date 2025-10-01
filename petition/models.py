from django.db import models
from django.contrib.auth.models import User


class Petition(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='liked_petitions', blank=True)

    def __str__(self):
        return f"{self.id} - {self.title}"
