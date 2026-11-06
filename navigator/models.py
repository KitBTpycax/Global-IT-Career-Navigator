from django.db import models

class CareerTrack(models.Model):
    slug = models.SlugField(max_length=64, unique=True, db_index=True)
    title = models.CharField(max_length=128)
    tagline = models.CharField(max_length=256)
    category = models.CharField(max_length=64)
    icon_type = models.CharField(max_length=32, default='code')
    badge_color = models.CharField(max_length=32, default='cyan')

    radar_learning_curve = models.FloatField()
    radar_financial_vector = models.FloatField()
    radar_architecture_visual = models.FloatField()
    radar_company_scale = models.FloatField()
    radar_stress_wlb = models.FloatField()

    short_desc = models.TextField()
    full_desc = models.TextField()
    salaries = models.JSONField(default=dict)
    market_stats = models.JSONField(default=dict)
    tech_stack = models.JSONField(default=list)
    pros = models.JSONField(default=list)
    cons = models.JSONField(default=list)
    roadmap = models.JSONField(default=list)

    class Meta:
        verbose_name = 'Кар\'єрний трек'
        verbose_name_plural = 'Кар\'єрні треки'
        ordering = ['title']

    def __str__(self):
        return self.title

    def to_dict(self, region='global'):
        regional_salary = self.salaries.get(region, self.salaries.get('global', {}))
        return {
            'id': self.id,
            'slug': self.slug,
            'title': self.title,
            'tagline': self.tagline,
            'category': self.category,
            'icon_type': self.icon_type,
            'badge_color': self.badge_color,
            'radar_profile': {
                'learning_curve': self.radar_learning_curve,
                'financial_vector': self.radar_financial_vector,
                'architecture_visual': self.radar_architecture_visual,
                'company_scale': self.radar_company_scale,
                'stress_wlb': self.radar_stress_wlb
            },
            'short_desc': self.short_desc,
            'regional_salary': regional_salary,
            'all_salaries': self.salaries,
            'market_stats': self.market_stats,
            'tech_stack': self.tech_stack,
            'pros': self.pros,
            'cons': self.cons,
            'roadmap': self.roadmap
        }


class MarketCache(models.Model):
    region = models.CharField(max_length=32, unique=True, db_index=True)
    payload = models.JSONField(default=dict)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Кеш трендів ринку'
        verbose_name_plural = 'Кеш трендів ринку'

    def __str__(self):
        return f"{self.region} ({self.updated_at:%Y-%m-%d %H:%M})"
