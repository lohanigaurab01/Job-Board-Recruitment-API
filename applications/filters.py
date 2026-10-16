import django_filters
from .models import Application


class StatusFilter(django_filters.FilterSet):
    message = "no status avaibale"
    status = django_filters.CharFilter(field_name="status", lookup_expr="icontains")

    class Meta:
        model = Application
        fields = ['status',]
