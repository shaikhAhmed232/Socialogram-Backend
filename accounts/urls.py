from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.RegisterUser.as_view(), name="register"),
    path('login/', views.LoginView.as_view(), name="Login"),
    path('current-user/', views.GetCurrentUser.as_view(), name="current_user"),
    path('update-pic/', views.UpdateProfilePic.as_view(), name="update_profile_pic"),
    path('users/', views.UserListView.as_view(), name="user_list"),
    path('follow-req/', views.FollowView.as_view(), name="follow_view"),
    path('change-password/', views.ChangeUserPassword.as_view(), name="change_user_password"),
    path('<str:username>/', views.UserProfileDetailView.as_view(), name="user_profile_view"),
    path('<str:username>/followers/', views.GetUserFollower.as_view(), name="user_follower_view"),
    path('<str:username>/following/', views.GetUserFollowing.as_view(), name="user_following_view"),
]
