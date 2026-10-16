import django_filters
from .models import JobPosting

class JobFiltering(django_filters.FilterSet):

    location = django_filters.CharFilter(field_name='location', lookup_expr='iexact')
    salary_min = django_filters.NumberFilter(field_name='salary_min', lookup_expr='gte')
    salary_max = django_filters.NumberFilter(field_name='salary_max', lookup_expr='lte')
    
    class Meta:
        model = JobPosting
        fields =[]
        