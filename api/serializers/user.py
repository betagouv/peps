from rest_framework import serializers
from django.contrib.auth import get_user_model

class LoggedUserSerializer(serializers.ModelSerializer):

    farmer_external_id = serializers.SlugRelatedField(
        source='farmer',
        read_only=True,
        slug_field='external_id'
    )

    farmer_id = serializers.SlugRelatedField(
        source='farmer',
        read_only=True,
        slug_field='id'
    )

    farmer_sequence_number = serializers.SlugRelatedField(
        source='farmer',
        read_only=True,
        slug_field='sequence_number'
    )

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'email',
            'farmer_external_id',
            'farmer_id',
            'farmer_sequence_number',
            'is_superuser',
            'username',
            'first_name',
            'last_name',
        )
