from django.db import models
from django.db.models import CASCADE
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from blog import settings
from blog.writers.models import Writers


class Articles(models.Model):
    writer = models.ForeignKey(Writers, on_delete=CASCADE, null=True)
    image = models.ImageField(upload_to='articles/', null=True, blank=True)
    title = models.CharField(_('Title'), max_length=255, blank=True)
    excerpt = models.TextField(_('Excerpt'), null=True, blank=True)
    text = models.TextField(_('Text'), null=True, blank=True)
    date_created = models.DateField(_('Date created'), null=True, blank=True)
    date_updated = models.DateField(_('Date updated'), null=True, blank=True)

    objects = models.Manager()

    def image_tag(self):
        return mark_safe(f'<img src="{settings.MEDIA_URL}{self.image}" height=100 />')

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True
