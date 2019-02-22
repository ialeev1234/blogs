from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from django.views import static
from rest_framework import routers

from blog.blogs.views import BlogsViewSet
from blog.articles.views import ArticlesViewSet
from blog.writers.views import WritersViewSet

router = routers.DefaultRouter()
router.register(r'blogs', BlogsViewSet)
router.register(r'articles', ArticlesViewSet)
router.register(r'writers', WritersViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    url(r'^media/(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT, 'show_indexes': False})
]
