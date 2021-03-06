from django.db import models
from django.contrib.auth.models import User
from model_utils.models import TimeStampedModel
import collections

#from jsonfield import jsonfield
from jsonfield import JSONField

# Create your models here.


class Program(TimeStampedModel):
    name = models.CharField(max_length=255) 
    user = models.ForeignKey(User)

    def __unicode__(self):
        return "%s" %(self.name, )

class Presentation(TimeStampedModel):
    pid = models.CharField(max_length=255)
    durration = models.IntegerField(default=0)
    program = models.ForeignKey(Program, related_name='presentations')

    def __unicode__(self):
        return "%s   | %d ms" %(self.pid, self.durration)

    class Meta:
        order_with_respect_to = 'program'


