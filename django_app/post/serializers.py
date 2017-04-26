from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'url', 'day', 'author', 'title', 'content', 'image', 'status', 'created_date')

        # id 정렬방법 : Descending
        ordering = (
            '-id',
        )
