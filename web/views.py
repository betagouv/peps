import json
from django.http import JsonResponse
from django.urls import reverse
from django.views.generic import TemplateView, View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin

class FormView(LoginRequiredMixin, TemplateView):
    """
    This view is the in-house basic form.
    """
    template_name = 'basic-form.html'


@method_decorator(csrf_exempt, name='dispatch')
class ProductionSystemFormView(LoginRequiredMixin, View):
    """
    UGLY temporary workaround while we have a proper form and/or
    use local storage in the client side. I'm sorry.

    Only sets the session variables and then tells
    where to redirect in JSON mode.
    """

    def post(self, request):
        from api.views import RankingsApiView
        from api.serializers import ResponseItemSerializer
        from rest_framework.renderers import JSONRenderer

        post_data = json.loads(request.body)
        answers = post_data['answers']
        blacklist = post_data['blacklist']
        suggestions = RankingsApiView.get_results(answers, blacklist)[1]
        suggestions_rendered = JSONRenderer().render(ResponseItemSerializer(suggestions, many=True).data)

        request.session['answers'] = answers
        request.session['blacklist'] = blacklist
        request.session['suggestions'] = json.loads(suggestions_rendered)

        return JsonResponse({'url': reverse('user_display')})

class UserDisplayView(LoginRequiredMixin, TemplateView):
    """
    This view is what the user may see directly.
    """
    template_name = 'user-display.html'

    def get_context_data(self, **kwargs):
        context = {
            'answers': self.request.session['answers'],
            'blacklist': self.request.session['blacklist'],
            'suggestions': self.request.session['suggestions'],
        }
        return context
