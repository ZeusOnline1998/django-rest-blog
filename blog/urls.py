from django.urls import path
from . import views

# app_name = 'blog'

urlpatterns = [
    # path('', views.index),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('blog/create/', views.create_post, name='create-post'),
    # path('blog/create/', views.create_post.as_view(), name='create-post'),
    path('blog/', views.post_list, name='post-list'),
    path('blog/<int:post_id>/', views.post_detail, name='post-detail'),
    path('blog/comments/create/', views.create_comment, name='create-comment'),
    path('blog/<int:post_id>/comments/', views.comment_list, name='comment-list'),
    path('blog/comments/<int:comment_id>/', views.comment_detail, name='comment-detail'),
]
