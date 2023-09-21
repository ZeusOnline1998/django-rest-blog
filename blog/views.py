from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Post, Comment
from .serializers import PostListSerializer, PostSerializer, PostCreateSerializer, PostUpdateSerializer, CommentSerializer, CommentCreateSerializer, CommentUpdateSerializer, UserRegistrationSerializer, UserLoginSerializer
from django.http import HttpRequest
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.pagination import PageNumberPagination

# Create your views here.
class CustomPagination(PageNumberPagination):
    page_size = 5  # Number of items per page
    page_query_param = 'page'  # Query parameter for page number
    page_size_query_param = 'page_size'  # Query parameter for page size
    max_page_size = 100  # Maximum page size


@api_view(['POST'])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def user_login(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data
        login(request._request, user)  # type: ignore
        return Response({"message": "Login successful", "user_id": user.id}, status=status.HTTP_200_OK)  # type: ignore
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def user_logout(request):
    logout(request)
    return Response({'msg': "Logged out"})

@api_view(['GET'])
def post_list(request):
    posts = Post.objects.all()
    pagination = CustomPagination()
    paginated_queryset = pagination.paginate_queryset(posts, request)
    # serializer = PostListSerializer(posts, many=True)
    serializer = PostListSerializer(paginated_queryset, many=True)
    # return Response(serializer.data)
    return pagination.get_paginated_response(serializer.data)

@api_view(['POST'])
# @csrf_exempt
def create_post(request):
    serializer = PostCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# class create_post(ListCreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostCreateSerializer

#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)

@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PostUpdateSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        post.delete()
        return Response(status=204)

@api_view(['GET'])
def comment_list(request, post_id):
    comments = Comment.objects.filter(post=post_id)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_comment(request):
    serializer = CommentCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()  # Set the author to the current user
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def comment_detail(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CommentUpdateSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=204)
