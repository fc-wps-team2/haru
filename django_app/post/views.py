from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions

from post.models import Post
from .serializers import PostSerializer

User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)
