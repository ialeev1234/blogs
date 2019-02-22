from django.db import models
from django.utils.translation import ugettext_lazy as _

from blog.articles.models import Articles


class Blogs(models.Model):
    articles = models.ManyToManyField(Articles, blank=True)
    title = models.CharField(_('Title'), max_length=255, blank=True)

    objects = models.Manager()
