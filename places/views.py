# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from mongoengine.queryset.visitor import Q
from django.shortcuts import render
from rest_framework.decorators import detail_route, list_route
from django.contrib.auth.models import User
from rest_framework_mongoengine import viewsets
from rest_framework import renderers
from places.serializers import PlaceSerializer, UserSerializer, CategorySerializer, RatedPlaceSerializer
from places.models import Place, User,Category, RatedPlace
from rest_framework.response import Response


class PlaceViewSet(viewsets.ModelViewSet):

    lookup_field = 'id'
    serializer_class = PlaceSerializer
    
    def get_queryset(self):
        return Place.objects.all()

    @list_route()
    def random(self, request, *args, **kwargs):
        count = Place.objects.count()
        places =Place.objects.all()
        return Response(count)


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


class UserViewSet(viewsets.ModelViewSet):

    lookup_field = 'id'
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()

    #User recommended places
    @detail_route()
    def places(self, request, *args, **kwargs):
        snippet = self.get_object()
        lat = request.query_params['lat']
        lng = request.query_params['lng']

        userId = kwargs.get("id")
        listPlaces = []
        secondListPlaces = listPlaces[:]

        user = User.objects(id=userId).get()
        userTypes = user.types


        places =  Place.objects(Q(loc__near=[float(lat), float(lng)]))

        for type in userTypes:
            typeName = Category.objects(id=type).get().name

            for place in places:
                if typeName in place.types:

                    #Rating place according to user
                    userRating = RatedPlace.objects(Q(user_id=userId) & Q(place_id=place.id) )
                    if userRating:
                        rating = userRating.get().rating
                    else:
                        rating = ''
                    place.user_rated = rating
                    secondListPlaces.append(place)

        serializer = PlaceSerializer(secondListPlaces, many=True)

        return Response(serializer.data)

    #User choosen categories
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



