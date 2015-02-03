from django.contrib.auth.models import User, Group
from . import models
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class SlideSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Slide
        fields=('pid', 'durration')
        read_only_fields=('program', '_order')

class SlideSerializer2(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Slide
        fields=('pid', 'durration')
        read_only_fields=('program', '_order')


class ProgramSerializer(serializers.HyperlinkedModelSerializer):
    slides = SlideSerializer2(many=True)
    #user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    owner = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = models.Program
        fields = ('id','name', 'owner', 'slides')

    def create(self, validated_data):
        slides_data = validated_data.pop('slides', [])
        program = models.Program(**validated_data)
        program.save()
        slides = [ models.Slide(**sd) for sd in slides_data ] 
        for order, slide in enumerate(slides):
            slide.program = program
            slide._order=order
        if slides:
            models.Slide.objects.bulk_create( slides )
        return program

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        slides_data = validated_data.pop('slides', [])
        current_slides = instance.slides.all()
        paired_slides = zip(current_slides, slides_data)
        orphaned_slides = current_slides[len(slides_data):]
        new_slide_data = slides_data[current_slides.count():]

        for orphan in orphaned_slides:
            orphan.delete()

        slide_serializer = SlideSerializer2()
        for current, sd in paired_slides:
            slide_serializer.update(current, sd).save()
        
        pair_total = instance.slides.count()
        new_slides = [ models.Slide(**sd) for sd in new_slide_data]
        for order, slide in enumerate(new_slides):
            slide.program = instance
            slide._order= pair_total + order
        
        if new_slides:
            models.Slide.objects.bulk_create( new_slides )
        return instance



    

        slides = [ models.Slide(**sd) for sd in slides_data ] 
        for order, slide in enumerate(slides):
            slide._order=order
        if slides:
            instance.slides.clear()
            instance.slides = slides
        return instance
