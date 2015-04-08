from django.contrib.auth.models import User, Group
from . import models
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class PresentationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Presentation
        fields=('pid', 'durration')
        read_only_fields=('program', '_order')

class PresentationSerializer2(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Presentation
        fields=('pid', 'durration')
        read_only_fields=('program', '_order')


class ProgramSerializer(serializers.HyperlinkedModelSerializer):
    presentations = PresentationSerializer2(many=True)
    #user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    owner = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = models.Program
        fields = ('id','name', 'owner', 'presentations')

    def create(self, validated_data):
        presentations_data = validated_data.pop('presentations', [])
        program = models.Program(**validated_data)
        program.save()
        presentations = [ models.Presentation(**sd) for sd in presentations_data ] 
        for order, presentation in enumerate(presentations):
            presentation.program = program
            presentation._order=order
        if presentations:
            models.Presentation.objects.bulk_create( presentations )
        return program

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        presentations_data = validated_data.pop('presentations', [])
        current_presentations = instance.presentations.all()
        paired_presentations = zip(current_presentations, presentations_data)
        orphaned_presentations = current_presentations[len(presentations_data):]
        new_presentation_data = presentations_data[current_presentations.count():]

        for orphan in orphaned_presentations:
            orphan.delete()

        presentation_serializer = PresentationSerializer2()
        for current, sd in paired_presentations:
            presentation_serializer.update(current, sd).save()
        
        pair_total = instance.presentations.count()
        new_presentations = [ models.Presentation(**sd) for sd in new_presentation_data]
        for order, presentation in enumerate(new_presentations):
            presentation.program = instance
            presentation._order= pair_total + order
        
        if new_presentations:
            models.Presentation.objects.bulk_create( new_presentations )
        return instance



    

        presentations = [ models.Presentation(**sd) for sd in presentations_data ] 
        for order, presentation in enumerate(presentations):
            presentation._order=order
        if presentations:
            instance.presentations.clear()
            instance.presentations = presentations
        return instance
