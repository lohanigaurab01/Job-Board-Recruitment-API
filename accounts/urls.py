from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('refresh/', views.MyRefreshView.as_view()),
    path('logout/', views.UserLogout.as_view()),

]
