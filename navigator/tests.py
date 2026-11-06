import json
from django.test import TestCase, Client
from navigator.models import CareerTrack, MarketCache
from navigator.services import DEFAULT_MARKET_SNAPSHOT

class NavigatorTests(TestCase):
    def setUp(self):
        CareerTrack.objects.create(
            slug="python-backend",
            title="Python Backend Engineer",
            tagline="Серце серверної архітектури",
            category="Backend & Cloud",
            icon_type="server",
            badge_color="emerald",
            radar_learning_curve=5.5,
            radar_financial_vector=8.5,
            radar_architecture_visual=2.0,
            radar_company_scale=5.0,
            radar_stress_wlb=5.0,
            short_desc="Проектування API",
            full_desc="Детальний опис",
            salaries={"global": {"junior": "$35,000", "senior": "$110,000"}},
            market_stats={"demand_index": 91, "remote_share": "82%", "yoy_growth": "+15.8%", "open_vacancies_est": "45,000+"},
            tech_stack=["Python", "FastAPI"],
            pros=["Чистий синтаксис"],
            cons=["Конкуренція"],
            roadmap=[{"phase": "Фаза 1", "duration": "4 тижні", "topics": ["Основи"]}]
        )
        MarketCache.objects.create(
            region="global",
            payload=DEFAULT_MARKET_SNAPSHOT["global"]
        )

    def test_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Кар\'єрний')

    def test_detail_page(self):
        response = self.client.get('/career/python-backend/?learn=6&fin=8&arch=2&scale=5&stress=5')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Python Backend Engineer')

    def test_api_match(self):
        payload = {
            'sliders': {
                'learning_curve': 6,
                'financial_vector': 8,
                'architecture_visual': 2,
                'company_scale': 5,
                'stress_wlb': 5
            },
            'region': 'global'
        }
        response = self.client.post(
            '/api/match/',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertTrue(len(data['top_matches']) > 0)
        self.assertEqual(data['top_matches'][0]['slug'], 'python-backend')

    def test_api_trends(self):
        response = self.client.get('/api/trends/?region=global')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
