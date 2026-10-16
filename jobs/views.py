from django.shortcuts import render
from rest_framework import generics,permissions, filters
from .models import JobPosting
from django_filters.rest_framework import DjangoFilterBackend
from.filters import JobFiltering
from .serializers import JobSerilaizer
from .permissions import IsRecuriter
from .permissions import IsRecuritorOwner

# Create your views here.
class JobPostingView(generics.ListCreateAPIView):
    queryset = JobPosting.objects.all()
    serializer_class= JobSerilaizer
    permission_classes= [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = JobFiltering
    search_fields = ['title']

    def perform_create(self, serializer):
        serializer.save(company = self.request.user.companys)

    def get_permissions(self):
        if self.request.method =="POST":
            permission_class =[IsRecuriter]
        else:
            permission_class=[permissions.AllowAny]

        return [permission() for permission in permission_class]


class JobRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobPosting.objects.all()
    serializer_class= JobSerilaizer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field='id'

    def get_permissions(self):
        if self.request.method in ["PATCH", "PUT", "DELETE"]:
            permission_class =[IsRecuritorOwner]
            
        else:
            permission_class=[permissions.AllowAny]
        
        return [permission() for permission in permission_class]
        
