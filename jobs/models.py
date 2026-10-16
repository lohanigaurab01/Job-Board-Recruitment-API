from django.db import models
from company.models import Company
from django.core.exceptions import ValidationError
# Create your models here.
class JobPosting(models.Model):
    JOB_TYPE_CHOICES = (
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('internship', 'Internship'),
        ('remote', 'Remote'),
    )
    STATUS_CHOICES = (('open', 'Open'), ('closed', 'Closed'))

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField()
    skills = models.CharField(max_length=500, help_text="comma-separated")
    location = models.CharField(max_length=255)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    salary_min = models.IntegerField(null=True, blank=True)
    salary_max = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.company} has open a job on {self.title}'

    def clean(self):
        if self.salary_min>self.salary_max:
            raise ValidationError(f'the salary minimum cannot be greather than salary maximium')


class ScreeningQuestion(models.Model):
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=500)