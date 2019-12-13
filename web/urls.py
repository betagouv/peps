from django.urls import path
from django.contrib.auth import views as auth_views
from web.views import FormView, VueAppDisplayView

urlpatterns = [
    path('', VueAppDisplayView.as_view(), name='app'),
    path('simulator', FormView.as_view(), name='form_view'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
]
