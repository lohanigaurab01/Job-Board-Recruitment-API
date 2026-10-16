from django.urls import path
from . import views

urlpatterns = [
    path('company/', views.CompanyCreate.as_view()),
    path('company/<int:id>/', views.CompanyRetrieveUpdate.as_view()),
    
]
