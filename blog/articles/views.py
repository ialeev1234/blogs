from rest_framework import viewsets

from blog.articles.models import Articles
from blog.articles.serializers import ArticlesSerializer


class ArticlesViewSet(viewsets.ModelViewSet):
    queryset = Articles.objects.all()
    serializer_class = ArticlesSerializer
