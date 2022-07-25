from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.parsers import MultiPartParser

from .models import Post
from .serializers import PostSerializer

User = get_user_model()
# Create your views here.
class GetPostList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args):
        user = request.user
        followers = user.followers.all()
        following = user.following.all()
        followers = [follower.user_id for follower in followers]
        following = [following.following_user_id for following in following]
        users = [*followers, *following]
        all_posts = Post.objects.all()
        filtered_posts = filter(lambda post: post if post.owner in users else None, all_posts)
        serializer = PostSerializer([*filtered_posts], many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class CreatePostView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request, *args):
        user = request.user
        data = request.data
        serializer = PostSerializer(data=data, context={"user": user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetSinglePost(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

class DeletePost(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

class UserPosts(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username, *args):
        user = User.objects.get(username=username)
        user_posts = Post.current_user_posts.get_current_user_posts(user=user)
        serializer = PostSerializer(user_posts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK) 



