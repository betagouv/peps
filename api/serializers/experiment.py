
from rest_framework import serializers
from drf_base64.fields import Base64ImageField, Base64FileField
from data.models import Experiment
from data.models import ExperimentImage, ExperimentVideo
from api.serializers import MediaListSerializer


class ExperimentImageSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    id = serializers.IntegerField(required=False)
    class Meta:
        model = ExperimentImage
        fields = (
            'image',
            'label',
            'copyright',
            'id',
        )

class ExperimentImageFastSerializer(serializers.Serializer):
    """
    Serializer to be used in retrieval actions. By bypassing
    the overhead of the ModelSerializer it is significantly
    faster : https://hakibenita.com/django-rest-framework-slow
    """
    image = Base64ImageField()
    id = serializers.IntegerField(required=False)
    label = serializers.CharField()
    copyright = serializers.CharField()


class ExperimentVideoSerializer(serializers.ModelSerializer):
    video = Base64FileField()
    id = serializers.IntegerField(required=False)
    class Meta:
        model = ExperimentVideo
        fields = (
            'video',
            'label',
            'copyright',
            'id'
        )

class ExperimentVideoFastSerializer(serializers.Serializer):
    """
    Serializer to be used in retrieval actions. By bypassing
    the overhead of the ModelSerializer it is significantly
    faster : https://hakibenita.com/django-rest-framework-slow
    """
    video = Base64FileField()
    id = serializers.IntegerField(required=False)
    label = serializers.CharField()
    copyright = serializers.CharField()


class ExperimentFastSerializer(serializers.Serializer):
    """
    Serializer to be used in retrieval actions. By bypassing
    the overhead of the ModelSerializer it is significantly
    faster : https://hakibenita.com/django-rest-framework-slow
    """
    images = MediaListSerializer(required=False, child=ExperimentImageFastSerializer(required=False))
    videos = MediaListSerializer(required=False, child=ExperimentVideoFastSerializer(required=False))
    id = serializers.UUIDField(read_only=True)
    sequence_number = serializers.IntegerField(read_only=True)
    external_id = serializers.CharField(read_only=True)
    tags = serializers.ListField()
    approved = serializers.BooleanField()
    state = serializers.CharField()
    name = serializers.CharField()
    short_name = serializers.CharField()
    objectives = serializers.CharField()
    equipment = serializers.CharField()
    control_presence = serializers.BooleanField()
    ongoing = serializers.BooleanField()
    results = serializers.CharField()
    results_details = serializers.CharField()
    links = serializers.ListField()

    description = serializers.CharField()
    investment = serializers.CharField()
    surface = serializers.CharField()
    surface_type = serializers.ListField()
    xp_type = serializers.CharField()

    cultures = serializers.ListField()
    creation_date = serializers.DateTimeField()
    modification_date = serializers.DateTimeField()


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
            'state',
            'name',
            'short_name',
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
            'cultures',
            'creation_date',
            'modification_date',
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


class ExperimentBriefsFastSerializer(serializers.Serializer):
    """
    Serializer to be used in retrieval actions. Only limited
    information is exposed, meant for a card display.
    """
    images = MediaListSerializer(required=False, child=ExperimentImageFastSerializer(required=False))
    id = serializers.UUIDField(read_only=True)
    sequence_number = serializers.IntegerField(read_only=True)
    tags = serializers.ListField()
    name = serializers.CharField()
    short_name = serializers.CharField()
    cultures = serializers.ListField()
    creation_date = serializers.DateTimeField()
    modification_date = serializers.DateTimeField()
    farmer = serializers.PrimaryKeyRelatedField(read_only=True)
    farmer_url_slug = serializers.SlugRelatedField(source="farmer", slug_field='url_slug', read_only=True)
    livestock_types = serializers.SlugRelatedField(source="farmer", slug_field='livestock_types', read_only=True)
    postal_code = serializers.SlugRelatedField(source="farmer", slug_field='postal_code', read_only=True)
    farmer_name = serializers.SlugRelatedField(source="farmer", slug_field='name', read_only=True)
    agriculture_types = serializers.SlugRelatedField(source="farmer", slug_field='agriculture_types', read_only=True)
