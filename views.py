from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from . import serializers
from . import models


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

class PresentationViewSet(viewsets.ModelViewSet):
    queryset = models.Presentation.objects.all()
    serializer_class = serializers.PresentationSerializer

class SlideViewSet(viewsets.ModelViewSet):
    queryset = models.Slide.objects.all()
    serializer_class = serializers.SlideSerializer
