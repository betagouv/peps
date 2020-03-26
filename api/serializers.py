from rest_framework import serializers
from data.models import Practice, Mechanism, Resource, PracticeType
from data.models import DiscardAction, Category, Farmer, Experiment, ExperimentImage, ExperimentVideo


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
            'image',
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

class ExperimentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperimentImage
        fields = (
            'image',
        )

class ExperimentVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperimentVideo
        fields = (
            'video',
        )

class ExperimentSerializer(serializers.ModelSerializer):
    images = ExperimentImageSerializer(many=True)
    videos = ExperimentVideoSerializer(many=True)

    class Meta:
        model = Experiment
        fields = (
            'id',
            'external_id',
            'name',
            'objectives',
            'method',
            'temporality',
            'equipment',
            'execution',
            'control_presence',
            'ongoing',
            'results',
            'results_details',
            'links',
            'description',
            'investment',
            'surface',
            'surface_type',
            'xp_type',
            'images',
            'videos',
        )

class FarmerSerializer(serializers.ModelSerializer):
    experiments = ExperimentSerializer(many=True)

    class Meta:
        model = Farmer
        fields = (
            'id',
            'external_id',
            'name',
            'production',
            'groups',
            'agriculture_types',
            'profile_image',
            'postal_code',
            'experiments',
            'lat',
            'lon',
            'installation_date',
            'personnel',
            'livestock_type',
            'livestock_number',
            'cultures',
            'soil_type',
            'description',
            'specificities',
            'contact_possible',
            'links',
            'surface',
            'surface_cultures',
            'surface_meadows',
            'output',
        )
