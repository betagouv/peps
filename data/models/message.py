import os
from django.db import models
from data.models import Farmer
from django.utils import timezone
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

class Message(models.Model):

    class Meta:
        indexes = [
            models.Index(fields=['sent_at']),
        ]
        ordering = ['-sent_at']

    subject = models.TextField(null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    sender = models.ForeignKey(Farmer, on_delete=models.PROTECT, related_name="sent_messages", verbose_name="Sender")
    recipient = models.ForeignKey(Farmer, related_name='received_messages', null=True, blank=True, on_delete=models.SET_NULL)
    sent_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    replied_at = models.DateTimeField(null=True, blank=True)
    sender_deleted_at = models.DateTimeField(null=True, blank=True)
    recipient_deleted_at = models.DateTimeField(null=True, blank=True)
    pending_delivery = models.BooleanField(default=False)

    @property
    def new(self):
        """returns whether the recipient has read the message or not"""
        return self.read_at is None

    def replied(self):
        """returns whether the recipient has written a reply to this message"""
        return self.replied_at is not None

    def send_email(self):
        if not self.recipient.email_for_messages_allowed:
            return

        protocol = 'https://' if os.getenv('PEPS_SECURE') == 'True' else 'http://'
        domain = protocol + os.getenv('PEPS_HOSTNAME', '')
        email_address = self.recipient.user.email
        email_subject = "Nouveau message de {0} sur Peps".format(self.sender.name)
        html_template = 'email-message.html'
        text_template = 'email-message.txt'
        context = {
            'recipient_name': self.recipient.name,
            'sender_name': self.sender.name,
            'body': self.body,
            'link': '/messages',
            'domain': domain,
        }
        text_message = loader.render_to_string(text_template, context)
        html_message = loader.render_to_string(html_template, context)
        email = EmailMultiAlternatives(
            email_subject,
            text_message,
            settings.DEFAULT_FROM_EMAIL,
            [email_address],
            headers={}
        )
        email.attach_alternative(html_message, 'text/html')
        email.send()

    def __str__(self):
        return f'Message from {self.sender.name} to {self.recipient.name}'
