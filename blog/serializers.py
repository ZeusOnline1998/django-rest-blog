from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Post, Comment, User

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'

class PostListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    # comments = CommentSerializer(many=True, read_only=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        # fields = ['id', 'title', 'content', 'comments', 'created_at', 'updated_at', 'author']
        fields = '__all__'

    def get_comments(self, obj):
        comments = Comment.objects.filter(post=obj)
        # request = self.context.get('request')
        return CommentSerializer(comments, many=True).data

class PostCreateSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.id')

    class Meta:
        model = Post
        fields = '__all__'

class CommentCreateSerializer(serializers.ModelSerializer):
    author = User
    post = Post

    class Meta:
        model = Comment
        fields = '__all__'

# Update operation
class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect credentials")
