from django.conf.urls import patterns, include, url
from rest_framework import routers
from gallery_back import views


router =  routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'presentations', views.PresentationViewSet)
router.register(r'slides', views.SlideViewSet)
urlpatterns = patterns('',
    url(r'^', include(router.urls)),
)
