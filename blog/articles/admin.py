from django.contrib import admin

from blog.articles.models import Articles


@admin.register(Articles)
class ArticlesAdmin(admin.ModelAdmin):

    fields = ('id', 'title', 'excerpt', 'text', 'date_created', 'date_updated', 'writer__name', 'image_tag')
