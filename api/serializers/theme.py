from rest_framework import serializers
from api.serializers import ExperimentBriefsFastSerializer, MediaListSerializer
from data.models import Experiment

class ThemeFastSerializer(serializers.Serializer):
    """
    Serializer to be used in retrieval actions. By bypassing
    the overhead of the ModelSerializer it is significantly
    faster : https://hakibenita.com/django-rest-framework-slow
    """
    def get_experiments(self, obj):
        prefetched_approved_experiments = obj.experiments.filter(state='Validé')
        return ExperimentBriefsFastSerializer(prefetched_approved_experiments, context=self.context, many=True).data

    id = serializers.UUIDField(read_only=True)
    active = serializers.BooleanField()
    name = serializers.CharField()
    description = serializers.CharField()
    creation_date = serializers.DateTimeField()
    modification_date = serializers.DateTimeField()
    experiments = serializers.SerializerMethodField(read_only=True)
    url_slug = serializers.CharField(read_only=True)
    image = serializers.ImageField()
    copyright = serializers.CharField()
