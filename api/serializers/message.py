import uuid
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from data.models import Farmer
from data.models import Message

class AsymetricFarmerMixin(object):
    """
    Allows setting the field with a farmer ID, serializes it
    with an object
    """
    def _decode(self, data):
        if isinstance(data, str):
            try:
                farmer_id = uuid.UUID(data)
                data = {'id': str(farmer_id)}
            except Exception as _:
                raise ValidationError('Recipient id is not valid')
        return data

    def to_internal_value(self, data):
        data = self._decode(data)
        return super(AsymetricFarmerMixin, self).to_internal_value(data)


class MessageFarmer(AsymetricFarmerMixin, serializers.ModelSerializer):
    id = serializers.UUIDField()

    class Meta:
        model = Farmer
        read_only_fields = [
            'sequence_number',
        ]
        fields = (
            'id',
            'sequence_number',
            'name',
            'url_slug',
            'farm_name',
            'sequence_number',
            'production',
            'groups',
            'agriculture_types',
            'profile_image',
        )

    def update(self, instance, validated_data):
        raise NotImplementedError('Update not allowed with this serializer')

    def create(self, validated_data):
        raise NotImplementedError('Create not allowed with this serializer')


class MessageSerializer(serializers.ModelSerializer):

    sender = MessageFarmer(read_only=True)
    recipient = MessageFarmer()

    class Meta:
        model = Message
        read_only_fields = [
            'id',
            'sender',
            'recipient',
            'sent_at',
        ]
        fields = (
            'id',
            'sender',
            'subject',
            'body',
            'recipient',
            'sent_at',
            'read_at',
            'new',
            'replied'
        )


    def create(self, validated_data):
        try:
            recipient = Farmer.objects.get(pk=validated_data.pop('recipient')['id'])
            sender = self.context['request'].user.farmer
            new_data = {**validated_data, **{'recipient': recipient, 'sender': sender}}
            instance = Message.objects.create(**new_data)
            return instance
        except Exception as _:
            raise ValidationError('Could not find recipient')

    def update(self, instance, validated_data):
        raise NotImplementedError('Update not allowed with this serializer')
