from tastypie.resources import ModelResource

from .models import Event


class EventResource(ModelResource):
    """
    EventResource is an object used by Tastypie to make the Event model
    available via RESTful API.
    """

    class Meta:
        """
        The Meta class contains configuration settings used by Tastypie in
        determining how the API for the event model is constructed and what
        data it offers.
        """
        queryset = Event.objects.all()
        resource_name = 'event'
        filtering = {
            "event_type": ('exact',),
            "event_timestamp": ('exact', 'month', 'lte', 'gte'),
        }