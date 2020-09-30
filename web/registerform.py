from django import forms
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.template import loader
from django.core.mail import send_mail
from django.utils.safestring import mark_safe
from magicauth.models import MagicToken
from data.models import Farmer


class RegisterForm(forms.ModelForm):
    email = forms.EmailField(label="", widget=forms.EmailInput(attrs={'placeholder': 'Votre email'}))
    email2 = forms.EmailField(label="", widget=forms.EmailInput(attrs={'placeholder': 'Confirmez votre email'}))
    name = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Nom et prénom'}))
    phone_number = forms.CharField(required=False, label="", widget=forms.TextInput(attrs={'placeholder': 'Votre numéro téléphone'}))
    cgu_approved = forms.BooleanField(label=mark_safe('J\'ai lu et j\'accepte les <a href="/conditions-generales-d-utilisation" target="_blank">conditions d\'utilisation</a>'))

    class Meta:
        model = Farmer
        fields = ('name', 'email', 'email2', 'phone_number', 'cgu_approved',)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.label_suffix = ""

    def clean_cgu_approved(self):
        if not self.cleaned_data.get("cgu_approved"):
            raise forms.ValidationError("Vous devez accepter les conditions d'utilisation")
        return self.cleaned_data['cgu_approved']

    def clean_email2(self):
        email1 = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')

        if email1 and email2 and email1 != email2:
            raise forms.ValidationError(
                'Les adresses email renseignés ne sont pas les mêmes',
                code='email_mismatch',
            )
        try:
            user = User.objects.get(email=email2)
            raise forms.ValidationError("Nous avons déjà un compte avec cette adresse mail. Voulez-vous <a onclick=\"window.location='/login'+window.location.search;\" style=\"color: #295a9f; text-decoration: underline; cursor: pointer; \">vous identifier</a> ?")
        except ObjectDoesNotExist as _:
            return email2

    def save(self, commit=True):
        farmer = super(RegisterForm, self).save(commit=False)
        farmer.email = User.objects.normalize_email(self.cleaned_data['email'])
        farmer.self_created = True

        if commit:
            farmer.save()

        return farmer

    def send_token_email(self, current_site, next_view):
        user_email = self.cleaned_data["email"]
        email_field = settings.MAGICAUTH_EMAIL_FIELD
        field_lookup = {f"{email_field}__iexact": user_email}
        user = User.objects.get(**field_lookup)
        token = MagicToken.objects.create(user=user)
        email_subject = settings.MAGICAUTH_EMAIL_SUBJECT
        html_template = settings.MAGICAUTH_EMAIL_HTML_TEMPLATE
        text_template = settings.MAGICAUTH_EMAIL_TEXT_TEMPLATE
        from_email = settings.MAGICAUTH_FROM_EMAIL
        context = {
            "token": token,
            "user": user,
            "site": current_site,
            "next_view": next_view,
        }
        text_message = loader.render_to_string(text_template, context)
        html_message = loader.render_to_string(html_template, context)
        send_mail(
            subject=email_subject,
            message=text_message,
            from_email=from_email,
            html_message=html_message,
            recipient_list=[user_email],
            fail_silently=False,
        )

    def send_onboarding_email(self, current_site):
        user_email = self.cleaned_data["email"]
        email_subject = 'Bienvenue sur Peps 🌱'
        html_template = 'email-onboarding.html'
        text_template = 'email-onboarding.txt'
        from_email = settings.MAGICAUTH_FROM_EMAIL

        context = {
            "site": current_site,
        }
        text_message = loader.render_to_string(text_template, context)
        html_message = loader.render_to_string(html_template, context)

        send_mail(
            subject=email_subject,
            message=text_message,
            from_email=from_email,
            html_message=html_message,
            recipient_list=[user_email],
            fail_silently=False,
        )
