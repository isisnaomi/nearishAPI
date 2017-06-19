# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework.decorators import detail_route, list_route
from django.contrib.auth.models import User
from rest_framework_mongoengine import viewsets
from rest_framework import renderers
from places.serializers import PlaceSerializer, UserSerializer
from places.models import Place, User
from rest_framework.response import Response


#class UserViewSet(viewsets.ModelViewSet):
#   """
#   API endpoint that allows users to be viewed or edited.
#   """
#   queryset = User.objects.all().order_by('-date_joined')
#   serializer_class = UserSerializer



class PlaceViewSet(viewsets.ModelViewSet):
    '''
        Contains information about inputs/outputs of a single program
        that may be used in Universe workflows.
        '''
    lookup_field = 'id'
    serializer_class = PlaceSerializer
    
    def get_queryset(self):
        return Place.objects.all()



class UserViewSet(viewsets.ModelViewSet):
    '''
        Contains information about inputs/outputs of a single program
        that may be used in Universe workflows.
        '''
    lookup_field = 'id'
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()


    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def places(self, request, *args, **kwargs):
        snippet = self.get_object()
        places = Place.objects(types__contains='bar')
        serializer = PlaceSerializer(places, many=True)


        return Response(serializer.data)



