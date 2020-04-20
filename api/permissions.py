from rest_framework import permissions
from data.models import Experiment

class IsExperimentAuthor(permissions.IsAuthenticated):
    """
    Custom permission to only allow the author of an experiment
    to make certain actions to it.
    """
    def has_object_permission(self, request, view, obj):

        if not isinstance(obj, Experiment):
            return False
        if not request.user or not request.user.farmer:
            return False

        return obj.farmer == request.user.farmer

class IsFarmer(permissions.IsAuthenticated):
    """
    These are for actions only permitted for farmers
    """
    def has_object_permission(self, request, view, obj):
        if not isinstance(obj, Experiment):
            return False
        return request.user and request.user.farmer
