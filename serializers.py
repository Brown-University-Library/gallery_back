from django.contrib.auth.models import User, Group
from . import models
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class SlideSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Slide

class SlideSerializer2(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Slide
        fields=('pid', 'durration')
        read_only_fields=('program', '_order')


class ProgramSerializer(serializers.HyperlinkedModelSerializer):
    slides = SlideSerializer2(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Program
        fields = ('id','name', 'user', 'slides')

    def create(self, validated_data):
        slides_data = validated_data.pop('slides', [])
        program = models.Program.objects.create(**validated_data)
        slides = [ models.Slide(**sd) for sd in slides_data ] 
        for order, slide in enumerate(slides):
            slide.program = program
            slide._order=order
        if slides:
            models.Slide.objects.bulk_create( slides )
        return program
