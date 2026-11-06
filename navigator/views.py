import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CareerTrack
from .services import (
    SUPPORTED_REGIONS,
    fetch_market_trends_with_cache,
    calculate_dss_matches
)

def index(request):
    selected_region = request.GET.get('region', 'global')
    if selected_region not in SUPPORTED_REGIONS:
        selected_region = 'global'

    market_trends = fetch_market_trends_with_cache(selected_region)
    tracks_count = CareerTrack.objects.count()

    context = {
        'regions': SUPPORTED_REGIONS,
        'current_region': selected_region,
        'market_trends': market_trends,
        'tracks_count': tracks_count
    }
    return render(request, 'index.html', context)

def career_detail(request, slug):
    track = get_object_or_404(CareerTrack, slug=slug)
    selected_region = request.GET.get('region', 'global')
    if selected_region not in SUPPORTED_REGIONS:
        selected_region = 'global'

    def parse_float(val):
        try:
            return float(val) if val is not None else None
        except (ValueError, TypeError):
            return None

    user_params = {
        'learning_curve': parse_float(request.GET.get('learn')),
        'financial_vector': parse_float(request.GET.get('fin')),
        'architecture_visual': parse_float(request.GET.get('arch')),
        'company_scale': parse_float(request.GET.get('scale')),
        'stress_wlb': parse_float(request.GET.get('stress'))
    }

    user_match = None
    if all(v is not None for v in user_params.values()):
        ranked = calculate_dss_matches(user_params, region=selected_region)
        for r in ranked:
            if r['slug'] == slug:
                user_match = r
                break

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
        'user_match': user_match
    }
    return render(request, 'results.html', context)

@csrf_exempt
def api_match(request):
    if request.method == 'POST':
        try:
            if request.body:
                data = json.loads(request.body.decode('utf-8'))
            else:
                data = request.POST.dict()
        except Exception:
            data = {}
    else:
        data = request.GET.dict()

    sliders = data.get('sliders', {})
    region = data.get('region', 'global')
    if region not in SUPPORTED_REGIONS:
        region = 'global'

    ranked_tracks = calculate_dss_matches(sliders, region=region)
    top_3 = ranked_tracks[:3]
    trends = fetch_market_trends_with_cache(region)

    return JsonResponse({
        'status': 'success',
        'region': region,
        'currency_symbol': SUPPORTED_REGIONS[region]['symbol'],
        'top_matches': top_3,
        'all_matches': ranked_tracks,
        'trends': trends
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
        'meta': SUPPORTED_REGIONS.get(region, SUPPORTED_REGIONS['global'])
    })
