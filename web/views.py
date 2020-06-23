from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth import logout
from django.contrib.auth import login, authenticate
from django.conf import settings
from django.urls import reverse_lazy
from django.shortcuts import redirect, render

from web.registerform import RegisterForm

class SimulatorFormView(UserPassesTestMixin, TemplateView):
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


class RegisterView(FormView):

    form_class = RegisterForm
    success_url = reverse_lazy("magicauth-email-sent")
    template_name = 'register.html'

    def form_valid(self, form):
        form.save()
        next_view = self.request.GET.get(
            "next",
            f"/{settings.MAGICAUTH_LOGGED_IN_REDIRECT_URL_NAME}/"
        )
        current_site = self.request.site
        form.send_email(current_site, next_view)
        return super().form_valid(form)

def logout_view(request):
    logout(request)
    return redirect('/map')
