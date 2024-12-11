from django.urls import path
from .views import PostInfiniteScrollView

urlpatterns = [
    path('posts/', PostInfiniteScrollView.as_view(), name='post-infinite-scroll'),
]