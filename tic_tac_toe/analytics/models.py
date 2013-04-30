from django.db import models


class Event(models.Model):
    """
    The Event model is the only model with the Analytics app.  Developers
    can easily customize the type of analytic 'events' that are available by
    adding entries to the EVENT_TYPE_CHOICES tuple.

    """

    EVENT_TYPE_CHOICES = (
        ('TIC_TAC_TOE_START', 'User Started a Tic-Tac-Toe Game'),
        ('TIC_TAC_TOE_FINISH_LOST', 'User Finish a Tic-Tac-Toe Game with a Loss'),
        ('TIC_TAC_TOE_FINISH_DRAW', 'User Finish a Tic-Tac-Toe Game with a Loss'),
        ('USER_REGISTRATION_START', 'User Started Registration'),
        ('USER_REGISTRATION_FINISH', 'User Completed Registration'),
        ('USER_LOGIN_START', 'User Started Log In'),
        ('USER_LOGIN_FINISH', 'User Completed Log In')
    )

    event_type = models.CharField(max_length=100, choices=EVENT_TYPE_CHOICES)
    event_timestamp = models.DateTimeField(auto_now_add=True)
    event_model = models.CharField(max_length=100, default="None")
    event_model_id = models.IntegerField(default="0")
    event_url = models.CharField(max_length=100, default="None")

    def __unicode__(self):
        return u'%s, %s' % (self.event_type, self.event_timestamp)

    class Meta:
        ordering = ['event_timestamp']
