from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from data.models import Experiment, Farmer, ExperimentImage, ExperimentVideo, FarmImage

admin.site.site_header = 'Administration Peps'

class ExperimentImageForm(forms.ModelForm):
    class Meta:
        model = ExperimentImage
        exclude = []
        widgets = {
            'label': forms.Textarea(attrs={'cols': 35, 'rows': 1}),
        }

class ExperimentImageInline(admin.TabularInline):
    model = ExperimentImage
    form = ExperimentImageForm
    extra = 0
    fields = ('image', 'label')


class ExperimentVideoForm(forms.ModelForm):
    class Meta:
        model = ExperimentVideo
        exclude = []
        widgets = {
            'label': forms.Textarea(attrs={'cols': 35, 'rows': 1}),
        }

class ExperimentVideoInline(admin.TabularInline):
    model = ExperimentVideo
    form = ExperimentVideoForm
    extra = 0
    fields = ('video', 'label')


class ExperimentForm(forms.ModelForm):
    class Meta:
        exclude = ('airtable_json', 'external_id', 'creation_date', 'method', 'temporality', 'origin', 'execution', 'additional_details')
        model = Experiment
        widgets = {
            'name': forms.Textarea(attrs={'cols': 35, 'rows': 1}),
            'objectives': forms.Textarea(attrs={'cols': 55, 'rows': 2}),
            'equipment': forms.Textarea(attrs={'cols': 35, 'rows': 1}),
            'results_details': forms.Textarea(attrs={'cols': 55, 'rows': 6}),
            'description': forms.Textarea(attrs={'cols': 55, 'rows': 8}),
            'investment': forms.Textarea(attrs={'cols': 55, 'rows': 2}),
            'surface': forms.Textarea(attrs={'cols': 35, 'rows': 1}),
        }

@admin.register(Experiment)
class ExperimentAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'xp_type', 'results',)
    inlines = (ExperimentImageInline, ExperimentVideoInline)
    form = ExperimentForm

    def author(self, obj):
        return format_html('<a href="{0}">{1}</a>'.format('/admin/data/farmer/' + str(obj.farmer.id), obj.farmer.name))


class FarmImageForm(forms.ModelForm):
    class Meta:
        model = FarmImage
        exclude = []
        widgets = {
            'label': forms.Textarea(attrs={'cols': 35, 'rows': 1}),
        }

class FarmImageInline(admin.TabularInline):
    model = FarmImage
    form = FarmImageForm
    extra = 0
    fields = ('image', 'label')

class FarmerForm(forms.ModelForm):
    class Meta:
        exclude = ('airtable_json', 'airtable_url', 'external_id', 'creation_date')
        model = Farmer
        widgets = {
            'name': forms.Textarea(attrs={'cols': 35, 'rows': 1}),
            'personnel': forms.Textarea(attrs={'cols': 35, 'rows': 1}),
            'livestock_number': forms.Textarea(attrs={'cols': 35, 'rows': 1}),
            'cultures': forms.Textarea(attrs={'cols': 55, 'rows': 3}),
            'soil_type': forms.Textarea(attrs={'cols': 35, 'rows': 1}),
            'description': forms.Textarea(attrs={'cols': 55, 'rows': 10}),
            'specificities': forms.Textarea(attrs={'cols': 55, 'rows': 10}),
            'surface': forms.Textarea(attrs={'cols': 35, 'rows': 1}),
            'surface_cultures': forms.Textarea(attrs={'cols': 35, 'rows': 1}),
            'surface_meadows': forms.Textarea(attrs={'cols': 35, 'rows': 1}),
            'output': forms.Textarea(attrs={'cols': 35, 'rows': 1}),
        }
        help_texts = {
            'email': 'Ce champ est utilisé pour le login',
        }

@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = ('name', 'postal_code', 'cultures',)
    inlines = (FarmImageInline, )
    form = FarmerForm
