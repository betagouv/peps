import json
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer

class MessageConsumer(WebsocketConsumer):
    def connect(self):
        self.farmer_id = self.scope['url_route']['kwargs']['farmer_id']
        self.group_name = '%s_messages_%s' % (settings.REDIS_MESSAGE_PREPEND, self.farmer_id)

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    @staticmethod
    def notify_farmer(farmer_id):
        channel_layer = get_channel_layer()
        message = "New message"
        group_name = '%s_messages_%s' % (settings.REDIS_MESSAGE_PREPEND, farmer_id)
        async_to_sync(channel_layer.group_send)(
            group_name,
            {'type': 'message_notification', 'message': message}
        )

    def message_notification(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'message': message
        }))
