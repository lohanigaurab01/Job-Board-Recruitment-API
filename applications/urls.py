from django.urls import path
from . import views

urlpatterns = [
    path('jobs/<id>/apply/', views.ApplicationCreate.as_view()),
    path('applications/', views.ApplicationGet.as_view()),
    path('applications/<int:id>', views.ApplicationRetrieve.as_view()),
    path('applications/<int:id>/update', views.ApplicationUpdate.as_view()),


]
