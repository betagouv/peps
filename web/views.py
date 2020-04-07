from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.shortcuts import redirect

class FormView(LoginRequiredMixin, TemplateView):
    """
    This view is the in-house basic form.
    """
    template_name = 'basic-form.html'

class VueAppDisplayView(TemplateView):
    """
    This is the VUE JS app web version of the client-facing simulator
    """
    template_name = 'application.html'

def logout_view(request):
    logout(request)
    return redirect('/#/map')
