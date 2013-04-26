from django.core import mail
from django.template.loader import render_to_string


class _Communication(object):
    """
    Parent class from which EmailCommunication and SMSCommunication are
    derived.

    Provides a common constructor for descendants a the send_message
    method stub.

    """

    def __init__(self, sender_email, recipients_email_list, subject,
                 template_name, context):
        self.sender = sender_email
        self.recipient_list = recipients_email_list
        self.subject = subject
        self.template_name = template_name
        self.context = context
        self.message = render_to_string(template_name, context)

    def send_message(self):
        """
        Provide a stub to be implemented by class descendants.

        """
        raise NotImplementedError


class EmailCommunication(_Communication):
    """
    Provide functionality to send text & html email messages.

    This class ultimately derives it power from the Django mail module.
    For it to work correctly, all related settings must have appropriate
    values.  More info: https://docs.djangoproject.com/en/1.5/topics/email

    """
    def send_message(self):
        message = mail.EmailMultiAlternatives(
            self.subject,
            self.message,
            self.sender,
            self.recipient_list)
        message.attach_alternative(self.message, "text/html")
        message.send()
