from django.views.generic import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth import logout
from django.shortcuts import redirect

class FormView(UserPassesTestMixin, TemplateView):
    """
    This view is the in-house basic form.
    """
    template_name = 'basic-form.html'

    def test_func(self):
        return self.request.user.is_superuser

class VueAppDisplayView(TemplateView):
    """
    This is the VUE JS app web version of the client-facing simulator
    """
    template_name = 'application.html'

def logout_view(request):
    logout(request)
    return redirect('/#/map')
