from rest_framework import serializers
from data.models import Practice, Mechanism, Resource, PracticeType
from data.models import DiscardAction, Category


class MechanismSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mechanism
        fields = (
            'id',
            'name',
            'description',
        )


class ResourceSerializer(serializers.ModelSerializer):

    resource_type = serializers.ReadOnlyField(source='get_type_name')

    class Meta:
        model = Resource
        fields = (
            'id',
            'airtable_url',
            'name',
            'description',
            'resource_type',
            'url',
        )


class PracticeTypeSerializer(serializers.ModelSerializer):

    category = serializers.ReadOnlyField(source='get_category_name')

    class Meta:
        model = PracticeType
        fields = (
            'id',
            'display_text',
            'penalty',
            'category',
        )


class PracticeSerializer(serializers.ModelSerializer):
    mechanism = MechanismSerializer()
    main_resource = ResourceSerializer()
    secondary_resources = ResourceSerializer(many=True)
    types = PracticeTypeSerializer(many=True)
    image_url = serializers.ImageField(source='image', use_url=True)
    class Meta:
        model = Practice
        fields = (
            'id',
            'external_id',
            'mechanism',
            'modification_date',
            'title',
            'short_title',
            'description',
            'equipment',
            'schedule',
            'impact',
            'additional_benefits',
            'success_factors',
            'needs_tillage',
            'precision',
            'difficulty',
            'image',
            'image_url',
            'airtable_url',
            'main_resource',
            'main_resource_label',
            'secondary_resources',
            'types',
        )


class ResponseItemSerializer(serializers.Serializer):
    practice = PracticeSerializer()
    weight = serializers.DecimalField(max_digits=7, decimal_places=6)

    def update(self, instance, validated_data):
        raise NotImplementedError('`update()` must be implemented.')

    def create(self, validated_data):
        raise NotImplementedError('`create()` must be implemented.')

class ResponseSerializer(serializers.Serializer):
    practices = ResponseItemSerializer(many=True)
    suggestions = ResponseItemSerializer(many=True)

    def update(self, instance, validated_data):
        raise NotImplementedError('`update()` must be implemented.')

    def create(self, validated_data):
        raise NotImplementedError('`create()` must be implemented.')

class DiscardActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscardAction
        fields = (
            'practice_airtable_id',
            'reason',
        )

class CategorySerializer(serializers.ModelSerializer):
    practices = PracticeSerializer(many=True)

    class Meta:
        model = Category
        fields = (
            'id',
            'external_id',
            'image',
            'airtable_url',
            'title',
            'description',
            'practices',
        )
