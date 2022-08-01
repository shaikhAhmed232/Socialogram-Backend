from django.urls import path
from .views import *

urlpatterns = [
    path("all-posts/", GetPostList.as_view(), name="post_list"),
    path("upload/", CreatePostView.as_view(), name="upload_post"),
    path("<int:pk>/delete-post/", DeletePost.as_view(), name="delete_post"),
    path("<int:pk>/", GetSinglePost.as_view(), name="get_single_post"),
    path("<str:username>/", UserPosts.as_view(), name='current_user_posts'),
    path('<int:pk>/add-comment/', AddComment.as_view(), name="add_comment"),
]