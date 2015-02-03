from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from . import serializers
from . import models


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

class ProgramViewSet(viewsets.ModelViewSet):
    queryset = models.Program.objects.all()
    serializer_class = serializers.ProgramSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SlideViewSet(viewsets.ModelViewSet):
    queryset = models.Slide.objects.all()
    serializer_class = serializers.SlideSerializer
