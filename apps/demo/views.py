# TODO There's certainly more than one way to do this task, so take your pick.

from rest_framework import viewsets
from .models import Post
from .serializers import PostSerializer
from rest_framework.response import Response

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-timestamp')
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return response

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)