import os
import math
from datetime import timedelta
import requests
from django.utils import timezone
from .models import CareerTrack, MarketCache

SUPPORTED_REGIONS = {
    'global': {'name': 'Global (Світовий ринок)', 'currency': 'USD', 'symbol': '$'},
    'usa': {'name': 'USA (Північна Америка)', 'currency': 'USD', 'symbol': '$'},
    'europe': {'name': 'Europe (ЄС та Швейцарія)', 'currency': 'EUR', 'symbol': '€'},
    'uk': {'name': 'United Kingdom (Британія)', 'currency': 'GBP', 'symbol': '£'},
    'ukraine': {'name': 'Ukraine (Український IT-хаб)', 'currency': 'USD', 'symbol': '$'}
}

DEFAULT_MARKET_SNAPSHOT = {
    'global': {
        'active_vacancies': '320,000+',
        'demand_index': 92,
        'remote_share': '74%',
        'avg_growth': '+16.4%',
        'hot_skill': 'AI/ML Integration & Kubernetes',
        'market_sentiment': 'Високий попит на Senior спеціалістів із мультистеком та розумінням бізнес-домену.',
        'top_hiring_segments': ['Cloud Computing', 'AI Platforms', 'Fintech', 'Cybersecurity'],
        'is_live': False,
        'feed_source': 'Regional Reference Benchmark',
        'feed_status': 'Reference Baseline'
    },
    'usa': {
        'active_vacancies': '145,000+',
        'demand_index': 95,
        'remote_share': '68%',
        'avg_growth': '+18.2%',
        'hot_skill': 'LLM Fine-tuning & Distributed Systems',
        'market_sentiment': 'Активна реструктуризація в сторону AI-native розробників та інфраструктурних інженерів.',
        'top_hiring_segments': ['Enterprise SaaS', 'HealthTech', 'Defense & GovTech', 'AI Infrastructure'],
        'is_live': False,
        'feed_source': 'Regional Reference Benchmark',
        'feed_status': 'Reference Baseline'
    },
    'europe': {
        'active_vacancies': '85,000+',
        'demand_index': 88,
        'remote_share': '71%',
        'avg_growth': '+12.8%',
        'hot_skill': 'Data Governance, Rust & Microservices',
        'market_sentiment': 'Стабільний попит з фокусом на WLB, кібербезпеку (NIS2) та відповідність GDPR.',
        'top_hiring_segments': ['Automotive Tech', 'CleanTech', 'Fintech & Neobanks', 'GovTech'],
        'is_live': False,
        'feed_source': 'Regional Reference Benchmark',
        'feed_status': 'Reference Baseline'
    },
    'uk': {
        'active_vacancies': '42,000+',
        'demand_index': 87,
        'remote_share': '65%',
        'avg_growth': '+11.5%',
        'hot_skill': 'Cloud Architecture & Event-Driven Systems',
        'market_sentiment': 'Лондон зберігає лідерство у фінтеху та інвестиціях в AI-стартапи.',
        'top_hiring_segments': ['Financial Services', 'LegalTech', 'E-Commerce Platforms', 'DevOps Services'],
        'is_live': False,
        'feed_source': 'Regional Reference Benchmark',
        'feed_status': 'Reference Baseline'
    },
    'ukraine': {
        'active_vacancies': '19,500+',
        'demand_index': 89,
        'remote_share': '92%',
        'avg_growth': '+14.1%',
        'hot_skill': 'MilTech, Fullstack TypeScript/Node & Python Backend',
        'market_sentiment': 'Бурхливий розвиток оборонних технологій (MilTech, дрони), висока частка ремоуту та західних клієнтів.',
        'top_hiring_segments': ['MilTech & Defense', 'Global Outstaff/Outsource', 'B2B SaaS Products', 'Embedded & Hardware'],
        'is_live': False,
        'feed_source': 'Regional Reference Benchmark',
        'feed_status': 'Reference Baseline'
    }
}

CACHE_TTL_HOURS = 6

AXIS_WEIGHTS = {
    'learning_curve': 1.0,
    'financial_vector': 1.0,
    'architecture_visual': 1.0,
    'company_scale': 1.0,
    'stress_wlb': 1.0,
}

MAX_AXIS_DELTA = 9.0  # 10.0 - 1.0 on a [1, 10] scale
MAX_EUCLIDEAN_DISTANCE = math.sqrt(sum(w * (MAX_AXIS_DELTA ** 2) for w in AXIS_WEIGHTS.values()))


def fetch_market_trends_with_cache(region='global'):
    if region not in SUPPORTED_REGIONS:
        region = 'global'

    now = timezone.now()
    cached_entry = MarketCache.objects.filter(region=region).first()

    if cached_entry and cached_entry.payload and cached_entry.updated_at:
        cache_age = now - cached_entry.updated_at
        if cache_age < timedelta(hours=CACHE_TTL_HOURS):
            return cached_entry.payload

    external_url = os.environ.get(
        'EXTERNAL_MARKET_API_URL',
        'https://remotive.com/api/remote-jobs?limit=50'
    )

    live_payload = None
    if external_url:
        try:
            resp = requests.get(
                external_url,
                timeout=3.0,
                headers={'User-Agent': 'IT-Career-Navigator/2.0'}
            )
            if resp.status_code == 200:
                raw_json = resp.json()
                live_count = 0
                hot_skill = None

                if 'total-job-count' in raw_json or 'jobs' in raw_json:
                    live_count = raw_json.get('total-job-count') or len(raw_json.get('jobs', []))
                    jobs = raw_json.get('jobs', [])
                    if jobs and isinstance(jobs, list):
                        categories = [j.get('category') for j in jobs if j.get('category')]
                        if categories:
                            hot_skill = f"{categories[0]} (Live Active Feed)"
                elif 'data' in raw_json and isinstance(raw_json['data'], list):
                    live_count = len(raw_json['data'])

                benchmark = DEFAULT_MARKET_SNAPSHOT.get(region, DEFAULT_MARKET_SNAPSHOT['global'])
                live_payload = {
                    'active_vacancies': f"{live_count:,} live vacancies" if live_count else benchmark['active_vacancies'],
                    'demand_index': benchmark['demand_index'],
                    'remote_share': benchmark['remote_share'],
                    'avg_growth': benchmark['avg_growth'],
                    'hot_skill': hot_skill or benchmark['hot_skill'],
                    'market_sentiment': benchmark['market_sentiment'],
                    'top_hiring_segments': benchmark.get('top_hiring_segments', []),
                    'is_live': True,
                    'feed_source': 'Public Tech Jobs Feed (Remotive)',
                    'feed_status': 'Live Feed Active',
                    'last_synced_at': now.isoformat(),
                }
                MarketCache.objects.update_or_create(
                    region=region,
                    defaults={'payload': live_payload}
                )
                return live_payload
        except Exception:
            pass

    if cached_entry and cached_entry.payload:
        return cached_entry.payload

    fallback_data = DEFAULT_MARKET_SNAPSHOT.get(region, DEFAULT_MARKET_SNAPSHOT['global']).copy()
    fallback_data['is_live'] = False
    fallback_data['feed_source'] = 'Regional Reference Benchmark'
    fallback_data['feed_status'] = 'Reference Baseline'
    fallback_data['last_synced_at'] = now.isoformat()

    MarketCache.objects.update_or_create(
        region=region,
        defaults={'payload': fallback_data}
    )
    return fallback_data


def parse_and_clamp_axis(value, axis_name):
    try:
        val_float = float(value)
    except (ValueError, TypeError):
        raise ValueError(f"Value for '{axis_name}' must be a numeric float, got {type(value).__name__}: {value!r}")

    if math.isnan(val_float) or math.isinf(val_float):
        raise ValueError(f"Value for '{axis_name}' cannot be NaN or infinite.")

    return max(1.0, min(10.0, val_float))


def calculate_dss_matches(user_vector, region='global'):
    if not isinstance(user_vector, dict):
        raise ValueError("user_vector must be a dictionary of slider coordinates.")

    u_learn = parse_and_clamp_axis(user_vector.get('learning_curve', 5.0), 'learning_curve')
    u_fin = parse_and_clamp_axis(user_vector.get('financial_vector', 5.0), 'financial_vector')
    u_arch = parse_and_clamp_axis(user_vector.get('architecture_visual', 5.0), 'architecture_visual')
    u_scale = parse_and_clamp_axis(user_vector.get('company_scale', 5.0), 'company_scale')
    u_stress = parse_and_clamp_axis(user_vector.get('stress_wlb', 5.0), 'stress_wlb')

    tracks = CareerTrack.objects.all()
    results = []

    for track in tracks:
        diff_learn = u_learn - track.radar_learning_curve
        diff_fin = u_fin - track.radar_financial_vector
        diff_arch = u_arch - track.radar_architecture_visual
        diff_scale = u_scale - track.radar_company_scale
        diff_stress = u_stress - track.radar_stress_wlb

        weighted_sq_sum = (
            AXIS_WEIGHTS['learning_curve'] * (diff_learn ** 2) +
            AXIS_WEIGHTS['financial_vector'] * (diff_fin ** 2) +
            AXIS_WEIGHTS['architecture_visual'] * (diff_arch ** 2) +
            AXIS_WEIGHTS['company_scale'] * (diff_scale ** 2) +
            AXIS_WEIGHTS['stress_wlb'] * (diff_stress ** 2)
        )
        raw_distance = math.sqrt(weighted_sq_sum)

        match_ratio = max(0.0, 1.0 - (raw_distance / MAX_EUCLIDEAN_DISTANCE))
        match_percentage = round(match_ratio * 100.0, 1)

        match_reasons = []
        if abs(diff_arch) <= 1.5:
            if track.radar_architecture_visual >= 7.0:
                match_reasons.append("Ідеальне попадання у вашу тягу до візуалу, UI/UX та живого зворотного зв'язку.")
            elif track.radar_architecture_visual <= 3.5:
                match_reasons.append("Точний збіг за запитом на глибоку системну архітектуру без необхідності малювати інтерфейси.")
            else:
                match_reasons.append("Гармонійний баланс між сервером та користувацьким інтерфейсом.")

        if abs(diff_learn) <= 2.0:
            if track.radar_learning_curve <= 4.5:
                match_reasons.append("Комфортний та швидкий поріг старту для впевненого входу в індустрію.")
            elif track.radar_learning_curve >= 7.5:
                match_reasons.append("Задовольняє високий апетит до фундаментальної теорії, математики та CS.")

        if abs(diff_fin) <= 1.8 and track.radar_financial_vector >= 8.0:
            match_reasons.append("Повний збіг за амбіціями щодо максимального заробітку на глобальному ринку.")

        if abs(diff_stress) <= 2.0:
            if track.radar_stress_wlb <= 4.0:
                match_reasons.append("Відповідає вашому пріоритету щодо здорового Work-Life Balance та низького стресу.")
            elif track.radar_stress_wlb >= 7.0:
                match_reasons.append("Співпадає з прагненням до високого челенджу, драйву та відповідальності за критичні системи.")

        if not match_reasons:
            match_reasons.append("Збалансований варіант за всіма ключовими параметрами вашого кар'єрного вектору.")

        item = track.to_dict(region=region)
        item['match_percentage'] = match_percentage
        item['match_reasons'] = match_reasons[:2]
        item['raw_distance'] = round(raw_distance, 4)
        results.append(item)

    results.sort(key=lambda x: x['raw_distance'])
    return results
