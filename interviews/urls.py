from django.urls import path
from . import views

urlpatterns = [
    path('applications/<int:application_id>/interviews/', views.InterviewSchedule.as_view()),
    path('interviews/<int:interview_id>/', views.InterviewScheduleUpdate.as_view()),

]
