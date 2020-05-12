from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from django.core.exceptions import ValidationError
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
        fields = [
            'name',
            'farmer',
            'approved',
            'xp_type',
            'objectives',
            'description',
            'results',
            'results_details',
            'tags',
            'control_presence',
            'ongoing',
            'equipment',
            'links',
            'investment',
            'surface_type',
            'surface',
        ]
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

class ApprovalFilter(admin.SimpleListFilter):
    title = 'Approval status'
    parameter_name = ''

    def lookups(self, request, model_admin):
        return [
            ('approved', 'Approved'),
            ('not_approved', 'Not approved'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'approved':
            return queryset.distinct().filter(approved=True)
        if self.value() == 'not_approved':
            return queryset.distinct().filter(approved=False)

class AuthorFilter(admin.SimpleListFilter):
    title = 'Author'
    parameter_name = 'XP Author'

    def lookups(self, request, model_admin):
        options = []
        for farmer in Farmer.objects.all().only('name').order_by('name'):
            options.append((farmer.name, farmer.name))
        return options

    def queryset(self, request, queryset):
        if self.value():
            return queryset.distinct().filter(farmer__name=self.value())

@admin.register(Experiment)
class ExperimentAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = ('name', 'author', 'xp_type', 'results', 'approved')
    list_filter = (ApprovalFilter, AuthorFilter)
    search_fields = ('name', )
    inlines = (ExperimentImageInline, ExperimentVideoInline)
    form = ExperimentForm

    def author(self, obj):
        return format_html('<a href="{0}">{1}</a>'.format('/admin/data/farmer/' + str(obj.farmer.id), obj.farmer.name))


class ExperimentInline(admin.TabularInline):
    model = Experiment
    show_change_link = True
    fields = ('name', 'approved', 'results')
    readonly_fields = ('name', 'approved', 'results')

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj):
        return False


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
        exclude = ('airtable_json', 'airtable_url', 'external_id', 'creation_date', 'user', 'livestock_type')
        model = Farmer
        widgets = {
            'name': forms.Textarea(attrs={'cols': 35, 'rows': 1}),
            'personnel': forms.Textarea(attrs={'cols': 35, 'rows': 1}),
            'livestock_number': forms.Textarea(attrs={'cols': 35, 'rows': 1}),
            'cultures': forms.Textarea(attrs={'cols': 55, 'rows': 3}),
            'soil_type': forms.Textarea(attrs={'cols': 35, 'rows': 1}),
            'description': forms.Textarea(attrs={'cols': 55, 'rows': 10}),
            'specificities': forms.Textarea(attrs={'cols': 55, 'rows': 5}),
            'surface': forms.Textarea(attrs={'cols': 35, 'rows': 1}),
            'surface_cultures': forms.Textarea(attrs={'cols': 35, 'rows': 1}),
            'surface_meadows': forms.Textarea(attrs={'cols': 35, 'rows': 1}),
            'output': forms.Textarea(attrs={'cols': 35, 'rows': 1}),
        }
        help_texts = {
            'email': 'Ce champ est utilisé pour le login',
        }
    def clean_email(self):
        if len(Farmer.objects.filter(email=self.data['email']).exclude(pk=self.instance.pk)) > 0:
            raise ValidationError('Another farmer already has this email', code='invalid')
        return self.cleaned_data['email']

@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = ('name', 'postal_code', 'email', 'approved')
    search_fields = ('name', 'email')
    list_filter = (ApprovalFilter, )
    inlines = (FarmImageInline, ExperimentInline)
    form = FarmerForm
