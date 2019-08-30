from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework import permissions, authentication
from rest_framework_api_key.permissions import HasAPIKey
from data.adapters import AirtableAdapter
from api.engine import Engine
from api.serializers import ResponseSerializer
from api.models import Response
from api.formschema import get_form_schema

# For the moment, we will authorize access to this endpoint in one of these two situations:
# - The user logged in and has a session (which identifies a user)
# - The call has an API key (which identifies projects, not users)
class RankingsApiView(APIView):
    """
    This view will return a list of practice IDs that
    correspond to the form from FormView.
    """
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [HasAPIKey | permissions.IsAuthenticated]

    def post(self, request):
        post_data = request.data
        practices, suggestions = RankingsApiView.get_results(
            post_data.get('answers'),
            post_data.get('practice_blacklist', []),
            post_data.get('type_blacklist', []))

        response = Response(practices, suggestions)
        data = JSONRenderer().render(ResponseSerializer(response).data)

        return HttpResponse(data, content_type="application/json")

    @staticmethod
    def get_results(answers, practice_blacklist, type_blacklist):
        engine = Engine(answers, practice_blacklist, type_blacklist)
        practices = engine.calculate_results()
        suggestions = engine.get_suggestions(practices)
        return (practices, suggestions)


class RefreshDataApiView(APIView):
    """
    This view will return a list of practice IDs that
    correspond to the form from FormView.
    """
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated | HasAPIKey]

    def post(self, request):
        AirtableAdapter.update_practices()
        return JsonResponse({"success": True})


class FormSchemaView(APIView):
    """
    This view will return the schema needed for rendering
    the form in the front-end
    """
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated | HasAPIKey]

    def get(self, request):
        return JsonResponse(get_form_schema())
