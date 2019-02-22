from django.contrib.gis import admin

from blog.writers.models import Writers


@admin.register(Writers)
class WritersAdmin(admin.ModelAdmin):
    pass
