from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from data.models import Farmer

class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)

    @property
    def farmer_external_id(self):
        farmer = Farmer.objects.filter(email=self.user.email).first()
        return farmer.external_id if farmer else None

@receiver(post_save, sender=get_user_model())
def create_user_profile(instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=get_user_model())
def save_user_profile(instance, **kwargs):
    instance.profile.save()
