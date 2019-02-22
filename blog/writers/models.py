from django.db import models
from django.utils.translation import ugettext_lazy as _


class Writers(models.Model):
    name = models.CharField(_('Name'), max_length=30, blank=True)
    age = models.IntegerField(_('Age'), null=True, blank=True)
    email = models.CharField(_('Email'), max_length=50, blank=True)
    address = models.CharField(_('Address'), max_length=255, blank=True)

    objects = models.Manager()
