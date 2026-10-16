from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Company(models.Model):
    owners = models.OneToOneField(User, on_delete=models.CASCADE, related_name='companys')
    name = models.CharField()
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.owners} company'
