from django.contrib.auth.models import User
from django.db import models
from django.forms.widgets import Input


class ColorWidget(Input):
    input_type = 'color'
    template_name = 'events/color.html'


class ColorField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 10
        super(ColorField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = ColorWidget
        return super(ColorField, self).formfield(**kwargs)


# Create your models here.
from samples.models import SampleTbl


class EventTypeTbl(models.Model):
    name = models.CharField(max_length=40)
    color = ColorField(default='#ff4312')
    index = models.IntegerField(default=0)


class EventsTbl(models.Model):
    message = models.CharField(max_length=140, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    event_at = models.DateTimeField(null=True)
    event_type = models.ForeignKey(EventTypeTbl, models.DO_NOTHING,
                                   db_column='event_typeID')
    user = models.ForeignKey(User, models.DO_NOTHING,
                             db_column='userID')
    sample = models.ForeignKey(SampleTbl, models.DO_NOTHING, db_column='sampleID')
