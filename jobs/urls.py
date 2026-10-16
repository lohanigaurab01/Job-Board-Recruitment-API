from django.urls import path
from . import views

urlpatterns = [
    path('jobs', views.JobPostingView.as_view()),
    path('jobs/<int:id>', views.JobRetrieveView.as_view()),

]
