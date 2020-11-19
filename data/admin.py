from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from django.core.exceptions import ValidationError
from data.models import Experiment, Farmer, ExperimentImage, ExperimentVideo, FarmImage
from data.models import CULTURES, Theme

admin.site.site_header = 'Administration Peps'

class ExperimentImageForm(forms.ModelForm):
    class Meta:
        model = ExperimentImage
        exclude = []
        widgets = {
            'label': forms.Textarea(attrs={'cols': 35, 'rows': 1}),
            'copyright': forms.Textarea(attrs={'cols': 35, 'rows': 1}),
        }

class ExperimentImageInline(admin.TabularInline):
    model = ExperimentImage
    form = ExperimentImageForm
    extra = 0
    fields = ('image', 'label', 'copyright')


class ExperimentVideoForm(forms.ModelForm):
    class Meta:
        model = ExperimentVideo
        exclude = []
        widgets = {
            'label': forms.Textarea(attrs={'cols': 35, 'rows': 1}),
            'copyright': forms.Textarea(attrs={'cols': 35, 'rows': 1}),
        }

class ExperimentVideoInline(admin.TabularInline):
    model = ExperimentVideo
    form = ExperimentVideoForm
    extra = 0
    fields = ('video', 'label', 'copyright')


class ExperimentForm(forms.ModelForm):
    class Meta:
        exclude = [
            'id',
            'sequence_number',
            'external_id',
            'modification_date',
            'airtable_json',
            'airtable_url',
            'creation_date',
        ]
        model = Experiment

        widgets = {
            'name': forms.Textarea(attrs={'cols': 35, 'rows': 1}),
            'short_name': forms.Textarea(attrs={'cols': 25, 'rows': 1}),
            'objectives': forms.Textarea(attrs={'cols': 55, 'rows': 2}),
            'equipment': forms.Textarea(attrs={'cols': 35, 'rows': 1}),
            'results_details': forms.Textarea(attrs={'cols': 55, 'rows': 6}),
            'description': forms.Textarea(attrs={'cols': 55, 'rows': 8}),
            'investment': forms.Textarea(attrs={'cols': 55, 'rows': 2}),
            'surface': forms.Textarea(attrs={'cols': 35, 'rows': 1}),
            'cultures': forms.CheckboxSelectMultiple(choices=CULTURES),
        }

class StateFilter(admin.SimpleListFilter):
    title = 'State'
    parameter_name = ''

    def lookups(self, request, model_admin):
        return [
            ("Brouillon", "Brouillon"),
            ("En attente de validation", "En attente de validation"),
            ("Validé", "Validé"),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.distinct().filter(state=self.value())


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

class ThemeInline(admin.TabularInline):
    model = Experiment.theme_set.through
    extra = 0

@admin.register(Experiment)
class ExperimentAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = ('name', 'author', 'xp_type', 'results', 'icon_state')
    list_filter = (StateFilter, AuthorFilter)
    search_fields = ('name', )
    readonly_fields = ('html_link', )

    fieldsets = (
        ('', {
            'fields': (
                'html_link',
                'state',
                'farmer',
                'name',
                'short_name',
                'xp_type',
                'objectives',
                'tags',
                'ongoing',
                'investment',
                'equipment',
                'description',
                'surface_type',
                'surface',
                'control_presence',
                'results',
                'results_details',
                'links',
            )
        }),
        ('Cultures', {
            'classes': ('collapse',),
            'fields': (
                'cultures',
            )
        }),
    )
    inlines = (ThemeInline, ExperimentImageInline, ExperimentVideoInline, )
    form = ExperimentForm

    def author(self, obj):
        return format_html('<a href="{0}">{1}</a>'.format('/admin/data/farmer/' + str(obj.farmer.id), obj.farmer.name))

    def icon_state(self, obj):
        if obj.state == "Brouillon":
            return format_html('<img src="/static/admin/img/icon-no.svg" alt="True">')
        elif obj.state == "En attente de validation":
            return format_html('<img src="/static/images/icon-bang.svg" alt="True">')
        elif obj.state == "Validé":
            return format_html('<img src="/static/admin/img/icon-yes.svg" alt="True">')
        else:
            return obj.state

    icon_state.allow_tags = True
    icon_state.short_description = 'State'


class ExperimentInline(admin.TabularInline):
    model = Experiment
    show_change_link = True
    fields = ('name', 'approved', 'results')
    readonly_fields = ('name', 'approved', 'results')
    extra = 0

    def has_add_permission(self, request, obj):
        return False


class AddExperimentInline(admin.TabularInline):
    model = Experiment
    # show_change_link = True
    fields = ('name', 'description', 'results')
    extra = 0

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'name':
            kwargs['widget'] = forms.Textarea(attrs={'cols': 35, 'rows': 1})
        return super(AddExperimentInline, self).formfield_for_dbfield(db_field, request, **kwargs)

    def has_change_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return False


class FarmImageForm(forms.ModelForm):
    class Meta:
        model = FarmImage
        exclude = []
        widgets = {
            'label': forms.Textarea(attrs={'cols': 35, 'rows': 1}),
            'copyright': forms.Textarea(attrs={'cols': 35, 'rows': 1}),
        }

class FarmImageInline(admin.TabularInline):
    model = FarmImage
    form = FarmImageForm
    extra = 0
    fields = ('image', 'label', 'copyright')

class FarmerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        instance = kwargs['instance'] if 'instance' in kwargs else None
        if 'initial' not in kwargs:
            kwargs['initial'] = {}
        if 'lat' not in kwargs['initial']:
            lat = instance.lat if instance and instance.lat else 0.0
            kwargs['initial'].update({'lat': lat})
        if 'lon' not in kwargs['initial']:
            lon = instance.lon if instance and instance.lon else 0.0
            kwargs['initial'].update({'lon': lon})
        super(FarmerForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Farmer
        exclude = ('airtable_json', 'airtable_url', 'external_id', 'creation_date', 'user', 'livestock_type')
        widgets = {
            'name': forms.Textarea(attrs={'cols': 35, 'rows': 1}),
            'farm_name': forms.Textarea(attrs={'cols': 35, 'rows': 1}),
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
    list_display = ('name', 'postal_code', 'email', 'approved', 'creation_date')
    search_fields = ('name', 'email')
    readonly_fields = ('self_created', 'html_link', )
    fieldsets = (
        ('', {
            'fields': (
                'self_created',
                'html_link',
                'approved',
                'cgu_approved',
                'can_send_messages',
            )
        }),
        ('Informations Personnelles', {
            'fields': (
                'name',
                'email',
                'phone_number',
                'profile_image',
                'contact_possible',
                'email_for_messages_allowed',
                'groups',
            )
        }),
        ('L\'exploitation', {
            'fields': (
                'farm_name',
                'production',
                'installation_date',
                'postal_code',
                'lat',
                'lon',
                'personnel',
                'surface',
                'surface_cultures',
                'surface_meadows',
                'livestock_types',
                'livestock_number',
                'cultures',
                'soil_type',
                'output',
                'description',
                'specificities',
                'agriculture_types',
                'links',
            )
        }),
    )
    list_filter = (ApprovalFilter, )
    inlines = (FarmImageInline, ExperimentInline, AddExperimentInline)
    form = FarmerForm

class ThemeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['experiments'].queryset = Experiment.objects.order_by('name')

    class Meta:
        model = Theme
        exclude = []
        widgets = {
            'name': forms.Textarea(attrs={'cols': 35, 'rows': 1}),
            'copyright': forms.Textarea(attrs={'cols': 35, 'rows': 1}),
            'description': forms.Textarea(attrs={'cols': 55, 'rows': 8}),
        }

@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'creation_date')
    form = ThemeForm
    search_fields = ('name', )
    readonly_fields = ('creation_date', 'modification_date', 'html_link', )
    filter_vertical = ('experiments', )
    fields = (
        'html_link',
        'active',
        'name',
        'image',
        'copyright',
        'description',
        'experiments',
    )

