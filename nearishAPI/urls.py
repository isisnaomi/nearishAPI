
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


router = routers.DefaultRouter()

############################
#######Nearish routes#######
############################
router.register(r'places', views.PlaceViewSet, 'Places'),
router.register(r'ratedplaces', views.RatedPlaceViewSet, 'RatedPlaces'),
router.register(r'users', views.UserViewSet, 'Users'),
router.register(r'users/(?P<username>\w{0,50})/places', snippet_user_places, 'snippet-user'),
router.register(r'categories', views.CategoryViewSet, 'Category'),

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
