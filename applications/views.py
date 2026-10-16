from django.shortcuts import render,get_object_or_404
from rest_framework import generics
from .models import Application
from .serializers import ApplicationPostSerializer,ApplicationListSerializer
from rest_framework import permissions, filters
from jobs.models import JobPosting
from django_filters.rest_framework import DjangoFilterBackend
from .permission import IsCandidate, IsRecruiterOrOwner
from .filters import StatusFilter

# Create your views here.
class ApplicationCreate(generics.ListCreateAPIView):
    queryset = Application.objects.all()
    serializer_class =ApplicationListSerializer
    permission_classes= [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ApplicationPostSerializer
        return super().get_serializer_class()  

    def get_queryset(self):
        qs = Application.objects.filter(job_posting = self.kwargs.get('id'), candidate = self.request.user)
        return qs

    def get_job(self):
        job = get_object_or_404(JobPosting, id = self.kwargs.get('id'))
        return job

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.kwargs.get('id'):
            context['job_posting']=self.get_job()
        return context
    
    def perform_create(self, serializer):
        serializer.save(candidate = self.request.user, job_posting = self.get_job())

    def get_permissions(self):
        if self.request.method =="POST":
            permission_class = [IsCandidate]
        else:
            permission_class = [permissions.IsAuthenticated]

        return [permission() for permission in permission_class]

class ApplicationGet(generics.ListAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend,]
    filterset_class = StatusFilter
    
    def get_queryset(self):
        if self.request.user.profile.role == 'candidate':
            qs = Application.objects.filter(candidate= self.request.user)
            return qs

        elif self.request.user.profile.role == 'recruiter':
            qs = Application.objects.filter(job_posting__company=self.request.user.companys)            
            return qs


class ApplicationRetrieve(generics.RetrieveAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field='id'

    def get_queryset(self):
        if self.request.user.profile.role == 'candidate':
            qs = Application.objects.filter(candidate= self.request.user)
            return qs

        elif self.request.user.profile.role == 'recruiter':
            qs = Application.objects.filter(job_posting__company=self.request.user.companys)            
            return qs

        else:
            return Application.objects.none()

class ApplicationUpdate(generics.UpdateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationListSerializer
    permission_classes = [permissions.IsAuthenticated, (IsRecruiterOrOwner|IsCandidate)]
    lookup_field = 'id' 

    def get_queryset(self):
        if self.request.user.profile.role == 'candidate':
            qs = Application.objects.filter(candidate= self.request.user)
            return qs
    
        elif self.request.user.profile.role == 'recruiter':
            qs = Application.objects.filter(job_posting__company=self.request.user.companys)            
            return qs
    
        else:
            return Application.objects.none()


        

        
        


