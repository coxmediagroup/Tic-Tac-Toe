from tastypie.resources import ModelResource

from .models import Event


class EventResource(ModelResource):

    class Meta:
        queryset = Event.objects.all()
        resource_name = 'event'
        filtering = {
            "event_type": ('exact',),
            "event_timestamp": ('exact', 'month', 'lte', 'gte'),
        }