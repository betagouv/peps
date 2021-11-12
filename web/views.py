import datetime
from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth import logout
from django.conf import settings
from django.urls import reverse_lazy
from django.shortcuts import redirect
from api.utils import AsanaUtils

from web.registerform import RegisterForm


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
        form.send_token_email(current_site, next_view)
        form.send_onboarding_email(current_site)

        try:
            AsanaUtils.send_task(
                settings.ASANA_PROJECT,
                'Création de compte Peps ({0})'.format(form.data['name']),
                '{0} a crée son compte sur /register'.format(form.data['name']),
                None)
        except Exception as _:
            print('Error sending task to Asana for newly created user')

        return super().form_valid(form)

def logout_view(request):
    logout(request)
    return redirect('/')
