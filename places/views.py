# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from mongoengine.queryset.visitor import Q
from django.shortcuts import render
from rest_framework.decorators import detail_route, list_route
from django.contrib.auth.models import User
from rest_framework_mongoengine import viewsets
from rest_framework import renderers
from places.serializers import PlaceSerializer, UserSerializer, CategorySerializer, RatedPlaceSerializer
from places.models import Place, User,Category, RatedPlace, Tweet
from rest_framework.response import Response
from random import randint

############################
########PlaceViewSet########
############################
class PlaceViewSet(viewsets.ModelViewSet):

    lookup_field = 'id'
    serializer_class = PlaceSerializer
    
    def get_queryset(self):
        return Place.objects.all()

    ########Random places
    @list_route()
    def random(self, request, *args, **kwargs):
        count = Place.objects.count()
        random = randint(0, count-10 )
        places = Place.objects(Q(types__contains="restaurant") | Q(types__contains= "bar")| Q(types__contains= "food")|
                               Q(types__contains= "bakery") | Q(types__contains= "cafe")| Q(types__contains= "casino") |
                               Q(types__contains= "convenience_store") | Q(types__contains= "meal_delivery") |
                               Q(types__contains= "make_takeaway") | Q(types__contains= "nightclub") |
                               Q(types__contains= "shopping_mall")).limit(10).skip(random)
        serializer = PlaceSerializer(places, many=True)
        return Response(serializer.data)


############################
######RatedPlaceViewSet#####
############################
class RatedPlaceViewSet(viewsets.ModelViewSet):

    lookup_field = 'id'
    serializer_class = RatedPlaceSerializer

    def get_queryset(self):
        return RatedPlace.objects.all()

class CategoryViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()


############################
########UserViewSet#########
############################
class UserViewSet(viewsets.ModelViewSet):

    lookup_field = 'id'
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()

    @list_route()
    def credentials(self, request, *args, **kwargs):
        email = request.query_params['email']
        password = request.query_params['password']

        user = User.objects(Q(email=email) & Q(password=password))

        if(len(user) == 1):
            serializer = UserSerializer(user, many=True)

            return Response(serializer.data)
        else:
            return Response(False)




    ########User recommended places
    @detail_route()
    def places(self, request, *args, **kwargs):
        snippet = self.get_object()
        lat = request.query_params['lat']
        lng = request.query_params['lng']

        userId = kwargs.get("id")
        listPlaces = []

        user = User.objects(id=userId).get()
        userTypes = user.types
        if not userTypes:
            userTypes = ['594c36a033cbb6eed6f364e6','594c36b233cbb6eed6f364f2','594c368633cbb6eed6f364da','594c4a504362de3d8fae464f','5956fee67d2bf938c292e0bc']

        places =  Place.objects(Q(loc__near=[float(lat), float(lng)]))

        for type in userTypes:
            typeName = Category.objects(id=type).get().name


            for place in places:
                if typeName in place.types:

                    # Rating place according to twitter
                    twitterRating = len(Tweet.objects(text__contains= place.name))
                    place.twitter_rating = twitterRating

                    #Rating place according to user
                    userRating = RatedPlace.objects(Q(user_id__exact=userId) & Q(place_id__exact=place.id) )
                    print userId
                    print place.id
                    print userRating

                    if userRating:

                        rating = userRating.order_by('-id').first().rating
                    else:
                        rating = ''
                    place.user_rating = rating

                    #Adding places to list of recommended places
                    listPlaces.append(place)

                    # Sort the list according to twitter rated
                    listPlaces.sort(key=lambda x: x.twitter_rating, reverse=True)

                    # Sort the list according to user rated
                    listPlaces.sort(key=lambda x: x.user_rating, reverse=True)

        serializer = PlaceSerializer(listPlaces[:20], many=True)

        return Response(serializer.data)

    ########User choosen categories
    @detail_route()
    def categories(self, request, *args, **kwargs):

        snippet = self.get_object()
        userId = kwargs.get("id")
        user = User.objects(id=userId).get()
        userTypes = user.types
        listCategories = []

        for type in userTypes:
            type = Category.objects(id=type).get()
            listCategories.append(type)

        serializer = CategorySerializer(listCategories, many=True)
        
        return Response(serializer.data)



