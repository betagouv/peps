from rest_framework import serializers
from drf_base64.fields import Base64ImageField
from data.models import Farmer, FarmImage
from api.serializers import ExperimentFastSerializer, MediaListSerializer

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

class FarmImageFastSerializer(serializers.Serializer):
    """
    Serializer to be used in retrieval actions. By bypassing
    the overhead of the ModelSerializer it is significantly
    faster : https://hakibenita.com/django-rest-framework-slow
    """
    image = Base64ImageField()
    id = serializers.IntegerField(required=False)
    label = serializers.CharField()
    copyright = serializers.CharField()

class FarmImageSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    id = serializers.IntegerField(required=False)
    class Meta:
        model = FarmImage
        fields = (
            'image',
            'label',
            'copyright',
            'id'
        )

class FieldRetrievers():
    """
    For performance reasons, we have two serializers for the Farmer object:
    FarmerFastSerializer - a fast readonly serializer, useful for list retrieval, and
    FarmerSerializer - a slower but safer serializer used for Farmer creation/modification

    Both share these field retrieval methods.
    """
    # pylint: disable=no-member
    def get_experiments(self, obj):
        request = self.context.get('request')
        user = request.user if request else None

        if user and hasattr(user, 'farmer') and user.farmer == obj:
            return ExperimentFastSerializer(obj.experiments, context=self.context, many=True).data

        prefetched_approved_experiments = [x for x in obj.experiments.all() if x.state == 'Validé']
        return ExperimentFastSerializer(prefetched_approved_experiments, context=self.context, many=True).data

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
    # pylint: enable=no-member

class FarmerFastSerializer(serializers.Serializer, FieldRetrievers):
    """
    Serializer to be used in retrieval actions. By bypassing
    the overhead of the ModelSerializer it is significantly
    faster : https://hakibenita.com/django-rest-framework-slow
    """
    id = serializers.UUIDField(read_only=True)
    sequence_number = serializers.IntegerField(read_only=True)
    external_id = serializers.CharField(read_only=True)
    approved = serializers.BooleanField()
    name = serializers.CharField()
    farm_name = serializers.CharField()
    production = serializers.ListField()
    groups = serializers.ListField()
    agriculture_types = serializers.ListField()
    profile_image = Base64ImageField()
    images = MediaListSerializer(child=FarmImageFastSerializer())
    postal_code = serializers.CharField()
    experiments = serializers.SerializerMethodField(read_only=True)
    lat = serializers.DecimalField(max_digits=9, decimal_places=6)
    lon = serializers.DecimalField(max_digits=9, decimal_places=6)
    installation_date = serializers.DateField()
    personnel = serializers.CharField()
    livestock_types = serializers.ListField()
    livestock_number = serializers.CharField()
    cultures = serializers.CharField()
    soil_type = serializers.CharField()
    description = serializers.CharField()
    specificities = serializers.CharField()
    contact_possible = serializers.BooleanField()
    email_for_messages_allowed = serializers.BooleanField()
    links = serializers.ListField()
    surface = serializers.CharField()
    surface_cultures = serializers.CharField()
    surface_meadows = serializers.CharField()
    output = serializers.CharField()
    onboarding_shown = get_writable_method_field(serializers.BooleanField)()
    phone_number = get_writable_method_field(serializers.CharField)()
    email = serializers.SerializerMethodField()


class FarmerSerializer(serializers.ModelSerializer, FieldRetrievers):
    experiments = serializers.SerializerMethodField()
    images = MediaListSerializer(required=False, child=FarmImageSerializer(required=False))
    profile_image = Base64ImageField(required=False, allow_null=True)

    onboarding_shown = get_writable_method_field(serializers.BooleanField)()
    phone_number = get_writable_method_field(serializers.CharField)()
    email = serializers.SerializerMethodField()

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
            'email_for_messages_allowed',
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
