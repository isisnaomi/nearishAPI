from django.contrib.auth.models import User
from places.models import Place, User,Category,RatedPlace
from rest_framework import serializers

from rest_framework_mongoengine import serializers

class PlaceSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Place
        fields = '__all__'


class UserSerializer(serializers.DocumentSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CategorySerializer(serializers.DocumentSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class RatedPlaceSerializer(serializers.DocumentSerializer):
    class Meta:
        model = RatedPlace
        fields = '__all__'