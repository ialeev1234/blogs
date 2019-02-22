from rest_framework import viewsets

from blog.writers.models import Writers
from blog.writers.serializers import WritersSerializer


class WritersViewSet(viewsets.ModelViewSet):
    queryset = Writers.objects.all()
    serializer_class = WritersSerializer
