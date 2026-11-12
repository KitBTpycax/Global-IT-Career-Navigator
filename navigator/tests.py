import json
import math
from datetime import timedelta
from unittest.mock import patch, MagicMock

from django.test import TestCase, Client, override_settings
from django.utils import timezone

from navigator.models import CareerTrack, MarketCache
from navigator.services import (
    DEFAULT_MARKET_SNAPSHOT,
    SUPPORTED_REGIONS,
    calculate_dss_matches,
    fetch_market_trends_with_cache,
    parse_and_clamp_axis,
    MAX_EUCLIDEAN_DISTANCE,
)


def _make_track(**kwargs):
    defaults = dict(
        slug='test-track',
        title='Test Track',
        tagline='A test tagline',
        category='Backend',
        icon_type='server',
        badge_color='emerald',
        radar_learning_curve=5.0,
        radar_financial_vector=5.0,
        radar_architecture_visual=5.0,
        radar_company_scale=5.0,
        radar_stress_wlb=5.0,
        short_desc='Short description.',
        full_desc='Full description.',
        salaries={
            'global': {'junior': '$30,000', 'middle': '$60,000', 'senior': '$90,000', 'lead': '$120,000'},
        },
        market_stats={'demand_index': 80, 'remote_share': '70%', 'yoy_growth': '+10%', 'open_vacancies_est': '10,000+'},
        tech_stack=['Python', 'Django'],
        pros=['Pro 1'],
        cons=['Con 1'],
        roadmap=[{'phase': 'Phase 1', 'duration': '4 weeks', 'topics': ['Topic A']}],
    )
    defaults.update(kwargs)
    return CareerTrack.objects.create(**defaults)


class ParseClampAxisTests(TestCase):
    def test_clamps_below_min(self):
        self.assertEqual(parse_and_clamp_axis(0, 'x'), 1.0)

    def test_clamps_above_max(self):
        self.assertEqual(parse_and_clamp_axis(11, 'x'), 10.0)

    def test_valid_mid(self):
        self.assertAlmostEqual(parse_and_clamp_axis('7.5', 'x'), 7.5)

    def test_non_numeric_raises(self):
        with self.assertRaises(ValueError):
            parse_and_clamp_axis('abc', 'x')

    def test_none_raises(self):
        with self.assertRaises((ValueError, TypeError)):
            parse_and_clamp_axis(None, 'x')


class DSSMatchingTests(TestCase):
    """Tests for the Weighted Euclidean Distance DSS ranking."""

    def setUp(self):
        MarketCache.objects.create(region='global', payload=DEFAULT_MARKET_SNAPSHOT['global'])

        self.frontend = _make_track(
            slug='frontend', title='Frontend Dev', category='Frontend',
            radar_learning_curve=4.0, radar_financial_vector=7.0,
            radar_architecture_visual=9.0, radar_company_scale=6.0, radar_stress_wlb=4.0,
        )
        self.devops = _make_track(
            slug='devops', title='DevOps Engineer', category='DevOps',
            radar_learning_curve=8.0, radar_financial_vector=9.5,
            radar_architecture_visual=2.0, radar_company_scale=5.0, radar_stress_wlb=7.5,
        )
        self.qa = _make_track(
            slug='qa', title='QA Engineer', category='QA',
            radar_learning_curve=3.0, radar_financial_vector=5.0,
            radar_architecture_visual=3.5, radar_company_scale=3.0, radar_stress_wlb=2.5,
        )

    def test_closest_track_ranks_first(self):
        user_vector = {
            'learning_curve': 4.0, 'financial_vector': 7.0,
            'architecture_visual': 9.0, 'company_scale': 6.0, 'stress_wlb': 4.0,
        }
        results = calculate_dss_matches(user_vector, region='global')
        self.assertEqual(results[0]['slug'], 'frontend')

    def test_devops_wins_for_devops_profile(self):
        user_vector = {
            'learning_curve': 8.0, 'financial_vector': 9.5,
            'architecture_visual': 1.5, 'company_scale': 4.0, 'stress_wlb': 7.5,
        }
        results = calculate_dss_matches(user_vector, region='global')
        self.assertEqual(results[0]['slug'], 'devops')

    def test_sorted_by_raw_distance_ascending(self):
        user_vector = {'learning_curve': 5.0, 'financial_vector': 5.0,
                       'architecture_visual': 5.0, 'company_scale': 5.0, 'stress_wlb': 5.0}
        results = calculate_dss_matches(user_vector, region='global')
        distances = [r['raw_distance'] for r in results]
        self.assertEqual(distances, sorted(distances))

    def test_match_percentage_in_range(self):
        user_vector = {'learning_curve': 5.0, 'financial_vector': 5.0,
                       'architecture_visual': 5.0, 'company_scale': 5.0, 'stress_wlb': 5.0}
        results = calculate_dss_matches(user_vector, region='global')
        for r in results:
            self.assertGreaterEqual(r['match_percentage'], 0.0)
            self.assertLessEqual(r['match_percentage'], 100.0)

    def test_perfect_match_produces_max_score(self):
        user_vector = {
            'learning_curve': self.frontend.radar_learning_curve,
            'financial_vector': self.frontend.radar_financial_vector,
            'architecture_visual': self.frontend.radar_architecture_visual,
            'company_scale': self.frontend.radar_company_scale,
            'stress_wlb': self.frontend.radar_stress_wlb,
        }
        results = calculate_dss_matches(user_vector, region='global')
        top = results[0]
        self.assertEqual(top['slug'], 'frontend')
        self.assertAlmostEqual(top['raw_distance'], 0.0, places=4)
        self.assertAlmostEqual(top['match_percentage'], 100.0, places=1)

    def test_non_dict_user_vector_raises(self):
        with self.assertRaises((ValueError, TypeError)):
            calculate_dss_matches([5.0, 5.0, 5.0, 5.0, 5.0], region='global')

    def test_string_slider_value_clamped_not_crashed(self):
        user_vector = {'learning_curve': '7', 'financial_vector': '8',
                       'architecture_visual': '5', 'company_scale': '6', 'stress_wlb': '4'}
        results = calculate_dss_matches(user_vector, region='global')
        self.assertGreater(len(results), 0)

    def test_zero_clamped_to_one(self):
        user_vector = {'learning_curve': 0, 'financial_vector': 0,
                       'architecture_visual': 0, 'company_scale': 0, 'stress_wlb': 0}
        results = calculate_dss_matches(user_vector, region='global')
        self.assertGreater(len(results), 0)
        for r in results:
            self.assertGreaterEqual(r['match_percentage'], 0.0)


class ApiMatchViewTests(TestCase):
    """Tests for /api/match/ hardening: CSRF, validation, and error codes."""

    def setUp(self):
        MarketCache.objects.create(region='global', payload=DEFAULT_MARKET_SNAPSHOT['global'])
        self.track = _make_track()

    def _post_json(self, payload, enforce_csrf=False):
        client = Client(enforce_csrf_checks=enforce_csrf)
        return client.post(
            '/api/match/',
            data=json.dumps(payload),
            content_type='application/json',
        )

    def test_valid_post_returns_200(self):
        payload = {
            'sliders': {'learning_curve': 5, 'financial_vector': 5,
                        'architecture_visual': 5, 'company_scale': 5, 'stress_wlb': 5},
            'region': 'global',
        }
        response = self._post_json(payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('top_matches', data)

    def test_list_body_returns_400(self):
        response = self._post_json([1, 2, 3])
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json()['status'])

    def test_string_body_returns_400(self):
        client = Client()
        response = client.post(
            '/api/match/',
            data='"abc"',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)

    def test_invalid_json_returns_400(self):
        client = Client()
        response = client.post(
            '/api/match/',
            data='{not valid json}',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)

    def test_sliders_as_list_returns_400(self):
        response = self._post_json({'sliders': [1, 2, 3], 'region': 'global'})
        self.assertEqual(response.status_code, 400)

    def test_non_numeric_slider_value_returns_400(self):
        response = self._post_json({
            'sliders': {'learning_curve': 'abc', 'financial_vector': 5,
                        'architecture_visual': 5, 'company_scale': 5, 'stress_wlb': 5},
            'region': 'global',
        })
        self.assertEqual(response.status_code, 400)

    def test_get_method_returns_405(self):
        response = self.client.get('/api/match/')
        self.assertEqual(response.status_code, 405)

    def test_csrf_required_without_token(self):
        client = Client(enforce_csrf_checks=True)
        payload = {
            'sliders': {'learning_curve': 5, 'financial_vector': 5,
                        'architecture_visual': 5, 'company_scale': 5, 'stress_wlb': 5},
            'region': 'global',
        }
        response = client.post(
            '/api/match/',
            data=json.dumps(payload),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 403)

    def test_empty_sliders_dict_still_returns_200(self):
        response = self._post_json({'sliders': {}, 'region': 'global'})
        self.assertEqual(response.status_code, 200)


class IndexViewTests(TestCase):
    def setUp(self):
        MarketCache.objects.create(region='global', payload=DEFAULT_MARKET_SNAPSHOT['global'])
        _make_track()

    def test_index_returns_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_index_contains_initial_sliders_json_script(self):
        response = self.client.get('/')
        self.assertContains(response, 'id="initial-sliders-data"')

    def test_index_initial_sliders_valid_json(self):
        response = self.client.get('/')
        content = response.content.decode('utf-8')
        start = content.find('id="initial-sliders-data"')
        self.assertGreater(start, -1)
        tag_start = content.rfind('<script', 0, start)
        tag_end = content.find('</script>', start) + len('</script>')
        script_block = content[tag_start:tag_end]
        json_start = script_block.index('>') + 1
        json_end = script_block.rindex('<')
        parsed = json.loads(script_block[json_start:json_end])
        self.assertIn('learning_curve', parsed)
        self.assertIn('financial_vector', parsed)

    def test_index_region_filter(self):
        MarketCache.objects.create(region='usa', payload=DEFAULT_MARKET_SNAPSHOT['usa'])
        response = self.client.get('/?region=usa')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['current_region'], 'usa')

    def test_invalid_region_falls_back_to_global(self):
        response = self.client.get('/?region=invalid_xyz')
        self.assertEqual(response.context['current_region'], 'global')


class DetailViewTests(TestCase):
    """Tests for /career/<slug>/ including json_script float safety."""

    def setUp(self):
        MarketCache.objects.create(region='global', payload=DEFAULT_MARKET_SNAPSHOT['global'])
        self.track = _make_track(
            slug='python-backend',
            title='Python Backend Engineer',
            radar_learning_curve=5.5,
            radar_financial_vector=8.5,
            radar_architecture_visual=2.0,
            radar_company_scale=5.0,
            radar_stress_wlb=5.0,
        )

    def test_detail_page_returns_200(self):
        response = self.client.get('/career/python-backend/')
        self.assertEqual(response.status_code, 200)

    def test_detail_contains_json_script_tag(self):
        response = self.client.get('/career/python-backend/')
        self.assertContains(response, 'id="detail-track-data"')

    def test_detail_track_data_is_valid_json_no_comma_decimals(self):
        """
        CRITICAL: Under LANGUAGE_CODE='uk', Django would format 5.5 as '5,5'
        inside a raw <script> tag. json_script must produce '5.5' (dot notation).
        """
        response = self.client.get('/career/python-backend/')
        content = response.content.decode('utf-8')

        start = content.find('id="detail-track-data"')
        self.assertGreater(start, -1, "detail-track-data script tag not found")

        tag_start = content.rfind('<script', 0, start)
        tag_end   = content.find('</script>', start) + len('</script>')
        script_block = content[tag_start:tag_end]

        json_start = script_block.index('>') + 1
        json_end   = script_block.rindex('<')
        raw_json   = script_block[json_start:json_end]

        parsed = json.loads(raw_json)
        self.assertIn('radar', parsed)
        self.assertAlmostEqual(parsed['radar']['learning_curve'], 5.5, places=4)
        self.assertAlmostEqual(parsed['radar']['financial_vector'], 8.5, places=4)

    def test_detail_with_query_params_clamps_zero_to_one(self):
        response = self.client.get('/career/python-backend/?learn=0&fin=5&arch=5&scale=5&stress=5')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        start = content.find('id="detail-track-data"')
        tag_start = content.rfind('<script', 0, start)
        tag_end   = content.find('</script>', start) + len('</script>')
        script_block = content[tag_start:tag_end]
        json_start   = script_block.index('>') + 1
        json_end     = script_block.rindex('<')
        parsed = json.loads(script_block[json_start:json_end])
        lc = parsed['user_vector']['learning_curve']
        self.assertIsNotNone(lc, "learning_curve should not be null when ?learn=0 is passed")
        self.assertGreaterEqual(lc, 1.0, "learning_curve=0 must be clamped to 1.0")

    def test_detail_no_params_user_vector_all_null(self):
        response = self.client.get('/career/python-backend/')
        content = response.content.decode('utf-8')
        start = content.find('id="detail-track-data"')
        tag_start = content.rfind('<script', 0, start)
        tag_end   = content.find('</script>', start) + len('</script>')
        script_block = content[tag_start:tag_end]
        json_start   = script_block.index('>') + 1
        json_end     = script_block.rindex('<')
        parsed = json.loads(script_block[json_start:json_end])
        for axis in ('learning_curve', 'financial_vector', 'architecture_visual', 'company_scale', 'stress_wlb'):
            self.assertIsNone(parsed['user_vector'][axis],
                              f"user_vector.{axis} should be null when no query params provided")

    def test_detail_404_on_missing_slug(self):
        response = self.client.get('/career/nonexistent-slug/')
        self.assertEqual(response.status_code, 404)


class MarketCacheTTLTests(TestCase):
    """Tests for shared 6-hour Remotive TTL cache, Counter category extraction, and failure backoff."""

    def setUp(self):
        MarketCache.objects.all().delete()

    @patch('navigator.services.requests.get')
    def test_live_api_called_when_no_cache_exists(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            'total-job-count': 310,
            'jobs': [
                {'category': 'Design'},
                {'category': 'DevOps / Sysadmin'},
                {'category': 'DevOps / Sysadmin'},
            ],
        }
        mock_get.return_value = mock_resp

        result = fetch_market_trends_with_cache('global')

        mock_get.assert_called_once()
        self.assertTrue(result['is_live'])
        self.assertEqual(result['source_url'], 'https://remotive.com')
        self.assertEqual(result['hot_skill'], 'DevOps / Sysadmin (Top in Remotive Feed)')
        self.assertIn('310', result['active_vacancies'])

    @patch('navigator.services.requests.get')
    def test_shared_global_cache_reused_across_regions_within_ttl(self, mock_get):
        MarketCache.objects.create(
            region='remotive_global_feed',
            payload={
                'live_count': 250,
                'top_category': 'Software Development',
                'is_live': True,
            },
        )

        global_res = fetch_market_trends_with_cache('global')
        ukraine_res = fetch_market_trends_with_cache('ukraine')

        mock_get.assert_not_called()
        self.assertTrue(global_res['is_live'])
        self.assertTrue(ukraine_res['is_live'])
        self.assertEqual(ukraine_res['hot_skill'], 'Software Development (Top in Remotive Feed)')
        self.assertEqual(ukraine_res['remote_share'], DEFAULT_MARKET_SNAPSHOT['ukraine']['remote_share'])

    @patch('navigator.services.requests.get')
    def test_api_called_when_cache_is_stale(self, mock_get):
        entry = MarketCache.objects.create(
            region='remotive_global_feed',
            payload={'live_count': 100, 'top_category': 'QA', 'is_live': True},
        )
        stale_time = timezone.now() - timedelta(hours=7)
        MarketCache.objects.filter(pk=entry.pk).update(updated_at=stale_time)

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {'jobs': [{'category': 'AI / ML'}], 'total-job-count': 42}
        mock_get.return_value = mock_resp

        result = fetch_market_trends_with_cache('global')

        mock_get.assert_called_once()
        self.assertTrue(result['is_live'])
        self.assertEqual(result['hot_skill'], 'AI / ML (Top in Remotive Feed)')

    @patch('navigator.services.requests.get')
    def test_fallback_on_api_error_touches_cache_to_avoid_repeated_timeouts(self, mock_get):
        mock_get.side_effect = Exception('Network timeout')

        first = fetch_market_trends_with_cache('usa')
        second = fetch_market_trends_with_cache('ukraine')

        mock_get.assert_called_once()
        self.assertFalse(first['is_live'])
        self.assertFalse(second['is_live'])
        self.assertEqual(first['active_vacancies'], DEFAULT_MARKET_SNAPSHOT['usa']['active_vacancies'])
        self.assertEqual(second['demand_index'], DEFAULT_MARKET_SNAPSHOT['ukraine']['demand_index'])

    @patch('navigator.services.requests.get')
    def test_no_extra_db_writes_on_cache_hit(self, mock_get):
        entry = MarketCache.objects.create(
            region='remotive_global_feed',
            payload={'live_count': 180, 'top_category': 'Backend', 'is_live': True},
        )
        updated_at_before = MarketCache.objects.get(pk=entry.pk).updated_at

        fetch_market_trends_with_cache('global')
        fetch_market_trends_with_cache('europe')

        mock_get.assert_not_called()
        updated_at_after = MarketCache.objects.get(pk=entry.pk).updated_at
        self.assertEqual(updated_at_before, updated_at_after)
        