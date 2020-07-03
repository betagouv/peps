from django.contrib.sitemaps import Sitemap
from data.models import Farmer, Experiment

class FarmerSitemap(Sitemap):
    def items(self):
        return Farmer.objects.filter(approved=True)

    def location(self, obj):
        return obj.url_path

    def lastmod(self, obj):
        return obj.modification_date

    def changefreq(self, obj):
        return 'weekly'

    def priority(self, obj):
        return 0.5


class ExperimentSitemap(Sitemap):
    def items(self):
        return Experiment.objects.filter(approved=True)

    def location(self, obj):
        return obj.url_path

    def lastmod(self, obj):
        return obj.modification_date

    def changefreq(self, obj):
        return 'monthly'

    def priority(self, obj):
        return 0.6


class WebSitemap(Sitemap):
    def items(self):
        return [
            {
                'location': '/login',
                'changefreq': 'yearly',
                'priority': 0.4
            },
            {
                'location': '/register',
                'changefreq': 'yearly',
                'priority': 0.7
            },
            {
                'location': '/qui-sommes-nous',
                'changefreq': 'yearly',
                'priority': 0.3
            },
            {
                'location': '/contact',
                'changefreq': 'yearly',
                'priority': 0.3
            },
            {
                'location': '/conditions-generales-d-utilisation',
                'changefreq': 'yearly',
                'priority': 0.2
            },
            {
                'location': '/',
                'changefreq': 'daily',
                'priority': 1.0
            },
        ]
    def location(self, obj):
        return obj.get('location')

    def changefreq(self, obj):
        return obj.get('changefreq')

    def priority(self, obj):
        return obj.get('priority')
