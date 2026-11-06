from django.core.management.base import BaseCommand
from navigator.models import CareerTrack, MarketCache
from navigator.services import DEFAULT_MARKET_SNAPSHOT

class Command(BaseCommand):
    help = 'Seeds the database with initial IT career tracks and market cache data'

    def handle(self, *args, **options):
        tracks_data = [
            {
                "slug": "python-backend",
                "title": "Python Backend Engineer",
                "tagline": "Серце серверної архітектури, API, мікросервісів та асинхронних систем",
                "category": "Backend & Cloud",
                "icon_type": "server",
                "badge_color": "emerald",
                "radar_learning_curve": 5.5,
                "radar_financial_vector": 8.5,
                "radar_architecture_visual": 2.0,
                "radar_company_scale": 5.0,
                "radar_stress_wlb": 5.0,
                "short_desc": "Проектування надійних REST/gRPC API, робота з базами даних (PostgreSQL), кешуванням (Redis) та асинхронними чергами (Celery/RabbitMQ).",
                "full_desc": "Python Backend розробник відповідає за бізнес-логіку додатків, обробку великих потоків даних, безпеку та взаємодію з базами даних. Python поєднує швидкість розробки та елегантність синтаксису завдяки фреймворкам FastAPI, Django та AsyncIO.",
                "salaries": {
                    "global": {"junior": "$35,000 - $55,000", "middle": "$65,000 - $95,000", "senior": "$110,000 - $160,000", "lead": "$170,000 - $220,000+"},
                    "usa": {"junior": "$75,000 - $95,000", "middle": "$115,000 - $150,000", "senior": "$165,000 - $225,000", "lead": "$230,000 - $310,000+"},
                    "europe": {"junior": "€38,000 - €50,000", "middle": "€60,000 - €85,000", "senior": "€95,000 - €135,000", "lead": "€140,000 - €180,000+"},
                    "uk": {"junior": "£32,000 - £45,000", "middle": "£55,000 - £80,000", "senior": "£90,000 - £130,000", "lead": "£135,000 - £175,000+"},
                    "ukraine": {"junior": "$800 - $1,500 / міс", "middle": "$2,200 - $3,800 / міс", "senior": "$4,500 - $6,500 / міс", "lead": "$6,500 - $8,500+ / міс"}
                },
                "market_stats": {
                    "demand_index": 91,
                    "remote_share": "82%",
                    "yoy_growth": "+15.8%",
                    "open_vacancies_est": "45,000+"
                },
                "tech_stack": [
                    "Python 3.12+", "FastAPI", "Django", "PostgreSQL", "Redis",
                    "Docker", "Kafka / RabbitMQ", "SQLAlchemy", "AsyncIO", "AWS / GCP"
                ],
                "pros": [
                    "Швидкий перехід у суміжні сфери: Data Engineering, AI/ML та Automation",
                    "Чистий, читабельний синтаксис та потужна світова спільнота",
                    "Висока середня зарплата та велика частка ремоут-позицій у світових компаніях",
                    "Величезна кількість бібліотек для будь-якої інженерної задачі"
                ],
                "cons": [
                    "Необхідність глибоко розуміти асинхронність та оптимізацію важких SQL-запитів",
                    "Висока конкуренція на позиції рівня Trainee/Junior",
                    "Динамічна типізація вимагає дисциплінованого покриття тестами (Pytest, Mypy)"
                ],
                "roadmap": [
                    {"phase": "Фаза 1: Основи CS та Python Core", "duration": "4-6 тижнів", "topics": ["Синтаксис, ООП, структури даних, алгоритми", "Декоратори, генератори, контекстні менеджери", "Робота з пам'яттю, GIL, тайп-хінти (Mypy)"]},
                    {"phase": "Фаза 2: Бази даних та Архітектура API", "duration": "6-8 тижнів", "topics": ["Реляційні БД (PostgreSQL, індекси, транзакції, ACID)", "ORM & Query Builders (SQLAlchemy, Alembic)", "FastAPI / Django REST Framework, JWT авторизація, OpenAPI"]},
                    {"phase": "Фаза 3: Асинхронність, Кеш та Черги", "duration": "6-8 тижнів", "topics": ["AsyncIO, Event Loop, неблокуючий I/O", "Кешування з Redis, черги завдань Celery / RQ", "Брокери повідомлень Kafka / RabbitMQ"]},
                    {"phase": "Фаза 4: DevOps, Тестування та Продакшн", "duration": "4-6 тижнів", "topics": ["Docker & Docker Compose, CI/CD (GitHub Actions)", "Тестування (Pytest, моки, інтеграційні тести)", "Мікросервісна архітектура, моніторинг (Prometheus, Grafana)"]}
                ]
            },
            {
                "slug": "frontend-react",
                "title": "Frontend / React & Next.js Engineer",
                "tagline": "Створення інтерактивних інтерфейсів, веб-додатків та виняткового користувацького досвіду",
                "category": "Frontend & Web",
                "icon_type": "code",
                "badge_color": "cyan",
                "radar_learning_curve": 4.5,
                "radar_financial_vector": 7.8,
                "radar_architecture_visual": 9.2,
                "radar_company_scale": 7.0,
                "radar_stress_wlb": 4.5,
                "short_desc": "Розробка адаптивних сучасних SPA/SSR додатків на React, TypeScript та Next.js з акцентом на швидкість, анімації та естетику UI.",
                "full_desc": "Frontend розробник створює все, що бачить і з чим взаємодіє користувач у браузері. Сучасний фронтенд давно вийшов за рамки верстки: це складна архітектура стану клієнта, SSR-рендеринг, робота з WebGL/Canvas та висока оптимізація продуктивності (Core Web Vitals).",
                "salaries": {
                    "global": {"junior": "$32,000 - $50,000", "middle": "$60,000 - $90,000", "senior": "$100,000 - $145,000", "lead": "$150,000 - $200,000+"},
                    "usa": {"junior": "$70,000 - $90,000", "middle": "$110,000 - $145,000", "senior": "$155,000 - $210,000", "lead": "$215,000 - $285,000+"},
                    "europe": {"junior": "€35,000 - €48,000", "middle": "€55,000 - €80,000", "senior": "€90,000 - €125,000", "lead": "€130,000 - €170,000+"},
                    "uk": {"junior": "£30,000 - £42,000", "middle": "£50,000 - £75,000", "senior": "£85,000 - £120,000", "lead": "£125,000 - £165,000+"},
                    "ukraine": {"junior": "$700 - $1,400 / міс", "middle": "$2,000 - $3,500 / міс", "senior": "$4,000 - $5,800 / міс", "lead": "$6,000 - $7,800+ / міс"}
                },
                "market_stats": {
                    "demand_index": 94,
                    "remote_share": "80%",
                    "yoy_growth": "+14.2%",
                    "open_vacancies_est": "60,000+"
                },
                "tech_stack": [
                    "TypeScript", "React 19", "Next.js", "Tailwind CSS",
                    "Zustand / Redux Toolkit", "TanStack Query", "HTML5 / CSS3", "Vite", "Playwright"
                ],
                "pros": [
                    "Миттєвий візуальний результат своєї роботи",
                    "Величезний ринок вакансій по всьому світу та фріланс-можливості",
                    "Сучасний TypeScript робить код надійним та зручним у підтримці",
                    "Швидкий розвиток екосистеми та висока креативність"
                ],
                "cons": [
                    "Стрімке оновлення бібліотек та фреймворків («JS fatigue»)",
                    "Кросбраузерні тонкощі, рендеринг на мобільних пристроях",
                    "Велика конкуренція серед початківців"
                ],
                "roadmap": [
                    {"phase": "Фаза 1: Фундамент вебу та сучасний JS", "duration": "4-5 тижнів", "topics": ["Семантичний HTML5, CSS Flexbox/Grid, Tailwind CSS", "Сучасний JavaScript ES2024 (проміси, async/await, деструктуризація)", "DOM API, робота з подіями, Fetch API"]},
                    {"phase": "Фаза 2: TypeScript та React Core", "duration": "6-7 тижнів", "topics": ["Основи TypeScript (інтерфейси, generics, типи утиліти)", "Компоненти, хуки (useState, useEffect, useMemo, useCallback)", "Управління станом (Zustand) та робота з формами"]},
                    {"phase": "Фаза 3: Fullstack React & Next.js", "duration": "5-6 тижнів", "topics": ["Next.js App Router, Server Components (RSC), SSR/SSG", "Асинхронний кеш (TanStack Query / React Query)", "Оптимізація швидкодії, Web Vitals, SEO"]},
                    {"phase": "Фаза 4: Тестування та Продакшн", "duration": "3-4 тижні", "topics": ["Unit-тестування (Vitest, React Testing Library)", "E2E тестування з Playwright", "Storybook, CI/CD деплой на Vercel/Cloudflare"]}
                ]
            },
            {
                "slug": "devops-cloud",
                "title": "DevOps & Cloud Architect",
                "tagline": "Автоматизація інфраструктури, хмарні платформи та безперебійна доставка коду",
                "category": "Infrastructure & Cloud",
                "icon_type": "cloud",
                "badge_color": "sky",
                "radar_learning_curve": 8.0,
                "radar_financial_vector": 9.3,
                "radar_architecture_visual": 1.5,
                "radar_company_scale": 4.0,
                "radar_stress_wlb": 7.5,
                "short_desc": "Побудова CI/CD конвеєрів, оркестрація контейнерів через Kubernetes, Infrastructure as Code (Terraform) та хмари AWS/Azure/GCP.",
                "full_desc": "DevOps інженер об'єднує розробку та експлуатацію. Головна мета — зробити процес випуску коду автоматизованим, безпечним та масштабованим, а інфраструктуру — стійкою до відмов (High Availability).",
                "salaries": {
                    "global": {"junior": "$42,000 - $65,000", "middle": "$75,000 - $110,000", "senior": "$125,000 - $175,000", "lead": "$180,000 - $240,000+"},
                    "usa": {"junior": "$85,000 - $110,000", "middle": "$130,000 - $165,000", "senior": "$175,000 - $245,000", "lead": "$250,000 - $330,000+"},
                    "europe": {"junior": "€45,000 - €60,000", "middle": "€70,000 - €95,000", "senior": "€105,000 - €145,000", "lead": "€150,000 - €195,000+"},
                    "uk": {"junior": "£40,000 - £55,000", "middle": "£65,000 - £90,000", "senior": "£100,000 - £145,000", "lead": "£150,000 - £190,000+"},
                    "ukraine": {"junior": "$1,000 - $1,800 / міс", "middle": "$2,800 - $4,500 / міс", "senior": "$5,000 - $7,500 / міс", "lead": "$7,500 - $10,000+ / міс"}
                },
                "market_stats": {
                    "demand_index": 96,
                    "remote_share": "85%",
                    "yoy_growth": "+21.5%",
                    "open_vacancies_est": "38,000+"
                },
                "tech_stack": [
                    "Linux / Bash", "Kubernetes (K8s)", "Docker", "Terraform",
                    "AWS / Azure / GCP", "GitHub Actions / GitLab CI", "Ansible",
                    "Prometheus & Grafana", "ArgoCD", "Python / Go"
                ],
                "pros": [
                    "Один із найвищих рівнів зарплат та затребуваності в ІТ",
                    "Мінімальна загроза заміни простими моделями ШІ (складна фізична та хмарна архітектура)",
                    "Широкі можливості для контрактів та високих рейт-часток",
                    "Ключова роль у забезпеченні життєдіяльності будь-якого продукту"
                ],
                "cons": [
                    "Висока відповідальність (якщо лежить прод — шукають вас)",
                    "Можливі нічні чергування (on-call ротації) у критичних системах",
                    "Високий поріг входу (потрібні глибокі знання мереж, ОС та системного адміністрування)"
                ],
                "roadmap": [
                    {"phase": "Фаза 1: Системні основи та мережі", "duration": "5-6 тижнів", "topics": ["Linux адміністрування (ядро, пам'ять, процеси, permissions)", "Комп'ютерні мережі: TCP/IP, DNS, SSL/TLS, HTTP/2, VPN, підмережі", "Bash скрипти та автоматизація на Python/Go"]},
                    {"phase": "Фаза 2: Контейнеризація та CI/CD", "duration": "6-7 тижнів", "topics": ["Docker: оптимізація образів, multi-stage збірки, безпека", "CI/CD: GitHub Actions, GitLab CI (пайплайни, артефакти, secrets)"]},
                    {"phase": "Фаза 3: Оркестрація та Хмари", "duration": "7-8 тижнів", "topics": ["Kubernetes: Pods, Services, Deployments, Ingress, Helm", "Хмарний провайдер (AWS або GCP): IAM, VPC, EKS, RDS, S3"]},
                    {"phase": "Фаза 4: IaC, GitOps та Observability", "duration": "5-6 тижнів", "topics": ["Terraform: модулі, remote state, Infrastructure as Code", "GitOps (ArgoCD, Flux)", "Моніторинг: Prometheus, Grafana, Alertmanager, Loki, OpenTelemetry"]}
                ]
            },
            {
                "slug": "data-science-ai",
                "title": "Data Scientist & AI/ML Engineer",
                "tagline": "Штучний інтелект, нейромережі, LLM та математичне моделювання",
                "category": "Data & AI",
                "icon_type": "cpu",
                "badge_color": "purple",
                "radar_learning_curve": 9.2,
                "radar_financial_vector": 9.8,
                "radar_architecture_visual": 3.0,
                "radar_company_scale": 6.5,
                "radar_stress_wlb": 6.8,
                "short_desc": "Навчання та тюнінг нейромереж, побудова RAG-систем для LLM, математичний аналіз великих даних за допомогою PyTorch та HuggingFace.",
                "full_desc": "Спеціаліст з AI/ML розробляє інтелектуальні алгоритми: від прогнозних моделей до великих мовних моделей (LLM), комп'ютерного зору (Computer Vision) та обробки природної мови (NLP). Поєднує глибоку вищу математику, статистику та інженерію коду.",
                "salaries": {
                    "global": {"junior": "$45,000 - $70,000", "middle": "$80,000 - $125,000", "senior": "$135,000 - $195,000", "lead": "$200,000 - $280,000+"},
                    "usa": {"junior": "$95,000 - $125,000", "middle": "$145,000 - $190,000", "senior": "$200,000 - $290,000", "lead": "$300,000 - $420,000+"},
                    "europe": {"junior": "€48,000 - €65,000", "middle": "€75,000 - €105,000", "senior": "€115,000 - €160,000", "lead": "€170,000 - €230,000+"},
                    "uk": {"junior": "£42,000 - £60,000", "middle": "£70,000 - £100,000", "senior": "£110,000 - £160,000", "lead": "£165,000 - £220,000+"},
                    "ukraine": {"junior": "$1,000 - $1,900 / міс", "middle": "$2,800 - $4,800 / міс", "senior": "$5,200 - $8,000 / міс", "lead": "$8,000 - $12,000+ / міс"}
                },
                "market_stats": {
                    "demand_index": 98,
                    "remote_share": "76%",
                    "yoy_growth": "+34.5%",
                    "open_vacancies_est": "52,000+"
                },
                "tech_stack": [
                    "Python", "PyTorch", "Hugging Face", "LangChain / LlamaIndex",
                    "Pandas & NumPy", "Scikit-Learn", "Vector DBs (Qdrant, Pinecone)",
                    "MLflow", "Docker / GPU Clusters", "SQL"
                ],
                "pros": [
                    "Найгарячіший та найбільш швидкозростаючий сегмент світової технологічної індустрії",
                    "Максимальні верхні ліміти компенсації (включаючи бонуси та опціони стартапів)",
                    "Робота на передовій наукового та технологічного прогресу людства",
                    "Високий інтелектуальний драйв та творчість у вирішенні задач"
                ],
                "cons": [
                    "Потрібна міцна база з лінійної алгебри, теорії ймовірностей та математичного аналізу",
                    "Висока невизначеність: гіпотеза або модель може не дати результату після тижнів навчання",
                    "Дорога інфраструктура (вимоги до GPU кластерів та оптимізації пам'яті)"
                ],
                "roadmap": [
                    {"phase": "Фаза 1: Математика та аналіз даних", "duration": "6-8 тижнів", "topics": ["Лінійна алгебра, матриці, градієнтний спуск", "Теорія ймовірностей, математична статистика", "Pandas, NumPy, очищення та аналіз даних (EDA)"]},
                    {"phase": "Фаза 2: Класичне машинне навчання", "duration": "5-6 тижнів", "topics": ["Лінійна та логістична регресія, дерева рішень, Random Forest", "Градієнтний бустинг (XGBoost, LightGBM, CatBoost)", "Метрики якості (ROC-AUC, F1, RMSE), крос-валідація"]},
                    {"phase": "Фаза 3: Deep Learning & PyTorch", "duration": "7-8 тижнів", "topics": ["Архітектури нейромереж: MLP, CNN, RNN/LSTM, Transformers", "Фреймворк PyTorch, функції втрат, оптимізатори (AdamW)", "Hugging Face екосистема, токенізація, претреновані моделі"]},
                    {"phase": "Фаза 4: Сучасний GenAI, RAG та MLOps", "duration": "6-7 тижнів", "topics": ["Побудова RAG (Retrieval-Augmented Generation), векторні бази (Pinecone/Qdrant)", "Fine-tuning моделей (LoRA/QLoRA), квантизація", "MLOps пайплайни (MLflow, Docker, FastAPI для AI сервісів)"]}
                ]
            },
            {
                "slug": "fullstack-web",
                "title": "Fullstack Web Developer (TS + Node / Python)",
                "tagline": "Універсальний інженер, здатний побудувати продукт від БД до інтерфейсу",
                "category": "Software Engineering",
                "icon_type": "code",
                "badge_color": "amber",
                "radar_learning_curve": 6.2,
                "radar_financial_vector": 8.2,
                "radar_architecture_visual": 6.0,
                "radar_company_scale": 8.0,
                "radar_stress_wlb": 6.0,
                "short_desc": "Поєднання клієнтської розробки (React/Next.js) та серверної логіки (Node.js/Python), що робить вас ідеальним кандидатом для стартапів та продуктових команд.",
                "full_desc": "Fullstack розробник бачить усю картину продукту. Він може самостійно спроектувати схему бази даних, написати безпечний бекенд, створити привабливий та швидкий інтерфейс і задеплоїти готове рішення в хмару.",
                "salaries": {
                    "global": {"junior": "$36,000 - $55,000", "middle": "$65,000 - $95,000", "senior": "$110,000 - $155,000", "lead": "$160,000 - $215,000+"},
                    "usa": {"junior": "$75,000 - $95,000", "middle": "$115,000 - $150,000", "senior": "$165,000 - $225,000", "lead": "$230,000 - $300,000+"},
                    "europe": {"junior": "€40,000 - €52,000", "middle": "€62,000 - €88,000", "senior": "€95,000 - €135,000", "lead": "€140,000 - €185,000+"},
                    "uk": {"junior": "£35,000 - £48,000", "middle": "£55,000 - £82,000", "senior": "£90,000 - £130,000", "lead": "£135,000 - £175,000+"},
                    "ukraine": {"junior": "$800 - $1,500 / міс", "middle": "$2,200 - $3,800 / міс", "senior": "$4,200 - $6,200 / міс", "lead": "$6,500 - $8,500+ / міс"}
                },
                "market_stats": {
                    "demand_index": 93,
                    "remote_share": "79%",
                    "yoy_growth": "+16.1%",
                    "open_vacancies_est": "68,000+"
                },
                "tech_stack": [
                    "TypeScript", "React / Next.js", "Node.js / Express / NestJS",
                    "PostgreSQL / Prisma", "Tailwind CSS", "Redis", "Docker", "REST / GraphQL", "AWS / Vercel"
                ],
                "pros": [
                    "Надзвичайна автономність: можливість запускати власні стартапи та пет-проєкти «під ключ»",
                    "Золотий стандарт для стартапів та гнучких продуктових команд",
                    "Різноманітність завдань — відсутність монотонності в робочому дні",
                    "Широкі перспективи кар'єрного росту до Tech Lead та CTO"
                ],
                "cons": [
                    "Необхідність утримувати в голові два великі світи (фронтенд і бекенд)",
                    "Ризик поверхових знань («jack of all trades, master of none») без дисципліни",
                    "Швидкі темпи змін одночасно у двох екосистемах"
                ],
                "roadmap": [
                    {"phase": "Фаза 1: Універсальний TypeScript та Веб-основи", "duration": "4-5 тижнів", "topics": ["Сучасний TypeScript для клієнта і сервера", "HTML5, Tailwind CSS, основи дизайну компонентів"]},
                    {"phase": "Фаза 2: Клієнтська частина (React & Next.js)", "duration": "5-6 тижнів", "topics": ["React хуки, стейт-менеджмент, оптимізація", "Next.js App Router, SSR, клієнтські та серверні форми"]},
                    {"phase": "Фаза 3: Серверна частина та Бази даних", "duration": "6-7 тижнів", "topics": ["Node.js (NestJS / Express) або Python (FastAPI)", "PostgreSQL, моделювання зв'язків, міграції з Prisma/Drizzle", "JWT, OAuth 2.0, безпека API, CORS"]},
                    {"phase": "Фаза 4: Інтеграція, Кешування та Деплой", "duration": "4-5 тижнів", "topics": ["Redis кешування, черги завдань BullMQ", "Docker контейнеризація, CI/CD деплой у хмару"]}
                ]
            },
            {
                "slug": "mobile-flutter-ios",
                "title": "Mobile Developer (Flutter / iOS / Android)",
                "tagline": "Мобільні додатки для мільйонів кишенькових пристроїв",
                "category": "Mobile Development",
                "icon_type": "mobile",
                "badge_color": "rose",
                "radar_learning_curve": 5.0,
                "radar_financial_vector": 7.5,
                "radar_architecture_visual": 8.0,
                "radar_company_scale": 6.0,
                "radar_stress_wlb": 5.2,
                "short_desc": "Розробка мобільних додатків на Flutter/Dart або Swift/Kotlin для App Store та Google Play з плавною графікою 120 FPS та роботою з датчиками пристрою.",
                "full_desc": "Мобільний інженер створює нативні та кросплатформні додатки, якими люди користуються щодня: від банкінгу та фітнес-трекерів до соцмереж та доставки їжі. Важлива увага приділяється роботі в офлайн-режимі, економії заряду батареї та жестам.",
                "salaries": {
                    "global": {"junior": "$32,000 - $50,000", "middle": "$60,000 - $90,000", "senior": "$105,000 - $145,000", "lead": "$150,000 - $200,000+"},
                    "usa": {"junior": "$72,000 - $92,000", "middle": "$115,000 - $145,000", "senior": "$160,000 - $215,000", "lead": "$220,000 - $290,000+"},
                    "europe": {"junior": "€36,000 - €48,000", "middle": "€58,000 - €82,000", "senior": "€90,000 - €128,000", "lead": "€135,000 - €175,000+"},
                    "uk": {"junior": "£32,000 - £45,000", "middle": "£52,000 - £78,000", "senior": "£85,000 - £125,000", "lead": "£130,000 - £170,000+"},
                    "ukraine": {"junior": "$750 - $1,400 / міс", "middle": "$2,000 - $3,600 / міс", "senior": "$4,200 - $6,000 / міс", "lead": "$6,200 - $8,000+ / міс"}
                },
                "market_stats": {
                    "demand_index": 86,
                    "remote_share": "75%",
                    "yoy_growth": "+12.4%",
                    "open_vacancies_est": "32,000+"
                },
                "tech_stack": [
                    "Dart / Flutter", "Swift / SwiftUI (iOS)", "Kotlin / Jetpack Compose (Android)",
                    "BLoC / Riverpod", "SQLite / Hive / Room", "REST & WebSocket", "Firebase", "Fastlane"
                ],
                "pros": [
                    "Приємно бачити свій додаток на смартфонах друзів та рідних",
                    "Flutter дозволяє писати один красивий код одразу під iOS та Android",
                    "Стабільний попит у фінтеху, доставці, e-commerce та стартапах",
                    "Зрозумілий та відчутний життєвий цикл додатків"
                ],
                "cons": [
                    "Сувора модерація в App Store та Google Play (можуть відхилити білд)",
                    "Необхідність тестування на десятках різних розмірів екранів та версій ОС",
                    "Для iOS розробки обов'язково потрібен Mac"
                ],
                "roadmap": [
                    {"phase": "Фаза 1: Мова програмування та ООП", "duration": "4-5 тижнів", "topics": ["Основи Dart або Swift: типізація, колекції, асинхронність", "ООП, патерни проектування, робота з пам'яттю"]},
                    {"phase": "Фаза 2: Віджети та Архітектура додатку", "duration": "6-7 тижнів", "topics": ["Flutter Widget Tree, адаптивна верстка під будь-який екран", "Керування станом (BLoC / Cubit / Riverpod)", "Навігація (GoRouter), робота з темами"]},
                    {"phase": "Фаза 3: Мережа, Локальна БД та Датчики", "duration": "5-6 тижнів", "topics": ["HTTP запити (Dio), JSON парсинг, WebSockets", "Локальне збереження даних (Hive, Isar, Drift, SQLite)", "Геолокація, камера, Push-повідомлення (Firebase Cloud Messaging)"]},
                    {"phase": "Фаза 4: Реліз в App Store та Google Play", "duration": "3-4 тижні", "topics": ["Автоматизація збірок (Fastlane, CI/CD)", "Підготовка сертифікатів, Provisioning Profiles", "Оптимізація розміру білду та аналітика крешів"]}
                ]
            },
            {
                "slug": "qa-automation",
                "title": "QA Automation & SDET",
                "tagline": "Автоматизація тестування, забезпечення надійності та якості коду",
                "category": "Quality & Testing",
                "icon_type": "check",
                "badge_color": "emerald",
                "radar_learning_curve": 4.0,
                "radar_financial_vector": 6.8,
                "radar_architecture_visual": 4.0,
                "radar_company_scale": 2.5,
                "radar_stress_wlb": 3.5,
                "short_desc": "Написання тестових фреймворків (Playwright, Cypress, Selenium), навантажувальне тестування (k6) та інтеграція в CI/CD пайплайни.",
                "full_desc": "SDET (Software Development Engineer in Test) та QA Automation інженер гарантує, що жоден баг не прослизне в реліз. Вони розробляють програми, які автоматично тестують інші програми: перевіряють API, користувацькі сценарії, навантаження та продуктивність.",
                "salaries": {
                    "global": {"junior": "$30,000 - $45,000", "middle": "$55,000 - $80,000", "senior": "$90,000 - $130,000", "lead": "$135,000 - $175,000+"},
                    "usa": {"junior": "$68,000 - $88,000", "middle": "$100,000 - $135,000", "senior": "$145,000 - $190,000", "lead": "$195,000 - $250,000+"},
                    "europe": {"junior": "€34,000 - €46,000", "middle": "€52,000 - €75,000", "senior": "€82,000 - €115,000", "lead": "€120,000 - €155,000+"},
                    "uk": {"junior": "£28,000 - £40,000", "middle": "£48,000 - £70,000", "senior": "£78,000 - £110,000", "lead": "£115,000 - £150,000+"},
                    "ukraine": {"junior": "$650 - $1,300 / міс", "middle": "$1,800 - $3,200 / міс", "senior": "$3,600 - $5,200 / міс", "lead": "$5,200 - $6,800+ / міс"}
                },
                "market_stats": {
                    "demand_index": 85,
                    "remote_share": "84%",
                    "yoy_growth": "+10.8%",
                    "open_vacancies_est": "29,000+"
                },
                "tech_stack": [
                    "Python / TypeScript / Java", "Playwright", "Cypress", "Pytest",
                    "Postman / Newman", "k6 / JMeter", "Docker", "CI/CD Actions", "Allure Report"
                ],
                "pros": [
                    "Найбільш прогнозований та спокійний робочий графік серед інженерних спеціальностей",
                    "М'який та комфортний поріг входження для світчерів",
                    "Висока затребуваність у великих стабільних корпораціях та банках",
                    "Можливість поступово вирости в повноцінного Backend або DevOps спеціаліста"
                ],
                "cons": [
                    "Стеля зарплати дещо нижча, ніж у розробників штучного інтелекту або архітекторів",
                    "Іноді виникає рутина під час підтримки застарілих тестових наборів",
                    "Потрібно постійно взаємодіяти з розробниками та доводити наявність дефектів"
                ],
                "roadmap": [
                    {"phase": "Фаза 1: Основи тестування та мова програмування", "duration": "4-5 тижнів", "topics": ["Теорія тестування: тест-кейси, баг-репорти, техніки тест-дизайну", "Python або TypeScript: базовий синтаксис, структури даних, функції"]},
                    {"phase": "Фаза 2: Автоматизація API тестування", "duration": "4-5 тижнів", "topics": ["Протокол HTTP, статус-коди, REST API", "Автоматизація запитів: Requests / SuperTest, валідація JSON схем", "Тестові раннери: Pytest, фікстури, параметризація, звіти Allure"]},
                    {"phase": "Фаза 3: UI Автоматизація", "duration": "5-6 тижнів", "topics": ["Сучасний Playwright / Cypress, Page Object Model (POM)", "Селектори, очікування елементів, робота з iFrames та cookies", "Паралельний запуск тестів"]},
                    {"phase": "Фаза 4: CI/CD та Навантажувальне тестування", "duration": "3-4 тижні", "topics": ["Інтеграція тестів у GitHub Actions / GitLab CI", "Тестування продуктивності з k6", "Docker контейнери для запуску тестів у безголовому режимі"]}
                ]
            },
            {
                "slug": "cybersecurity",
                "title": "Cybersecurity & InfoSec Specialist",
                "tagline": "Захист цифрових фортець, пентестинг та протидія кібератакам",
                "category": "Security & Defense",
                "icon_type": "shield",
                "badge_color": "rose",
                "radar_learning_curve": 8.8,
                "radar_financial_vector": 9.2,
                "radar_architecture_visual": 1.0,
                "radar_company_scale": 2.0,
                "radar_stress_wlb": 8.8,
                "short_desc": "Аналіз вразливостей, етичний хакінг (Red Team), побудова захисту (Blue Team), аналіз мережевих протоколів та безпека хмарної інфраструктури.",
                "full_desc": "Фахівець з кібербезпеки стоїть на варті захисту критичних даних та інфраструктури бізнесу і держави від хакерських угруповань. Сфера охоплює етичний хакінг, реверс-інжиніринг, розслідування інцидентів (SOC) та дотримання стандартів безпеки.",
                "salaries": {
                    "global": {"junior": "$42,000 - $65,000", "middle": "$75,000 - $115,000", "senior": "$130,000 - $185,000", "lead": "$190,000 - $260,000+"},
                    "usa": {"junior": "$85,000 - $110,000", "middle": "$135,000 - $175,000", "senior": "$180,000 - $260,000", "lead": "$260,000 - $350,000+"},
                    "europe": {"junior": "€45,000 - €60,000", "middle": "€70,000 - €100,000", "senior": "€110,000 - €155,000", "lead": "€160,000 - €210,000+"},
                    "uk": {"junior": "£38,000 - £55,000", "middle": "£65,000 - £95,000", "senior": "£105,000 - £150,000", "lead": "£155,000 - £205,000+"},
                    "ukraine": {"junior": "$900 - $1,700 / міс", "middle": "$2,500 - $4,200 / міс", "senior": "$4,800 - $7,200 / міс", "lead": "$7,000 - $10,000+ / міс"}
                },
                "market_stats": {
                    "demand_index": 95,
                    "remote_share": "69%",
                    "yoy_growth": "+24.8%",
                    "open_vacancies_est": "35,000+"
                },
                "tech_stack": [
                    "Linux / Kali", "Wireshark / Burp Suite", "Python / Bash",
                    "SIEM (Splunk, Wazuh)", "Metasploit", "Cryptography",
                    "Cloud Security (AWS IAM, GuardDuty)", "OWASP Top 10"
                ],
                "pros": [
                    "Критична важливість: безпеку не скоротять навіть під час кризи",
                    "Надзвичайно цікава сфера для тих, хто любить загадки та дослідження",
                    "Величезні бюджети у банках, оборонному секторі та транснаціональних корпораціях",
                    "Престижність професії та міжнародний авторитет"
                ],
                "cons": [
                    "Високий рівень стресу у разі інцидентів та атак нульового дня (0-day)",
                    "Потрібно знати все: від заліза та кабелів до веб-сокетів та психології (соцінженерія)",
                    "Часто потрібні дорогі сертифікати (OSCP, CEH, CISSP)"
                ],
                "roadmap": [
                    {"phase": "Фаза 1: Фундамент мереж та систем", "duration": "6-7 тижнів", "topics": ["Мережеві протоколи в деталях: DNS, BGP, ARP, TCP/UDP, TLS handshakes", "Аналіз трафіку з Wireshark, tcpdump", "Linux ядро, системні виклики, пам'ять"]},
                    {"phase": "Фаза 2: Веб-безпека та вразливості", "duration": "5-6 тижнів", "topics": ["OWASP Top 10 (SQLi, XSS, CSRF, SSRF, IDOR)", "Практика з Burp Suite, аудит веб-додатків", "Платформи PortSwigger Web Security Academy & TryHackMe"]},
                    {"phase": "Фаза 3: Blue Team & Моніторинг", "duration": "6-7 тижнів", "topics": ["SIEM системи (Splunk, Elastic SIEM, Wazuh)", "Аналіз логів, детекція аномалій, правила Sigma/YARA", "Incident Response та цифрова криміналістика (Forensics)"]},
                    {"phase": "Фаза 4: Хмарна безпека та Пентестинг", "duration": "5-6 тижнів", "topics": ["Cloud Security (AWS Security Hub, Kubernetes Pod Security)", "Етичний пентестинг, Metasploit, Privilege Escalation", "Підготовка до сертифікацій (CompTIA Security+ / eJPT / OSCP)"]}
                ]
            },
            {
                "slug": "data-engineer",
                "title": "Data Engineer & Big Data",
                "tagline": "Побудова магістралей даних, озер даних та пайплайнів обробки терабайтів",
                "category": "Data & Cloud",
                "icon_type": "server",
                "badge_color": "indigo",
                "radar_learning_curve": 7.4,
                "radar_financial_vector": 8.9,
                "radar_architecture_visual": 1.8,
                "radar_company_scale": 3.0,
                "radar_stress_wlb": 5.8,
                "short_desc": "Проектування сховищ даних (DWH, Snowflake), розподілена обробка (Apache Spark, Kafka) та оркестрація пайплайнів (Apache Airflow).",
                "full_desc": "Data Engineer створює та підтримує канали передачі даних. Без нього аналітики та Data Scientists не зможуть працювати — інженер збирає дані з десятків джерел, очищує їх, трансформує та завантажує у сховища даних (Data Lake / Lakehouse).",
                "salaries": {
                    "global": {"junior": "$38,000 - $60,000", "middle": "$72,000 - $105,000", "senior": "$120,000 - $170,000", "lead": "$175,000 - $235,000+"},
                    "usa": {"junior": "$80,000 - $105,000", "middle": "$125,000 - $160,000", "senior": "$170,000 - $240,000", "lead": "$240,000 - $320,000+"},
                    "europe": {"junior": "€42,000 - €56,000", "middle": "€68,000 - €92,000", "senior": "€105,000 - €145,000", "lead": "€148,000 - €190,000+"},
                    "uk": {"junior": "£36,000 - £50,000", "middle": "£62,000 - £88,000", "senior": "£95,000 - £140,000", "lead": "£145,000 - £185,000+"},
                    "ukraine": {"junior": "$900 - $1,700 / міс", "middle": "$2,500 - $4,200 / міс", "senior": "$4,800 - $7,000 / міс", "lead": "$7,000 - $9,200+ / міс"}
                },
                "market_stats": {
                    "demand_index": 92,
                    "remote_share": "81%",
                    "yoy_growth": "+19.4%",
                    "open_vacancies_est": "39,000+"
                },
                "tech_stack": [
                    "Python / SQL (Advanced)", "Apache Spark (PySpark)", "Apache Kafka",
                    "Apache Airflow", "Snowflake / BigQuery / Databricks",
                    "dbt (data build tool)", "Docker", "AWS S3 / GCP Cloud Storage"
                ],
                "pros": [
                    "Фундаментальна роль у будь-якій компанії, що працює з даними та AI",
                    "Висока стабільність контрактів та довгострокові проекти",
                    "Відмінне поєднання написання коду та архітектури розподілених систем",
                    "Гідні компенсації навіть на позиціях рівня Middle"
                ],
                "cons": [
                    "Потрібно віртуозно володіти складними аналітичними SQL-запитами та оптимізацією",
                    "Нічні збої у важких щоденних ETL-процесах",
                    "Робота переважно за лаштунками (без яскравого візуального інтерфейсу)"
                ],
                "roadmap": [
                    {"phase": "Фаза 1: Advanced SQL & Data Modeling", "duration": "5-6 тижнів", "topics": ["Віконні функції, оптимізація планів виконання (EXPLAIN ANALYZE)", "Моделювання даних: зірка, сніжинка, Data Vault, повільно змінювані виміри (SCD)", "Python для інженерії даних"]},
                    {"phase": "Фаза 2: Розподілена обробка (Big Data)", "duration": "6-7 тижнів", "topics": ["Apache Spark архітектура: RDD, DataFrames, партиціонування", "PySpark оптимізація пам'яті, shuffle, broadcast joins", "Робота з форматами Parquet, Delta Lake"]},
                    {"phase": "Фаза 3: Потокова передача та Оркестрація", "duration": "5-6 тижнів", "topics": ["Стрімінг з Apache Kafka (topics, partitions, consumer groups)", "Оркестрація пайплайнів з Apache Airflow (DAGs, operators, sensors)", "Трансформація даних з dbt"]},
                    {"phase": "Фаза 4: Хмарні DWH та Data Lakehouse", "duration": "4-5 тижнів", "topics": ["Snowflake / Google BigQuery / Databricks", "CI/CD для даних (DataOps), валідація якості даних (Great Expectations)"]}
                ]
            },
            {
                "slug": "game-dev",
                "title": "Game Developer (C++ / Unreal / Unity)",
                "tagline": "Створення віртуальних світів, ігрової фізики та інтерактивного геймплею",
                "category": "Gaming & Simulation",
                "icon_type": "game",
                "badge_color": "purple",
                "radar_learning_curve": 8.2,
                "radar_financial_vector": 6.5,
                "radar_architecture_visual": 8.5,
                "radar_company_scale": 6.0,
                "radar_stress_wlb": 7.8,
                "short_desc": "Програмування ігрових механік, AI супротивників, рендерингу шейдерів та фізики на C++ (Unreal Engine) або C# (Unity).",
                "full_desc": "Розробник ігор оживляє віртуальні світи. Спеціальність поєднує низькорівневу оптимізацію пам'яті, лінійну алгебру (вектори, кватерніони, матриці трансформацій), роботу з графічним конвеєром та художнє відчуття динаміки гри.",
                "salaries": {
                    "global": {"junior": "$30,000 - $48,000", "middle": "$55,000 - $82,000", "senior": "$95,000 - $140,000", "lead": "$145,000 - $190,000+"},
                    "usa": {"junior": "$65,000 - $85,000", "middle": "$95,000 - $135,000", "senior": "$145,000 - $200,000", "lead": "$205,000 - $275,000+"},
                    "europe": {"junior": "€32,000 - €45,000", "middle": "€50,000 - €75,000", "senior": "€85,000 - €120,000", "lead": "€125,000 - €165,000+"},
                    "uk": {"junior": "£28,000 - £40,000", "middle": "£48,000 - £72,000", "senior": "£80,000 - £118,000", "lead": "£120,000 - £160,000+"},
                    "ukraine": {"junior": "$600 - $1,200 / міс", "middle": "$1,700 - $3,200 / міс", "senior": "$3,800 - $5,500 / міс", "lead": "$5,500 - $7,500+ / міс"}
                },
                "market_stats": {
                    "demand_index": 80,
                    "remote_share": "68%",
                    "yoy_growth": "+9.5%",
                    "open_vacancies_est": "24,000+"
                },
                "tech_stack": [
                    "C++ / C#", "Unreal Engine 5 (UE5)", "Unity",
                    "HLSL / GLSL Shaders", "3D Math & Physics", "Git LFS",
                    "Multiplayer Networking", "DirectX / Vulkan basics"
                ],
                "pros": [
                    "Максимальна пристрасть та драйв: ви створюєте емоції для мільйонів гравців",
                    "Глибокі інженерні знання роботи заліза, пам'яті та графічних процесорів",
                    "Можливість створювати власні інді-ігри та запускати їх у Steam/Epic Store",
                    "Робота на стику мистецтва, фізики та чистого хардкорного коду"
                ],
                "cons": [
                    "Подекуди присутня культура дедлайнів («кранчів») перед великими релізами",
                    "Співвідношення складності та оплати трохи поступається фінтеху та хмарам",
                    "Великі білди, що вимагають потужного заліза"
                ],
                "roadmap": [
                    {"phase": "Фаза 1: Мова програмування та 3D Математика", "duration": "5-6 тижнів", "topics": ["C++20 (вказівники, посилання, керування пам'яттю, RAII, шаблони)", "Векторна алгебра, скалярний/векторний добуток, матриці, кватерніони"]},
                    {"phase": "Фаза 2: Рушій та Ігровий цикл", "duration": "6-7 тижнів", "topics": ["Unreal Engine 5 архітектура: Actors, Components, Blueprints & C++ зв'язка", "Game Loop, фізичні колізії, raycasting, анімаційні стейт-машини"]},
                    {"phase": "Фаза 3: Штучний інтелект та Графіка", "duration": "6-7 тижнів", "topics": ["Ігровий AI: Behavior Trees, Blackboard, Navigation Mesh", "Шейдери (HLSL), матеріали, освітлення Lumen, оптимізація Nanite"]},
                    {"phase": "Фаза 4: Мережевий код та Профайлінг", "duration": "5-6 тижнів", "topics": ["Мультиплеєр: реплікація змінних, RPC, компенсація лагу", "Профайлінг пам'яті та кадрів (Unreal Insights), оптимізація draw calls"]}
                ]
            }
        ]

        tracks_created = 0
        tracks_updated = 0
        for item in tracks_data:
            obj, created = CareerTrack.objects.update_or_create(
                slug=item["slug"],
                defaults=item
            )
            if created:
                tracks_created += 1
            else:
                tracks_updated += 1

        caches_count = 0
        for region_key, payload in DEFAULT_MARKET_SNAPSHOT.items():
            MarketCache.objects.update_or_create(
                region=region_key,
                defaults={'payload': payload}
            )
            caches_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Базу даних успішно наповнено! Створено: {tracks_created}, Оновлено: {tracks_updated} треків. Кеш оновлено для {caches_count} регіонів."
        ))
