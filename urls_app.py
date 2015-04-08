from django.conf.urls import patterns, include, url
from rest_framework import routers
from gallery_back import views


router =  routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'programs', views.ProgramViewSet)
urlpatterns = patterns('',
    url(r'^', include(router.urls)),
)
