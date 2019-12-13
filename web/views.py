import json
from rest_framework.renderers import JSONRenderer
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from api.serializers import PracticeSerializer
from data.models import Practice

class FormView(LoginRequiredMixin, TemplateView):
    """
    This view is the in-house basic form.
    """
    template_name = 'basic-form.html'

class UserDisplayView(LoginRequiredMixin, TemplateView):
    """
    This view is what the user may see directly.
    """
    template_name = 'user-display.html'

    def get_context_data(self, **kwargs):
        query_param = self.request.GET.get('practices')
        practice_external_ids = query_param.split(',') if query_param else []
        suggestions = [Practice.objects.filter(external_id=x).first() for x in practice_external_ids]
        suggestions_rendered = JSONRenderer().render(PracticeSerializer([x for x in suggestions if x], many=True).data)
        context = {
            'suggestions': json.loads(suggestions_rendered),
        }
        return context

class VueAppDisplayView(TemplateView):
    """
    This is the VUE JS app web version of the client-facing simulator
    """
    template_name = 'application.html'
