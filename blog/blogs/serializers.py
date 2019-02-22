from rest_framework import serializers
from rest_framework.fields import CharField

from blog.articles.models import Articles
from blog.articles.serializers import ArticlesSerializer
from blog.blogs.models import Blogs
from blog.writers.models import Writers


def required(value):
    if value is None:
        raise serializers.ValidationError('This field is required')


class BlogsSerializer(serializers.ModelSerializer):
    title = CharField(validators=[required])
    articles = ArticlesSerializer(many=True)

    def create(self, validated_data):
        articles_data = validated_data.pop('articles')
        blog = Blogs.objects.create(**validated_data)
        art_ids = []
        blog.articles.clear()
        for art in articles_data:
            writer = art.pop('writer')
            obj = Articles.objects.create(**art, writer=Writers.objects.create(**writer))
            blog.articles.add(obj)
            art_ids.append(obj.id)
        blog.save()
        return blog

    class Meta:
        model = Blogs
        fields = ('id', 'title', 'articles')
