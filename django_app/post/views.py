import django_filters
from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions

from post.models import Post
from .serializers import PostSerializer

User = get_user_model()


class PostFilter(django_filters.rest_framework.FilterSet):
    year = django_filters.NumberFilter(name='day', lookup_expr='year')
    month = django_filters.NumberFilter(name='day', lookup_expr='month')

    class Meta:
        model = Post
        fields = ('year', 'month',)


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = PostFilter
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)
