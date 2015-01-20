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
        read_only_fields=('presentation', '_order')


class PresentationSerializer(serializers.HyperlinkedModelSerializer):
    slides = SlideSerializer2(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    #slides = serializers.StringRelatedField(many=True)

    class Meta:
        model = models.Presentation
        fields = ('name', 'user', 'slides')

    def create(self, validated_data):
        print validated_data
        slides_data = validated_data.pop('slides', [])
        print slides_data
        presentation = models.Presentation.objects.create(**validated_data)
        slides = [ models.Slide(**sd) for sd in slides_data ] 
        for order, slide in enumerate(slides):
            slide.presentation = presentation
            slide._order=order
        if slides:
            models.Slide.objects.bulk_create( slides )
        return presentation

