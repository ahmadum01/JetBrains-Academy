from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Resume(models.Model):
    description = models.CharField(max_length=1024)
    author = models.ForeignKey(User, on_delete=models.CASCADE)