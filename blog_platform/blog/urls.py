from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserLogoutView,
    BlogPostListCreateView,
    BlogPostDetailView,
    CommentListCreateView,
    AdminUserRegistrationView,
    CommentDetailView,
    BlogPostAdminListView,
    BlogPostAdminDetailView,
    CommentAdminListView,
    CommentAdminDetailView,
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('logout/', UserLogoutView.as_view()),
    path('blogposts/', BlogPostListCreateView.as_view()),
    path('blogposts/<int:pk>/', BlogPostDetailView.as_view()),
    path('comments/', CommentListCreateView.as_view()),
    path('comments/<int:pk>/', CommentDetailView.as_view()),
    path('blogposts/admin/', BlogPostAdminListView.as_view()),
    path('blogposts/<int:pk>/admin/', BlogPostAdminDetailView.as_view()),
    path('register/admin/', AdminUserRegistrationView.as_view(), name='admin-register'),
    path('comments/admin/', CommentAdminListView.as_view()),
    path('comments/<int:pk>/admin/', CommentAdminDetailView.as_view()),
]
