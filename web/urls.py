from django.urls import path
from web.views import SimulatorFormView, VueAppDisplayView, logout_view, RegisterView

urlpatterns = [
    path('', VueAppDisplayView.as_view(), name='app'),
    path('simulator', SimulatorFormView.as_view(), name='form_view'),
    path('logout', logout_view, name='logout'),
    path('register', RegisterView.as_view(), name='register'),
]
