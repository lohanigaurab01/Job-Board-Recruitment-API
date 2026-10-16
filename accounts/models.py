from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    role_choices =(
        ('recruiter', 'Recruiter'),
        ('candidate', 'Candidate'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE ,related_name = 'profile')
    role = models.CharField(choices=role_choices)
    age = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user } Profile'