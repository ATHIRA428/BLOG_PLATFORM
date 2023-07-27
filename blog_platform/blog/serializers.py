from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import BlogPost, Comment

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')

class UserviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name']

class CommentSerializer(serializers.ModelSerializer):
    user_first_name = serializers.ReadOnlyField(source='user.first_name')

    class Meta:
        model = Comment
        fields = ('id', 'user', 'user_first_name', 'blog_post', 'content', 'created_time', 'updated_time')
        read_only_fields = ('user', 'user_first_name', 'created_time', 'updated_time')


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content', 'user']

class BlogPostSerializer(serializers.ModelSerializer):
    comments = CommentsSerializer(many=True, read_only=True)
    user = UserviewSerializer(read_only=True)  

    class Meta:
        model = BlogPost
        fields = ('id', 'title', 'content', 'image', 'created_time', 'updated_time', 'comments', 'user')
    
    def validate_image(self, value):
        return value


class AdminUserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_staff=True,
            is_superuser=True, 
        )
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
