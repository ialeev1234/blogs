from rest_framework import serializers
from rest_framework.fields import CharField, IntegerField

from blog.writers.models import Writers


def required(value):
    if value is None:
        raise serializers.ValidationError('This field is required')


class WritersSerializer(serializers.ModelSerializer):
    name = CharField(validators=[required])
    age = IntegerField(validators=[required])
    email = CharField(validators=[required])
    address = CharField(validators=[required])

    class Meta:
        model = Writers
        fields = ('id', 'name', 'age', 'email', 'address')
