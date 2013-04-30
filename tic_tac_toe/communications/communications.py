from django.core import mail
from django.template.loader import render_to_string


class _Communication(object):
    """
    Parent abstract class from which EmailCommunication and SMSCommunication
    are derived.

    The most important thing about this class is the constructor method
    that it provides to its descendants.  It provides the ability to
    leverage Django's template objects in communications.

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
        """
        Send an email message with plain text and html versions.

        It's important to note that while these method will send a
        plain-text version of the message, the html tags are not being
        stripped and so the message will be quite ugly.

        """
        message = mail.EmailMultiAlternatives(
            self.subject,
            self.message,
            self.sender,
            self.recipient_list)
        message.attach_alternative(self.message, "text/html")
        message.send()


class SMSCommunication(_Communication):
    """
    Provide functionality to send sms messages.

    """

    def send_message(self):
        """
        Needs implementation.

        """
        raise NotImplementedError
