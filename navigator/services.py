import os
import math
import requests
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
        'top_hiring_segments': ['Cloud Computing', 'AI Platforms', 'Fintech', 'Cybersecurity']
    },
    'usa': {
        'active_vacancies': '145,000+',
        'demand_index': 95,
        'remote_share': '68%',
        'avg_growth': '+18.2%',
        'hot_skill': 'LLM Fine-tuning & Distributed Systems',
        'market_sentiment': 'Активна реструктуризація в сторону AI-native розробників та інфраструктурних інженерів.',
        'top_hiring_segments': ['Enterprise SaaS', 'HealthTech', 'Defense & GovTech', 'AI Infrastructure']
    },
    'europe': {
        'active_vacancies': '85,000+',
        'demand_index': 88,
        'remote_share': '71%',
        'avg_growth': '+12.8%',
        'hot_skill': 'Data Governance, Rust & Microservices',
        'market_sentiment': 'Стабільний попит з фокусом на WLB, кібербезпеку (NIS2) та відповідність GDPR.',
        'top_hiring_segments': ['Automotive Tech', 'CleanTech', 'Fintech & Neobanks', 'GovTech']
    },
    'uk': {
        'active_vacancies': '42,000+',
        'demand_index': 87,
        'remote_share': '65%',
        'avg_growth': '+11.5%',
        'hot_skill': 'Cloud Architecture & Event-Driven Systems',
        'market_sentiment': 'Лондон зберігає лідерство у фінтеху та інвестиціях в AI-стартапи.',
        'top_hiring_segments': ['Financial Services', 'LegalTech', 'E-Commerce Platforms', 'DevOps Services']
    },
    'ukraine': {
        'active_vacancies': '19,500+',
        'demand_index': 89,
        'remote_share': '92%',
        'avg_growth': '+14.1%',
        'hot_skill': 'MilTech, Fullstack TypeScript/Node & Python Backend',
        'market_sentiment': 'Бурхливий розвиток оборонних технологій (MilTech, дрони), висока частка ремоуту та західних клієнтів.',
        'top_hiring_segments': ['MilTech & Defense', 'Global Outstaff/Outsource', 'B2B SaaS Products', 'Embedded & Hardware']
    }
}

def fetch_market_trends_with_cache(region='global'):
    if region not in SUPPORTED_REGIONS:
        region = 'global'

    cached_entry = MarketCache.objects.filter(region=region).first()

    external_url = os.environ.get('EXTERNAL_MARKET_API_URL')
    if external_url:
        try:
            response = requests.get(
                f"{external_url}?country={region}",
                timeout=2.0,
                headers={'User-Agent': 'IT-Career-Navigator/1.0'}
            )
            if response.status_code == 200:
                api_data = response.json()
                if cached_entry:
                    cached_entry.payload = api_data
                    cached_entry.save()
                else:
                    cached_entry = MarketCache.objects.create(
                        region=region,
                        payload=api_data
                    )
                return cached_entry.payload
        except Exception:
            pass

    if cached_entry and cached_entry.payload:
        return cached_entry.payload

    fallback_data = DEFAULT_MARKET_SNAPSHOT.get(region, DEFAULT_MARKET_SNAPSHOT['global'])
    MarketCache.objects.update_or_create(
        region=region,
        defaults={'payload': fallback_data}
    )
    return fallback_data

def calculate_dss_matches(user_vector, region='global'):
    weights = {
        'learning_curve': 1.05,
        'financial_vector': 1.00,
        'architecture_visual': 1.25,
        'company_scale': 0.90,
        'stress_wlb': 1.00
    }

    max_possible_distance = math.sqrt(sum(w * (9.0 ** 2) for w in weights.values()))

    u_learn = max(1.0, min(10.0, float(user_vector.get('learning_curve', 5))))
    u_fin = max(1.0, min(10.0, float(user_vector.get('financial_vector', 5))))
    u_arch = max(1.0, min(10.0, float(user_vector.get('architecture_visual', 5))))
    u_scale = max(1.0, min(10.0, float(user_vector.get('company_scale', 5))))
    u_stress = max(1.0, min(10.0, float(user_vector.get('stress_wlb', 5))))

    tracks = CareerTrack.objects.all()
    results = []

    for track in tracks:
        diff_learn = (u_learn - track.radar_learning_curve)
        diff_fin = (u_fin - track.radar_financial_vector)
        diff_arch = (u_arch - track.radar_architecture_visual)
        diff_scale = (u_scale - track.radar_company_scale)
        diff_stress = (u_stress - track.radar_stress_wlb)

        weighted_sq_sum = (
            weights['learning_curve'] * (diff_learn ** 2) +
            weights['financial_vector'] * (diff_fin ** 2) +
            weights['architecture_visual'] * (diff_arch ** 2) +
            weights['company_scale'] * (diff_scale ** 2) +
            weights['stress_wlb'] * (diff_stress ** 2)
        )
        euclidean_distance = math.sqrt(weighted_sq_sum)

        normalized_ratio = euclidean_distance / max_possible_distance
        match_percentage = round(max(15, min(99, (1.0 - (normalized_ratio ** 1.15)) * 100)))

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
        item['raw_distance'] = round(euclidean_distance, 2)
        results.append(item)

    results.sort(key=lambda x: x['match_percentage'], reverse=True)
    return results
