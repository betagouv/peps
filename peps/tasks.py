import os
from .celery import app
from datetime import datetime, timedelta
from data.models import Message
from django.conf import settings
from django.template import loader
import django.core.mail as mail

@app.task()
def remind_recipients():
    cutoff_date = datetime.today() - timedelta(days=7)
    messages = (Message
                .objects
                .filter(notified=False)
                .filter(pending_delivery=False)
                .filter(read_at__isnull=True)
                .filter(sent_at__lte=cutoff_date))
    for message in messages:
        conversation = (Message.objects.filter(sender=message.sender, recipient=message.recipient) 
                       | Message.objects.filter(sender=message.recipient, recipient=message.sender))
        if conversation.count() == 1:
            message.notified = True
            message.save()
            protocol = 'https://' if os.getenv('PEPS_SECURE') == 'True' else 'http://'
            domain = protocol + os.getenv('PEPS_HOSTNAME', '')
            context = {
                'recipient_name': message.recipient.name,
                'sender_name': message.sender.name,
                'body': message.body,
                'link': '/messages',
                'domain': domain,
            }
            text_message = loader.render_to_string('email-reminder.txt', context)
            html_message = loader.render_to_string('email-reminder.html', context)
            from_email = settings.MAGICAUTH_FROM_EMAIL
            mail.send_mail(
                subject='Rappel 🛎 - Vous avez un message non lu de {0}'.format(message.sender.name),
                from_email=from_email,
                recipient_list=[message.recipient.user.email],
                message=text_message,
                html_message=html_message,
                fail_silently=True,
            )
