# TODO There's certainly more than one way to do this task, so take your pick.

from rest_framework import serializers
from .models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'timestamp', 'user']

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many = True, read_only = True)

    class Meta:
        model = Post
        fields = ['id', 'text', 'timestamp', 'user', 'comments']