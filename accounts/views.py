from django.shortcuts import render
from django.contrib.auth import get_user_model, authenticate

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from accounts.models import User, Contact
from .serializer import UserSerializer, ChangeUserPasswordSerializer, ContactSerializer
from .utils import get_token, convert_to_seconds

# Create your views here.

class RegisterUser(APIView):
    def post(self, request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                # generate token.
                tokens = get_token(user)
                # access_time_limit = convert_to_seconds(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"])
                # refresh_time_limit = convert_to_seconds(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'])

                return Response(data={
                    "access": tokens["access"],
                    "refresh": tokens["refresh"],
                }, status=status.HTTP_200_OK)

            else:
                return Response(data={"status": "error", "message": "Your account has been block for security reasons"}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response(data={
                "status": "error",
                "message": "Invalid username or password",
            }, status=status.HTTP_400_BAD_REQUEST)

# view for getting current login user.
class GetCurrentUser(APIView):
    permission_classes = [IsAuthenticated]

    # getting current user
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(data = serializer.data , status=status.HTTP_200_OK)

    # changing fields value of current user.
    def put(self, request):
        user = request.user
        data = request.data
        serializer = UserSerializer(instance=user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# view for Changing profile picture of current user.
class UpdateProfilePic(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request):
        user = request.user
        data = request.data
        serializer = UserSerializer(instance=user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangeUserPassword(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data
        serializer = ChangeUserPasswordSerializer(instance=user, data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'success': "password change successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request):
        user = request.user
        user_list = User.objects.all().exclude(username=user.username)
        serializer = UserSerializer(user_list, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

# view for getting any user's details.
class UserProfileDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'

    # def get_queryset(self, username):
    #     try:
    #         return User.objects.get(username=username)
    #     except NotFoundErr:
    #         return Response(status=status.HTTP_404_NOT_FOUND)

    # def get(self, request, username):
    #     user = self.get_queryset(username)
    #     followers = user.followers.all()
    #     following = user.following.all()
    #     print(followers, following)
    #     serializer = self.serializer_class(user)
    #     followers_serializer = FollowingSerializer(followers, many=True)
    #     following_serializer = FollowerSerializer(following, many=True)
        
    #     return Response({
    #         "user": serializer.data,
    #         "followers": followers_serializer.data,
    #         "following": following_serializer.data,
    #     }, status=status.HTTP_200_OK)

# view for getting followers list in form of user object. 
class GetUserFollower(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        user = User.objects.get(username=username)
        followers = user.followers.all()
        follower_user = []
        for follower in followers:
            follower_user.append(follower.user_id)
        serializer = UserSerializer(follower_user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# view for getting following list in form of user object.
class GetUserFollowing(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        user = User.objects.get(username=username)
        following = user.following.all()
        following_user = []
        for each in following:
            following_user.append(each.following_user_id)
        serializer = UserSerializer(following_user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# view for follow and unfollow requests.
class FollowView(APIView):
    permission_classes = [IsAuthenticated]

    # create contact instance (follow request).
    def post(self, request):
        # user who makes follow request.
        follower = request.user
        # user id who is being followed.
        following_id = request.data["following"]
        # getting followed user from db.
        following_user = User.objects.get(id=following_id["id"])

        # check for if following_user is active or not?
        if not following_user.is_active:
            return Response({"msg": f"{following_user} is blocked you can't follow this user."}, status=status.HTTP_400_BAD_REQUEST)
        # check for if following_user already getting followed by follower?
        if follower.following.filter(following_user_id=following_user.id).exists():
            return Response({"msg": "You already following {0}".format(following_user)},status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = ContactSerializer(data={"user_id": follower.id, "following_user_id": following_user.id})
            if serializer.is_valid():
                serializer.save()
                return Response({"msg": "{0} start following {1}".format(follower, following_user)}, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete Contact instance (unfollow).
    def delete(self, request):
        # user who is making unfollow request.
        un_follower = request.user
        # user id who is getting unfollowed by un_follower.
        un_following = request.data["un_following"]
        # getting un_following user from db.
        un_following_user = User.objects.get(id = un_following["id"])

        # checking for contact in which un_follower following un_following_user exists or not?
        try:
            contact = Contact.objects.get(user_id=un_follower.id, following_user_id=un_following_user.id)
        except Contact.DoesNotExist:
            return Response({"msg": f"you don't follow {un_following_user} so you can't unfollow this user."}, status=status.HTTP_404_NOT_FOUND)
        contact.delete()
        return Response({"msg": f"{un_follower} unfollowed {un_following_user}"}, status=status.HTTP_200_OK)



        
        

            
        
        
















