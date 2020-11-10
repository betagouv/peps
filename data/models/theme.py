from urllib.parse import quote
from django.db import models, connection
from django.utils import timezone
from django.utils.html import mark_safe
from data.utils import optimize_image
from .experiment import Experiment
class Theme(models.Model):

    modification_date = models.DateTimeField(auto_now=True)
    creation_date = models.DateTimeField(default=timezone.now)

    active = models.BooleanField(default=False, db_index=True)

    name = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    experiments = models.ManyToManyField(Experiment)

    image = models.ImageField(null=True, blank=True)
    copyright = models.TextField(null=True, blank=True)

    @property
    def url_slug(self):
        url_name = quote(self.name or '')
        if self.id:
            return f'{url_name}--{self.id}'
        else:
            return ''

    @property
    def url_path(self):
        return f'/themes/{self.url_slug}'

    @property
    def html_link(self):
        """ # TODO, refactoring needed
        This is used in the admin panel to link to the farmer's page
        """
        if self.id:
            unescaped_url = f'/themes/{self.name or ""}--{self.id}'
            return mark_safe(f'<a href="{self.url_path}" target="_blank">{unescaped_url}</a>')
        else:
            return 'Pas encore live'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.image:
            self.image = optimize_image(self.image, self.image.name)
        super(Theme, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.name
