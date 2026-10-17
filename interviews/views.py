from django.shortcuts import render, get_object_or_404
from rest_framework import generics,permissions
from .models import Interview
from applications.models import Application
from .serializers import InterviewScheduleSerializer,InterviewUpdateSerializer
from .permissions import IsRecuriter,IsRecuriterOrOwner

# Create your views here.
class InterviewSchedule(generics.ListCreateAPIView):
    queryset = Interview.objects.all()
    serializer_class = InterviewScheduleSerializer

    def get_queryset(self):
        return super().get_queryset()

    def get_application(self):
        app_id = self.kwargs.get('application_id')
        return get_object_or_404(Application, id = app_id, job_posting__company= self.request.user.companys)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.kwargs.get('application_id'):
            context['application']= self.get_application()
        return context

    def perform_create(self, serializer):
        app = self.get_application()
        serializer.save(application = app, interviewer= self.request.user)

    def get_permissions(self):
        if self.request.method =="POST":
            permission_class = [IsRecuriter]

        else:
            permission_class = [permissions.IsAuthenticated]
        return [permission() for permission in permission_class]


class InterviewScheduleUpdate(generics.UpdateAPIView):
    queryset = Interview.objects.all()
    serializer_class = InterviewUpdateSerializer
    permission_classes = [IsRecuriterOrOwner]
    lookup_field = 'id'
    lookup_url_kwarg= 'interview_id'
        
        


    
