from django.db import models
from applications.models import Application
from django.contrib.auth.models import User

# Create your models here.
class Interview(models.Model):
    MODE_CHOICES = (
    ('onsite', 'Onsite'), 
    ('remote', 'Remote'),
    ('phone', 'Phone')
    )
    
    STATUS_CHOICES = (
    ('scheduled', 'Scheduled'), 
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'))

    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='interviews')
    scheduled_at = models.DateTimeField()
    interviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    mode = models.CharField(max_length=20, choices=MODE_CHOICES)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')