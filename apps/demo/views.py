# TODO There's certainly more than one way to do this task, so take your pick.

from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Prefetch
from .models import Post, Comment
from .serializers import PostSerializer

class PostInfiniteScrollView(generics.ListAPIView):

    """
        API endpoint for infinite scrolling list of posts

        Query Parameters:
        - last_timestamp (datetime, optional): 
        Timestamp of the last post loaded by the client
        If not provided, returns the most recent posts

        Returns:
        - List of posts older than the last_timestamp
        - Sorted by timestamp, latest first
        - Each post includes:
        * Post details (id, text, timestamp, author)
        * Up to 3 most recent comments
        * Total comment count
        - Includes a flag to indicate if more posts are available
   """
       
    serializer_class = PostSerializer
    
    def get_queryset(self):
        last_timestamp = self.request.query_params.get('last_timestamp')

        queryset = Post.objects.prefetch_related(
            Prefetch('comments', 
                     queryset=Comment.objects.order_by('-timestamp')[:3])
        )

        if last_timestamp:
            queryset = queryset.filter(timestamp__lt=last_timestamp)

        return queryset.order_by('-timestamp')
    

    def list(self, request, *args, **kwargs):
        
        page_size = int(request.query_params.get('page_size', 10))
        
        queryset = self.get_queryset()
        
        posts_batch = queryset[:page_size]
        
        serializer = self.get_serializer(posts_batch, many=True)
        
        response_data = {
            'posts': serializer.data,
            'has_more': queryset.count() > page_size
        }
        
        # If there are posts, include the timestamp of the last post for next request
        if posts_batch:
            response_data['last_timestamp'] = posts_batch.last().timestamp.isoformat()
        
        return Response(response_data)

