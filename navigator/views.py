import json
import math
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import CareerTrack
from .services import (
    SUPPORTED_REGIONS,
    fetch_market_trends_with_cache,
    calculate_dss_matches
)

_CLAMP_MIN = 1.0
_CLAMP_MAX = 10.0


def _parse_clamped_float(raw_value, default):
    """Parse a string query param and clamp to [1.0, 10.0].

    Returns ``default`` only when the raw value is None (param absent).
    When present but non-numeric, returns ``default`` as well.
    Zero is treated as a numeric value and clamped to 1.0.
    """
    if raw_value is None:
        return default
    try:
        v = float(raw_value)
        if math.isnan(v) or math.isinf(v):
            return default
        return max(_CLAMP_MIN, min(_CLAMP_MAX, v))
    except (ValueError, TypeError):
        return default


@ensure_csrf_cookie
def index(request):
    selected_region = request.GET.get('region', 'global')
    if selected_region not in SUPPORTED_REGIONS:
        selected_region = 'global'

    market_trends = fetch_market_trends_with_cache(selected_region)
    tracks_count = CareerTrack.objects.count()

    initial_sliders = {
        'learning_curve': 5.0,
        'financial_vector': 7.0,
        'architecture_visual': 5.0,
        'company_scale': 6.0,
        'stress_wlb': 5.0,
    }

    context = {
        'regions': SUPPORTED_REGIONS,
        'current_region': selected_region,
        'market_trends': market_trends,
        'tracks_count': tracks_count,
        'initial_sliders': initial_sliders,
    }
    return render(request, 'index.html', context)


@ensure_csrf_cookie
def career_detail(request, slug):
    track = get_object_or_404(CareerTrack, slug=slug)
    selected_region = request.GET.get('region', 'global')
    if selected_region not in SUPPORTED_REGIONS:
        selected_region = 'global'

    raw_learn = request.GET.get('learn')
    raw_fin   = request.GET.get('fin')
    raw_arch  = request.GET.get('arch')
    raw_scale = request.GET.get('scale')
    raw_stress = request.GET.get('stress')

    have_all_params = all(p is not None for p in (raw_learn, raw_fin, raw_arch, raw_scale, raw_stress))

    user_params = {
        'learning_curve':      _parse_clamped_float(raw_learn,  None),
        'financial_vector':    _parse_clamped_float(raw_fin,    None),
        'architecture_visual': _parse_clamped_float(raw_arch,   None),
        'company_scale':       _parse_clamped_float(raw_scale,  None),
        'stress_wlb':          _parse_clamped_float(raw_stress, None),
    }

    user_match = None
    if have_all_params and all(v is not None for v in user_params.values()):
        ranked = calculate_dss_matches(user_params, region=selected_region)
        for r in ranked:
            if r['slug'] == slug:
                user_match = r
                break

    track_data = {
        'title': track.title,
        'radar': {
            'learning_curve':      float(track.radar_learning_curve),
            'financial_vector':    float(track.radar_financial_vector),
            'architecture_visual': float(track.radar_architecture_visual),
            'company_scale':       float(track.radar_company_scale),
            'stress_wlb':          float(track.radar_stress_wlb),
        },
        'user_vector': {
            'learning_curve':      user_params['learning_curve'],
            'financial_vector':    user_params['financial_vector'],
            'architecture_visual': user_params['architecture_visual'],
            'company_scale':       user_params['company_scale'],
            'stress_wlb':          user_params['stress_wlb'],
        },
    }

    context = {
        'track': track,
        'salaries': track.salaries,
        'market_stats': track.market_stats,
        'tech_stack': track.tech_stack,
        'pros': track.pros,
        'cons': track.cons,
        'roadmap': track.roadmap,
        'regions': SUPPORTED_REGIONS,
        'current_region': selected_region,
        'user_params': user_params,
        'user_match': user_match,
        'track_data': track_data,
    }
    return render(request, 'results.html', context)


def api_match(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed.'}, status=405)

    try:
        body = request.body
        if not body:
            return JsonResponse({'status': 'error', 'message': 'Empty request body.'}, status=400)
        data = json.loads(body.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        return JsonResponse({'status': 'error', 'message': f'Invalid JSON: {exc}'}, status=400)

    if not isinstance(data, dict):
        return JsonResponse(
            {'status': 'error', 'message': 'Request body must be a JSON object, not a list or scalar.'},
            status=400
        )

    sliders = data.get('sliders', {})
    if not isinstance(sliders, dict):
        return JsonResponse(
            {'status': 'error', 'message': '"sliders" must be a JSON object.'},
            status=400
        )

    region = data.get('region', 'global')
    if region not in SUPPORTED_REGIONS:
        region = 'global'

    try:
        ranked_tracks = calculate_dss_matches(sliders, region=region)
    except (ValueError, TypeError) as exc:
        return JsonResponse({'status': 'error', 'message': str(exc)}, status=400)

    top_3 = ranked_tracks[:3]
    trends = fetch_market_trends_with_cache(region)

    return JsonResponse({
        'status': 'success',
        'region': region,
        'currency_symbol': SUPPORTED_REGIONS[region]['symbol'],
        'top_matches': top_3,
        'all_matches': ranked_tracks,
        'trends': trends,
    })


def api_trends(request):
    region = request.GET.get('region', 'global')
    if region not in SUPPORTED_REGIONS:
        region = 'global'

    trends = fetch_market_trends_with_cache(region)
    return JsonResponse({
        'status': 'success',
        'region': region,
        'trends': trends,
        'meta': SUPPORTED_REGIONS.get(region, SUPPORTED_REGIONS['global']),
    })
