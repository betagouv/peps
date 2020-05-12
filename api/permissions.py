from rest_framework import permissions
from data.models import Experiment, Farmer

class IsExperimentAuthor(permissions.BasePermission):
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

    def has_permission(self, request, view):
        if not request.user or not request.user.farmer:
            return False
        experiment_id = request.resolver_match.kwargs.get('pk')
        if not experiment_id:
            return False
        experiment = Experiment.objects.get(id=experiment_id)
        return experiment and experiment.farmer == request.user.farmer


class IsFarmer(permissions.BasePermission):
    """
    These are for actions only permitted for farmers
    """
    def has_object_permission(self, request, view, obj):
        return request.user and hasattr(request.user, 'farmer') and request.user.farmer

    def has_permission(self, request, view):
        return request.user and hasattr(request.user, 'farmer') and request.user.farmer


class IsProfileOwner(permissions.BasePermission):
    """
    These are for actions only permitted for farmers
    """
    def has_object_permission(self, request, view, obj):
        if not isinstance(obj, Farmer):
            return False
        return request.user and hasattr(request.user, 'farmer') and request.user.farmer == obj

    def has_permission(self, request, view):
        if not request.user or not hasattr(request.user, 'farmer'):
            return False
        farmer_id = request.resolver_match.kwargs.get('pk')
        if not farmer_id:
            return False
        farmer = Farmer.objects.get(id=farmer_id)
        return farmer and farmer == request.user.farmer
