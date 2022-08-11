from urllib.request import parse_keqv_list
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.parsers import MultiPartParser

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from .permissions import IsPostOwner
from accounts.serializer import UserSerializer

User = get_user_model()
# Create your views here.
class GetPostList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args):
        user = request.user
        # getting user followers and following list
        followers = user.followers.all()
        following = user.following.all()
        # getting user object list form following and followers list since.
        followers = [follower.user_id for follower in followers]
        following = [following.following_user_id for following in following]
        # copying all into one list of user objects
        users = [*followers, *following]
        all_posts = Post.objects.all().select_related('owner').prefetch_related('comments', 'comments__comment_by', "likes")
        # filtering post by post owner since wanted show post of users who have follower or following relation with current login user.
        filtered_posts = filter(lambda post: post if post.owner in users else None, all_posts)
        serializer = PostSerializer(filtered_posts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class CreatePostView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request, *args):
        user = request.user
        data = request.data
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save(owner=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetSinglePost(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    
    def get(self, request, pk):
        post = Post.objects.select_related('owner').prefetch_related('comments', 'comments__comment_by', 'likes').get(pk=pk)
        post_serializer = PostSerializer(post)
        return Response(data=post_serializer.data, status=status.HTTP_200_OK)

class DeletePost(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsPostOwner]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

class UserPosts(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username, *args):
        user = User.objects.get(username=username)
        user_posts = Post.current_user_posts.get_current_user_posts(user=user).prefetch_related('comments', 'comments__comment_by', "likes")
        serializer = PostSerializer(user_posts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class AddComment(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['post',]
    def post(self, request, pk):
        user = request.user
        post = Post.objects.get(pk=pk)
        data = request.data
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save(post=post, comment_by=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddLike(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        post = Post.objects.get(pk=pk)
        if not post.likes.filter(liked_by=user).exists():
            new_like = Like(post=post, liked_by=user)
            new_like.save()
            serializer = LikeSerializer(new_like)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        like = post.likes.get(liked_by=user)
        like.delete()
        return Response({"message": "unliked post successfully"}, status=status.HTTP_200_OK)






