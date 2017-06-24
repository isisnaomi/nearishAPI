"""nearishAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from django.conf.urls import url, include
from rest_framework import routers
from places import views
from rest_framework import renderers
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import verify_jwt_token

snippet_user_places = views.UserViewSet.as_view({
    'get': 'places'
}, renderer_classes=[renderers.StaticHTMLRenderer])

snippet_random_places = views.PlaceViewSet.as_view({
    'get': 'random'
}, renderer_classes=[renderers.StaticHTMLRenderer])

router = routers.DefaultRouter()
#router.register(r'users', views.UserViewSet)
router.register(r'randomplaces', snippet_random_places, 'snippet-random'),

router.register(r'places', views.PlaceViewSet, 'Places'),
router.register(r'ratedplaces', views.RatedPlaceViewSet, 'RatedPlaces'),
router.register(r'users', views.UserViewSet, 'Users'),
router.register(r'users/(?P<username>\w{0,50})/places', snippet_user_places, 'snippet-user'),
router.register(r'categories', views.CategoryViewSet, 'Category'),


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
