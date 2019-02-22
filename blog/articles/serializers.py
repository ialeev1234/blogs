from rest_framework import serializers
from rest_framework.fields import CharField, DateField

from blog.articles.models import Articles
from blog.writers.models import Writers
from blog.writers.serializers import WritersSerializer


def required(value):
    if value is None:
        raise serializers.ValidationError('This field is required')


class ArticlesSerializer(serializers.ModelSerializer):
    title = CharField(validators=[required])
    excerpt = CharField(validators=[required])
    text = CharField(validators=[required])
    date_created = DateField(validators=[required])
    date_updated = DateField(validators=[required])
    writer = WritersSerializer(validators=[required])

    def create(self, validated_data):
        writer_data = validated_data.pop('writer')
        article = Articles.objects.create(**validated_data, writer=Writers.objects.create(**writer_data))
        return article

    class Meta:
        model = Articles
        fields = ('id', 'title', 'excerpt', 'text', 'date_created', 'date_updated', 'writer')
