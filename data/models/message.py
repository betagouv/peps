from django.db import models
from data.models import Farmer
from django.utils import timezone


class Message(models.Model):
    subject = models.TextField(null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    sender = models.ForeignKey(Farmer, on_delete=models.PROTECT, related_name="sent_messages", verbose_name="Sender")
    recipient = models.ForeignKey(Farmer, related_name='received_messages', null=True, blank=True, on_delete=models.SET_NULL)
    sent_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    replied_at = models.DateTimeField(null=True, blank=True)
    sender_deleted_at = models.DateTimeField(null=True, blank=True)
    recipient_deleted_at = models.DateTimeField(null=True, blank=True)

    @property
    def new(self):
        """returns whether the recipient has read the message or not"""
        return self.read_at is None

    def replied(self):
        """returns whether the recipient has written a reply to this message"""
        return self.replied_at is not None

    def __str__(self):
        return f'Message "{self.subject}"'

    class Meta:
        ordering = ['-sent_at']
