from django.contrib.auth.models import User
from places.models import Place, User
from rest_framework import serializers

from rest_framework_mongoengine import serializers

#class UserSerializer(serializers.HyperlinkedModelSerializer):
#class Meta:
#     model = User
#        fields = ('url', 'username', 'email')


class PlaceSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Place
        fields = '__all__'

class UserSerializer(serializers.DocumentSerializer):
    class Meta:
        model = User
        fields = '__all__'