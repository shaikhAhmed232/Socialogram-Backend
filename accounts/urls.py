from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.RegisterUser.as_view(), name="register"),
    path('login/', views.LoginView.as_view(), name="Login"),
    path('current-user/', views.GetCurrentUser.as_view(), name="current_user"),   
]
