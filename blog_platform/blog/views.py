from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status  
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer,BlogPostSerializer,CommentSerializer,AdminUserRegistrationSerializer
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import generics,exceptions
from .models import BlogPost,Comment
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAdminUser
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView

User = get_user_model()

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            subject = 'Welcome to  Blogging Platform'
            message = f"Dear {user.username},\n\nThank you for registering on our Blogging Platform. We are excited to have you on board!"
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = user.email
            send_mail(subject, message, from_email, [to_email])

            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
from rest_framework_simplejwt.views import TokenObtainPairView

class UserLogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)

class BlogPostListCreateView(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BlogPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        blog_post = self.get_object()
        comments = Comment.objects.filter(blog_post=blog_post)
        comment_serializer = CommentSerializer(comments, many=True)
        response.data['comments'] = comment_serializer.data

        return response

class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to update this comment.")
        serializer.save()
    
    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this comment.")
        instance.delete()

class AdminUserRegistrationView(CreateAPIView):
    serializer_class = AdminUserRegistrationSerializer
    permission_classes = [IsAdminUser] 

    def perform_create(self, serializer):
        serializer.save()

class BlogPostAdminListView(generics.ListAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAdminUser]

class BlogPostAdminDetailView(generics.RetrieveDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsAdminUser]

class CommentAdminListView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAdminUser]

class CommentAdminDetailView(generics.RetrieveDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAdminUser]

    def perform_destroy(self, instance):
        if not self.request.user.is_staff:
            raise exceptions.PermissionDenied("You do not have permission to delete this comment.")
        instance.delete()
