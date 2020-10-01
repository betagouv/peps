from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):

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

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'email',
            'farmer_external_id',
            'farmer_id',
            'is_superuser',
            'username',
            'first_name',
            'last_name',
        )
