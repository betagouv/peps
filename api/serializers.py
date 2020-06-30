from rest_framework import serializers
from django.contrib.auth.models import User
from drf_base64.fields import Base64ImageField, Base64FileField
from data.models import Practice, Mechanism, Resource, PracticeType
from data.models import DiscardAction, Category, Farmer, Experiment
from data.models import ExperimentImage, ExperimentVideo, FarmImage

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
    image = Base64ImageField()
    id = serializers.IntegerField(required=False)
    class Meta:
        model = ExperimentImage
        fields = (
            'image',
            'label',
            'id',
        )


class ExperimentVideoSerializer(serializers.ModelSerializer):
    video = Base64FileField()
    id = serializers.IntegerField(required=False)
    class Meta:
        model = ExperimentVideo
        fields = (
            'video',
            'label',
            'id'
        )


class MediaListSerializer(serializers.ListSerializer):
    """
    For linked models and list serializers, we need to specify the update behaviour since
    Django Rest Framework does not do it :
    https://www.django-rest-framework.org/api-guide/serializers/#customizing-multiple-update
    """

    def update(self, instance, validated_data):
        instance_mapping = {instance.id: instance for instance in instance}

        media = []

        # New media will be created and existing media will be updated.
        for item in validated_data:
            element = instance_mapping.get(item.get('id'), None)
            if element is None:
                media.append(self.child.create(item))
            else:
                media.append(self.child.update(element, item))

        # Media that was removed will be also removed from the database.
        data_mapping = {item['id']: item for item in validated_data if item.get('id')}
        for element_id, element in instance_mapping.items():
            if element_id not in data_mapping:
                element.delete()

        return media



class ExperimentSerializer(serializers.ModelSerializer):
    images = MediaListSerializer(required=False, child=ExperimentImageSerializer(required=False))
    videos = MediaListSerializer(required=False, child=ExperimentVideoSerializer(required=False))

    class Meta:
        model = Experiment
        read_only_fields = [
            'id',
            'sequence_number',
            'external_id',
        ]
        fields = (
            'id',
            'sequence_number',
            'external_id',
            'tags',
            'approved',
            'name',
            'objectives',
            'equipment',
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

    def create(self, validated_data):
        if 'images' not in validated_data and 'videos' not in validated_data:
            return super().create(validated_data)

        image_validated_data = validated_data.pop('images', None)
        video_validated_data = validated_data.pop('videos', None)
        experiment = super().create(validated_data)

        if image_validated_data is not None:
            experiment_image_serializer = self.fields['images']
            for item in image_validated_data:
                item['experiment'] = experiment
            experiment_image_serializer.create(image_validated_data)

        if video_validated_data is not None:
            experiment_video_serializer = self.fields['videos']
            for item in video_validated_data:
                item['experiment'] = experiment
            experiment_video_serializer.create(video_validated_data)

        return experiment


    def update(self, instance, validated_data):
        if 'images' not in validated_data and 'videos' not in validated_data:
            return super().update(instance, validated_data)

        image_validated_data = validated_data.pop('images', None)
        video_validated_data = validated_data.pop('videos', None)
        experiment = super().update(instance, validated_data)

        if image_validated_data is not None:
            experiment_image_serializer = self.fields['images']
            for item in image_validated_data:
                item['experiment'] = experiment
            experiment_image_serializer.update(experiment.images.all(), image_validated_data)

        if video_validated_data is not None:
            experiment_video_serializer = self.fields['videos']
            for item in video_validated_data:
                item['experiment'] = experiment
            experiment_video_serializer.update(experiment.videos.all(), video_validated_data)

        return experiment

class FarmImageSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    id = serializers.IntegerField(required=False)
    class Meta:
        model = FarmImage
        fields = (
            'image',
            'label',
            'id'
        )

def get_writable_method_field(base_serializer_class):
    """
    Returns a SerializerMethod field that inherits the update
    methods from another serializer class.
    """
    class WritableSerializerMethodField(base_serializer_class):
        def __init__(self, method_name=None, **kwargs):
            self.method_name = method_name
            super().__init__(**kwargs)

        def bind(self, field_name, parent):
            default_method_name = 'get_{field_name}'.format(field_name=field_name)
            if self.method_name is None:
                self.method_name = default_method_name
            super().bind(field_name, parent)

        def to_representation(self, value):
            method = getattr(self.parent, self.method_name)
            return method(value)

        def get_attribute(self, instance):
            return instance
    return WritableSerializerMethodField


class FarmerSerializer(serializers.ModelSerializer):
    experiments = serializers.SerializerMethodField()
    images = MediaListSerializer(required=False, child=FarmImageSerializer(required=False))
    profile_image = Base64ImageField(required=False, allow_null=True)

    onboarding_shown = get_writable_method_field(serializers.BooleanField)()
    phone_number = get_writable_method_field(serializers.CharField)()
    email = serializers.SerializerMethodField()

    def get_experiments(self, obj):
        request = self.context.get('request')
        user = request.user if request else None

        if user and hasattr(user, 'farmer') and user.farmer == obj:
            return ExperimentSerializer(obj.experiments, context=self.context, many=True).data
        return ExperimentSerializer(obj.approved_experiments, context=self.context, many=True).data

    def get_onboarding_shown(self, obj):
        return self._field_if_logged(obj, 'onboarding_shown')

    def get_phone_number(self, obj):
        return self._field_if_logged(obj, 'phone_number')

    def get_email(self, obj):
        return self._field_if_logged(obj, 'email')

    def _field_if_logged(self, obj, field_name):
        request = self.context.get('request')
        user = request.user if request else None

        if user and hasattr(user, 'farmer') and user.farmer == obj:
            return getattr(obj, field_name)
        return None

    class Meta:
        model = Farmer
        read_only_fields = [
            'id',
            'external_id',
            'experiments',
            'sequence_number',
        ]
        fields = (
            'id',
            'sequence_number',
            'external_id',
            'approved',
            'name',
            'farm_name',
            'production',
            'groups',
            'agriculture_types',
            'profile_image',
            'images',
            'postal_code',
            'experiments',
            'lat',
            'lon',
            'installation_date',
            'personnel',
            'livestock_types',
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
            'onboarding_shown',
            'phone_number',
            'email',
        )

    def update(self, instance, validated_data):
        if 'images' not in validated_data:
            return super().update(instance, validated_data)

        image_validated_data = validated_data.pop('images', None)
        farmer = super().update(instance, validated_data)

        if image_validated_data is not None:
            farmer_image_serializer = self.fields['images']
            for item in image_validated_data:
                item['farmer'] = farmer
            farmer_image_serializer.update(farmer.images.all(), image_validated_data)

        return farmer

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
