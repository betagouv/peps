from django.contrib import admin
from django.utils.html import format_html
from data.models import DiscardAction, GroupCount, RefererCount

@admin.register(DiscardAction)
class DiscardActionAdmin(admin.ModelAdmin):
    list_display = ('creation_date', 'url_field', 'reason')

    def url_field(self, obj):
        return format_html('<a href="{0}" target="_blank">{1}</a>'.format(obj.airtable_url, obj.practice_airtable_id))

@admin.register(GroupCount)
class GroupCountAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'counter')

@admin.register(RefererCount)
class RefererCountAdmin(admin.ModelAdmin):
    list_display = ('referer_name', 'counter')
