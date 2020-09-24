import uuid
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from drf_base64.fields import Base64ImageField, Base64FileField
from data.models import Practice, Mechanism, Resource, PracticeType
from data.models import DiscardAction, Category, Farmer, Experiment
from data.models import ExperimentImage, ExperimentVideo, FarmImage
from data.models import Message

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
        model = User
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
