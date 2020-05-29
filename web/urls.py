from django.urls import path
from django.views.generic.base import RedirectView
from web.views import SimulatorFormView, VueAppDisplayView, logout_view, RegisterView

urlpatterns = [
    path('', VueAppDisplayView.as_view(), name='app'),
    path('app/', RedirectView.as_view(pattern_name="app"), name='app_redirect'),
    path('simulator', SimulatorFormView.as_view(), name='form_view'),
    path('logout', logout_view, name='logout'),
    path('register', RegisterView.as_view(), name='register'),
]
