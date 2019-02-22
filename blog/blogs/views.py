from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from blog.articles.serializers import ArticlesSerializer
from blog.blogs.models import Blogs
from blog.blogs.serializers import BlogsSerializer


class BlogsViewSet(viewsets.ModelViewSet):
    queryset = Blogs.objects.all()
    serializer_class = BlogsSerializer

    @action(methods=['get'], detail=True)
    def articles(self, request, pk=None):
        blog = Blogs.objects.get(pk=pk)
        return Response(ArticlesSerializer(blog.articles, many=True).data)
