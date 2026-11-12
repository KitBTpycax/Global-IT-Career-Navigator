from django.core.management.base import BaseCommand
from navigator.models import CareerTrack, MarketCache
from navigator.services import DEFAULT_MARKET_SNAPSHOT

class Command(BaseCommand):
    help = 'Seeds the database with balanced IT career tracks and initial regional market benchmarks'

    def handle(self, *args, **options):
        tracks_data = [
            {
                "slug": "qa-automation",
                "title": "QA Automation & SDET",
                "tagline": "Автоматизація тестування, забезпечення надійності та стабільний графік",
                "category": "Quality & Testing",
                "icon_type": "check",
                "badge_color": "emerald",
                "radar_learning_curve": 3.0,
                "radar_financial_vector": 4.5,
                "radar_architecture_visual": 3.5,
                "radar_company_scale": 2.5,
                "radar_stress_wlb": 2.0,
                "short_desc": "Написання тестових фреймворків (Playwright, Cypress, Selenium), навантажувальне тестування (k6) та CI/CD валідація.",
                "full_desc": "SDET та QA Automation інженер гарантує стабільність релізів. Спеціальність відрізняється комфортним передбачуваним темпом, збалансованим робочим графіком та високим попитом у банківських і корпоративних системах.",
                "salaries": {
                    "global": {
                        "junior": "$30,000 - $45,000",
                        "middle": "$55,000 - $80,000",
                        "senior": "$90,000 - $130,000",
                        "lead": "$135,000 - $175,000+",
                        "structured": {
                            "junior": {"min": 30000, "max": 45000, "currency": "USD", "period": "yearly"},
                            "middle": {"min": 55000, "max": 80000, "currency": "USD", "period": "yearly"},
                            "senior": {"min": 90000, "max": 130000, "currency": "USD", "period": "yearly"},
                            "lead": {"min": 135000, "max": 175000, "currency": "USD", "period": "yearly"}
                        }
                    },
                    "usa": {
                        "junior": "$65,000 - $85,000",
                        "middle": "$95,000 - $130,000",
                        "senior": "$140,000 - $180,000",
                        "lead": "$190,000 - $240,000+",
                        "structured": {
                            "junior": {"min": 65000, "max": 85000, "currency": "USD", "period": "yearly"},
                            "middle": {"min": 95000, "max": 130000, "currency": "USD", "period": "yearly"},
                            "senior": {"min": 140000, "max": 180000, "currency": "USD", "period": "yearly"},
                            "lead": {"min": 190000, "max": 240000, "currency": "USD", "period": "yearly"}
                        }
                    },
                    "europe": {
                        "junior": "€32,000 - €44,000",
                        "middle": "€50,000 - €72,000",
                        "senior": "€80,000 - €110,000",
                        "lead": "€115,000 - €150,000+",
                        "structured": {
                            "junior": {"min": 32000, "max": 44000, "currency": "EUR", "period": "yearly"},
                            "middle": {"min": 50000, "max": 72000, "currency": "EUR", "period": "yearly"},
                            "senior": {"min": 80000, "max": 110000, "currency": "EUR", "period": "yearly"},
                            "lead": {"min": 115000, "max": 150000, "currency": "EUR", "period": "yearly"}
                        }
                    },
                    "uk": {
                        "junior": "£26,000 - £38,000",
                        "middle": "£45,000 - £68,000",
                        "senior": "£75,000 - £105,000",
                        "lead": "£110,000 - £145,000+",
                        "structured": {
                            "junior": {"min": 26000, "max": 38000, "currency": "GBP", "period": "yearly"},
                            "middle": {"min": 45000, "max": 68000, "currency": "GBP", "period": "yearly"},
                            "senior": {"min": 75000, "max": 105000, "currency": "GBP", "period": "yearly"},
                            "lead": {"min": 110000, "max": 145000, "currency": "GBP", "period": "yearly"}
                        }
                    },
                    "ukraine": {
                        "junior": "$600 - $1,200 / міс",
                        "middle": "$1,700 - $3,000 / міс",
                        "senior": "$3,500 - $5,000 / міс",
                        "lead": "$5,000 - $6,500+ / міс",
                        "structured": {
                            "junior": {"min": 600, "max": 1200, "currency": "USD", "period": "monthly"},
                            "middle": {"min": 1700, "max": 3000, "currency": "USD", "period": "monthly"},
                            "senior": {"min": 3500, "max": 5000, "currency": "USD", "period": "monthly"},
                            "lead": {"min": 5000, "max": 6500, "currency": "USD", "period": "monthly"}
                        }
                    }
                },
                "market_stats": {
                    "demand_index": 85,
                    "remote_share": "84%",
                    "yoy_growth": "+10.8%",
                    "open_vacancies_est": "29,000+"
                },
                "tech_stack": [
                    "Python / TypeScript", "Playwright", "Cypress", "Pytest",
                    "Postman / Newman", "k6 / JMeter", "Docker", "GitHub Actions", "Allure Report"
                ],
                "pros": [
                    "Найбільш прогнозований та спокійний робочий графік серед інженерних спеціальностей",
                    "М'який та комфортний поріг входження для світчерів",
                    "Висока затребуваність у великих стабільних корпораціях та банках",
                    "Можливість плавно зростати в напрямках Backend чи DevOps"
                ],
                "cons": [
                    "Фінансова стеля помірніша за AI чи Low-level інфраструктуру",
                    "Підтримка застарілих тестових наборів інколи буває рутинною",
                    "Необхідність тісної комунікації та відстоювання стандартів якості перед командою"
                ],
                "roadmap": [
                    {"phase": "Фаза 1: Основи тестування та мова автоматизації", "duration": "4-5 тижнів", "topics": ["Теорія тестування: тест-кейси, баг-репорти, техніки тест-дизайну", "Python або TypeScript: базовий синтаксис, структури даних, функції"]},
                    {"phase": "Фаза 2: Автоматизація API тестування", "duration": "4-5 тижнів", "topics": ["Протокол HTTP, статус-коди, REST API", "Автоматизація запитів: Requests / SuperTest, валідація JSON схем", "Тестові раннери: Pytest, фікстури, параметризація, звіти Allure"]},
                    {"phase": "Фаза 3: UI Автоматизація", "duration": "5-6 тижнів", "topics": ["Сучасний Playwright / Cypress, Page Object Model (POM)", "Селектори, очікування елементів, робота з iFrames та cookies", "Паралельний запуск тестів"]},
                    {"phase": "Фаза 4: CI/CD та Навантажувальне тестування", "duration": "3-4 тижні", "topics": ["Інтеграція тестів у GitHub Actions / GitLab CI", "Тестування продуктивності з k6", "Docker контейнери для запуску тестів у безголовому режимі"]}
                ]
            },
            {
                "slug": "frontend-react",
                "title": "Frontend / React & Next.js Engineer",
                "tagline": "Інтерактивні інтерфейси, клієнтська архітектура та користувацький досвід",
                "category": "Frontend & Web",
                "icon_type": "code",
                "badge_color": "cyan",
                "radar_learning_curve": 4.5,
                "radar_financial_vector": 7.0,
                "radar_architecture_visual": 9.5,
                "radar_company_scale": 7.5,
                "radar_stress_wlb": 4.0,
                "short_desc": "Розробка сучасних веб-додатків на React, TypeScript та Next.js з акцентом на швидкість, анімації та UI/UX.",
                "full_desc": "Frontend розробник створює взаємодію користувача з додатком у браузері. Сучасний фронтенд включає SSR-рендеринг, складні клієнтські стейт-машини, мікроінтеракції та оптимізацію Core Web Vitals.",
                "salaries": {
                    "global": {
                        "junior": "$32,000 - $50,000",
                        "middle": "$60,000 - $90,000",
                        "senior": "$100,000 - $145,000",
                        "lead": "$150,000 - $200,000+",
                        "structured": {
                            "junior": {"min": 32000, "max": 50000, "currency": "USD", "period": "yearly"},
                            "middle": {"min": 60000, "max": 90000, "currency": "USD", "period": "yearly"},
                            "senior": {"min": 100000, "max": 145000, "currency": "USD", "period": "yearly"},
                            "lead": {"min": 150000, "max": 200000, "currency": "USD", "period": "yearly"}
                        }
                    },
                    "usa": {
                        "junior": "$70,000 - $90,000",
                        "middle": "$110,000 - $145,000",
                        "senior": "$155,000 - $210,000",
                        "lead": "$215,000 - $285,000+",
                        "structured": {
                            "junior": {"min": 70000, "max": 90000, "currency": "USD", "period": "yearly"},
                            "middle": {"min": 110000, "max": 145000, "currency": "USD", "period": "yearly"},
                            "senior": {"min": 155000, "max": 210000, "currency": "USD", "period": "yearly"},
                            "lead": {"min": 215000, "max": 285000, "currency": "USD", "period": "yearly"}
                        }
                    },
                    "europe": {
                        "junior": "€35,000 - €48,000",
                        "middle": "€55,000 - €80,000",
                        "senior": "€90,000 - €125,000",
                        "lead": "€130,000 - €170,000+",
                        "structured": {
                            "junior": {"min": 35000, "max": 48000, "currency": "EUR", "period": "yearly"},
                            "middle": {"min": 55000, "max": 80000, "currency": "EUR", "period": "yearly"},
                            "senior": {"min": 90000, "max": 125000, "currency": "EUR", "period": "yearly"},
                            "lead": {"min": 130000, "max": 170000, "currency": "EUR", "period": "yearly"}
                        }
                    },
                    "uk": {
                        "junior": "£30,000 - £42,000",
                        "middle": "£50,000 - £75,000",
                        "senior": "£85,000 - £120,000",
                        "lead": "£125,000 - £165,000+",
                        "structured": {
                            "junior": {"min": 30000, "max": 42000, "currency": "GBP", "period": "yearly"},
                            "middle": {"min": 50000, "max": 75000, "currency": "GBP", "period": "yearly"},
                            "senior": {"min": 85000, "max": 120000, "currency": "GBP", "period": "yearly"},
                            "lead": {"min": 125000, "max": 165000, "currency": "GBP", "period": "yearly"}
                        }
                    },
                    "ukraine": {
                        "junior": "$700 - $1,400 / міс",
                        "middle": "$2,000 - $3,500 / міс",
                        "senior": "$4,000 - $5,800 / міс",
                        "lead": "$6,000 - $7,800+ / міс",
                        "structured": {
                            "junior": {"min": 700, "max": 1400, "currency": "USD", "period": "monthly"},
                            "middle": {"min": 2000, "max": 3500, "currency": "USD", "period": "monthly"},
                            "senior": {"min": 4000, "max": 5800, "currency": "USD", "period": "monthly"},
                            "lead": {"min": 6000, "max": 7800, "currency": "USD", "period": "monthly"}
                        }
                    }
                },
                "market_stats": {
                    "demand_index": 94,
                    "remote_share": "80%",
                    "yoy_growth": "+14.2%",
                    "open_vacancies_est": "60,000+"
                },
                "tech_stack": [
                    "TypeScript", "React 19", "Next.js", "Tailwind CSS",
                    "Zustand / Redux", "TanStack Query", "HTML5 / CSS3", "Vite", "Playwright"
                ],
                "pros": [
                    "Миттєвий візуальний результат своєї праці",
                    "Широкий глобальний ринок праці та віддалених проєктів",
                    "Сучасний типізований стек з високою продуктивністю",
                    "Творчий елемент поєднання дизайну та інженерії"
                ],
                "cons": [
                    "Динамічна зміна інструментів та бібліотек екосистеми",
                    "Кросбраузерні тонкощі та підтримка мобільних веб-вью",
                    "Висока конкуренція серед початківців"
                ],
                "roadmap": [
                    {"phase": "Фаза 1: Фундамент вебу та сучасний JS", "duration": "4-5 тижнів", "topics": ["Семантичний HTML5, CSS Flexbox/Grid, Tailwind CSS", "Сучасний JavaScript ES2024 (проміси, async/await, деструктуризація)", "DOM API, робота з подіями, Fetch API"]},
                    {"phase": "Фаза 2: TypeScript та React Core", "duration": "6-7 тижнів", "topics": ["Основи TypeScript (інтерфейси, generics, типи утиліти)", "Компоненти, хуки (useState, useEffect, useMemo, useCallback)", "Управління станом (Zustand) та робота з формами"]},
                    {"phase": "Фаза 3: Fullstack React & Next.js", "duration": "5-6 тижнів", "topics": ["Next.js App Router, Server Components (RSC), SSR/SSG", "Асинхронний кеш (TanStack Query / React Query)", "Оптимізація швидкодії, Web Vitals, SEO"]},
                    {"phase": "Фаза 4: Тестування та Продакшн", "duration": "3-4 тижні", "topics": ["Unit-тестування (Vitest, React Testing Library)", "E2E тестування з Playwright", "Storybook, CI/CD деплой на Vercel/Cloudflare"]}
                ]
            },
            {
                "slug": "mobile-flutter-ios",
                "title": "Mobile Developer (Flutter / iOS / Android)",
                "tagline": "Мобільні додатки для мільйонів користувачів смартфонів",
                "category": "Mobile Development",
                "icon_type": "mobile",
                "badge_color": "rose",
                "radar_learning_curve": 5.0,
                "radar_financial_vector": 6.8,
                "radar_architecture_visual": 8.0,
                "radar_company_scale": 6.0,
                "radar_stress_wlb": 4.5,
                "short_desc": "Розробка мобільних додатків на Flutter/Dart або Swift/Kotlin з плавною анімацією 120 FPS та роботою з пристроєм.",
                "full_desc": "Мобільний інженер розробляє нативні або кросплатформні додатки: банкінг, e-commerce, сервіси доставки та соціальні мережі. Пріоритетами є автономність, збереження батареї, сенсори та безпека локальних даних.",
                "salaries": {
                    "global": {
                        "junior": "$32,000 - $50,000",
                        "middle": "$60,000 - $90,000",
                        "senior": "$105,000 - $145,000",
                        "lead": "$150,000 - $200,000+",
                        "structured": {
                            "junior": {"min": 32000, "max": 50000, "currency": "USD", "period": "yearly"},
                            "middle": {"min": 60000, "max": 90000, "currency": "USD", "period": "yearly"},
                            "senior": {"min": 105000, "max": 145000, "currency": "USD", "period": "yearly"},
                            "lead": {"min": 150000, "max": 200000, "currency": "USD", "period": "yearly"}
                        }
                    },
                    "usa": {
                        "junior": "$72,000 - $92,000",
                        "middle": "$115,000 - $145,000",
                        "senior": "$160,000 - $215,000",
                        "lead": "$220,000 - $290,000+",
                        "structured": {
                            "junior": {"min": 72000, "max": 92000, "currency": "USD", "period": "yearly"},
                            "middle": {"min": 115000, "max": 145000, "currency": "USD", "period": "yearly"},
                            "senior": {"min": 160000, "max": 215000, "currency": "USD", "period": "yearly"},
                            "lead": {"min": 220000, "max": 290000, "currency": "USD", "period": "yearly"}
                        }
                    },
                    "europe": {
                        "junior": "€36,000 - €48,000",
                        "middle": "€58,000 - €82,000",
                        "senior": "€90,000 - €128,000",
                        "lead": "€135,000 - €175,000+",
                        "structured": {
                            "junior": {"min": 36000, "max": 48000, "currency": "EUR", "period": "yearly"},
                            "middle": {"min": 58000, "max": 82000, "currency": "EUR", "period": "yearly"},
                            "senior": {"min": 90000, "max": 128000, "currency": "EUR", "period": "yearly"},
                            "lead": {"min": 135000, "max": 175000, "currency": "EUR", "period": "yearly"}
                        }
                    },
                    "uk": {
                        "junior": "£32,000 - £45,000",
                        "middle": "£52,000 - £78,000",
                        "senior": "£85,000 - £125,000",
                        "lead": "£130,000 - £170,000+",
                        "structured": {
                            "junior": {"min": 32000, "max": 45000, "currency": "GBP", "period": "yearly"},
                            "middle": {"min": 52000, "max": 78000, "currency": "GBP", "period": "yearly"},
                            "senior": {"min": 85000, "max": 125000, "currency": "GBP", "period": "yearly"},
                            "lead": {"min": 130000, "max": 170000, "currency": "GBP", "period": "yearly"}
                        }
                    },
                    "ukraine": {
                        "junior": "$750 - $1,400 / міс",
                        "middle": "$2,000 - $3,600 / міс",
                        "senior": "$4,200 - $6,000 / міс",
                        "lead": "$6,200 - $8,000+ / міс",
                        "structured": {
                            "junior": {"min": 750, "max": 1400, "currency": "USD", "period": "monthly"},
                            "middle": {"min": 2000, "max": 3600, "currency": "USD", "period": "monthly"},
                            "senior": {"min": 4200, "max": 6000, "currency": "USD", "period": "monthly"},
                            "lead": {"min": 6200, "max": 8000, "currency": "USD", "period": "monthly"}
                        }
                    }
                },
                "market_stats": {
                    "demand_index": 86,
                    "remote_share": "75%",
                    "yoy_growth": "+12.4%",
                    "open_vacancies_est": "32,000+"
                },
                "tech_stack": [
                    "Dart / Flutter", "Swift / SwiftUI", "Kotlin / Compose",
                    "BLoC / Riverpod", "SQLite / Drift", "REST / WebSockets", "Firebase", "Fastlane"
                ],
                "pros": [
                    "Один кодовий фундамент для iOS та Android на Flutter",
                    "Відчутний продукт, доступний на смартфонах реальних користувачів",
                    "Стабільний попит у фінтеху, доставці та комерції",
                    "Чітко визначений життєвий цикл додатків"
                ],
                "cons": [
                    "Процес модерації релізів у App Store та Google Play",
                    "Тестування на різноманітних екранах та версіях ОС",
                    "Для збірок під iOS потрібна macOS інфраструктура"
                ],
                "roadmap": [
                    {"phase": "Фаза 1: Мова програмування та ООП", "duration": "4-5 тижнів", "topics": ["Основи Dart або Swift: типізація, колекції, асинхронність", "ООП, патерни проектування, робота з пам'яттю"]},
                    {"phase": "Фаза 2: Віджети та Архітектура додатку", "duration": "6-7 тижнів", "topics": ["Flutter Widget Tree, адаптивна верстка під будь-який екран", "Керування станом (BLoC / Cubit / Riverpod)", "Навігація (GoRouter), робота з темами"]},
                    {"phase": "Фаза 3: Мережа, Локальна БД та Датчики", "duration": "5-6 тижнів", "topics": ["HTTP запити (Dio), JSON парсинг, WebSockets", "Локальне збереження даних (Hive, Isar, Drift, SQLite)", "Геолокація, камера, Push-повідомлення (Firebase Cloud Messaging)"]},
                    {"phase": "Фаза 4: Реліз в App Store та Google Play", "duration": "3-4 тижні", "topics": ["Автоматизація збірок (Fastlane, CI/CD)", "Підготовка сертифікатів, Provisioning Profiles", "Оптимізація розміру білду та аналітика крешів"]}
                ]
            },
            {
                "slug": "python-backend",
                "title": "Python Backend Engineer",
                "tagline": "Серце серверної архітектури, API, бази даних та мікросервіси",
                "category": "Backend & Cloud",
                "icon_type": "server",
                "badge_color": "emerald",
                "radar_learning_curve": 5.5,
                "radar_financial_vector": 7.8,
                "radar_architecture_visual": 1.8,
                "radar_company_scale": 5.0,
                "radar_stress_wlb": 5.0,
                "short_desc": "Проектування REST/gRPC API, робота з базами даних (PostgreSQL), кешуванням (Redis) та чергами завдань.",
                "full_desc": "Python Backend інженер відповідає за бізнес-логіку серверів, обробку запитів, транзакційну цілісність баз даних та взаємодію сервісів через асинхронні брокери повідомлень.",
                "salaries": {
                    "global": {
                        "junior": "$35,000 - $55,000",
                        "middle": "$65,000 - $95,000",
                        "senior": "$110,000 - $160,000",
                        "lead": "$170,000 - $220,000+",
                        "structured": {
                            "junior": {"min": 35000, "max": 55000, "currency": "USD", "period": "yearly"},
                            "middle": {"min": 65000, "max": 95000, "currency": "USD", "period": "yearly"},
                            "senior": {"min": 110000, "max": 160000, "currency": "USD", "period": "yearly"},
                            "lead": {"min": 170000, "max": 220000, "currency": "USD", "period": "yearly"}
                        }
                    },
                    "usa": {
                        "junior": "$75,000 - $95,000",
                        "middle": "$115,000 - $150,000",
                        "senior": "$165,000 - $225,000",
                        "lead": "$230,000 - $310,000+",
                        "structured": {
                            "junior": {"min": 75000, "max": 95000, "currency": "USD", "period": "yearly"},
                            "middle": {"min": 115000, "max": 150000, "currency": "USD", "period": "yearly"},
                            "senior": {"min": 165000, "max": 225000, "currency": "USD", "period": "yearly"},
                            "lead": {"min": 230000, "max": 310000, "currency": "USD", "period": "yearly"}
                        }
                    },
                    "europe": {
                        "junior": "€38,000 - €50,000",
                        "middle": "€60,000 - €85,000",
                        "senior": "€95,000 - €135,000",
                        "lead": "€140,000 - €180,000+",
                        "structured": {
                            "junior": {"min": 38000, "max": 50000, "currency": "EUR", "period": "yearly"},
                            "middle": {"min": 60000, "max": 85000, "currency": "EUR", "period": "yearly"},
                            "senior": {"min": 95000, "max": 135000, "currency": "EUR", "period": "yearly"},
                            "lead": {"min": 140000, "max": 180000, "currency": "EUR", "period": "yearly"}
                        }
                    },
                    "uk": {
                        "junior": "£32,000 - £45,000",
                        "middle": "£55,000 - £80,000",
                        "senior": "£90,000 - £130,000",
                        "lead": "£135,000 - £175,000+",
                        "structured": {
                            "junior": {"min": 32000, "max": 45000, "currency": "GBP", "period": "yearly"},
                            "middle": {"min": 55000, "max": 80000, "currency": "GBP", "period": "yearly"},
                            "senior": {"min": 90000, "max": 130000, "currency": "GBP", "period": "yearly"},
                            "lead": {"min": 135000, "max": 175000, "currency": "GBP", "period": "yearly"}
                        }
                    },
                    "ukraine": {
                        "junior": "$800 - $1,500 / міс",
                        "middle": "$2,200 - $3,800 / міс",
                        "senior": "$4,500 - $6,500 / міс",
                        "lead": "$6,500 - $8,500+ / міс",
                        "structured": {
                            "junior": {"min": 800, "max": 1500, "currency": "USD", "period": "monthly"},
                            "middle": {"min": 2200, "max": 3800, "currency": "USD", "period": "monthly"},
                            "senior": {"min": 4500, "max": 6500, "currency": "USD", "period": "monthly"},
                            "lead": {"min": 6500, "max": 8500, "currency": "USD", "period": "monthly"}
                        }
                    }
                },
                "market_stats": {
                    "demand_index": 91,
                    "remote_share": "82%",
                    "yoy_growth": "+15.8%",
                    "open_vacancies_est": "45,000+"
                },
                "tech_stack": [
                    "Python 3.12+", "FastAPI", "Django", "PostgreSQL", "Redis",
                    "Docker", "Kafka / RabbitMQ", "SQLAlchemy", "AsyncIO", "AWS"
                ],
                "pros": [
                    "Чистий, читабельний синтаксис та потужна інженерна спільнота",
                    "Простий перехід у сфери Data Engineering та AI/ML сервісів",
                    "Висока частка віддаленої роботи у світових компаніях",
                    "Багата екосистема перевірених продакшн бібліотек"
                ],
                "cons": [
                    "Потребує глибокого розуміння асинхронності та індексів БД",
                    "Динамічна типізація вимагає суворого тестування (Mypy, Pytest)",
                    "Висока конкуренція на стартових позиціях"
                ],
                "roadmap": [
                    {"phase": "Фаза 1: Основи CS та Python Core", "duration": "4-6 тижнів", "topics": ["Синтаксис, ООП, структури даних, алгоритми", "Декоратори, генератори, контекстні менеджери", "Робота з пам'яттю, GIL, тайп-хінти (Mypy)"]},
                    {"phase": "Фаза 2: Бази даних та Архітектура API", "duration": "6-8 тижнів", "topics": ["Реляційні БД (PostgreSQL, індекси, транзакції, ACID)", "ORM & Query Builders (SQLAlchemy, Alembic)", "FastAPI / Django REST Framework, JWT авторизація, OpenAPI"]},
                    {"phase": "Фаза 3: Асинхронність, Кеш та Черги", "duration": "6-8 тижнів", "topics": ["AsyncIO, Event Loop, неблокуючий I/O", "Кешування з Redis, черги завдань Celery / RQ", "Брокери повідомлень Kafka / RabbitMQ"]},
                    {"phase": "Фаза 4: DevOps, Тестування та Продакшн", "duration": "4-6 тижнів", "topics": ["Docker & Docker Compose, CI/CD (GitHub Actions)", "Тестування (Pytest, моки, інтеграційні тести)", "Мікросервісна архітектура, моніторинг (Prometheus, Grafana)"]}
                ]
            },
            {
                "slug": "fullstack-web",
                "title": "Fullstack Web Developer (TS + Node / Python)",
                "tagline": "Універсальний інженер для швидкого створення продуктів під ключ",
                "category": "Software Engineering",
                "icon_type": "code",
                "badge_color": "amber",
                "radar_learning_curve": 6.0,
                "radar_financial_vector": 7.5,
                "radar_architecture_visual": 6.0,
                "radar_company_scale": 9.0,
                "radar_stress_wlb": 6.0,
                "short_desc": "Поєднання клієнтської розробки (React/Next.js) та серверної логіки (Node.js/Python), що ідеально для стартапів.",
                "full_desc": "Fullstack розробник охоплює повний цикл веб-продукту: від схеми БД та безпечного бекенду до інтерактивного UI та розгортання в хмарі.",
                "salaries": {
                    "global": {
                        "junior": "$36,000 - $55,000",
                        "middle": "$65,000 - $95,000",
                        "senior": "$110,000 - $155,000",
                        "lead": "$160,000 - $215,000+",
                        "structured": {
                            "junior": {"min": 36000, "max": 55000, "currency": "USD", "period": "yearly"},
                            "middle": {"min": 65000, "max": 95000, "currency": "USD", "period": "yearly"},
                            "senior": {"min": 110000, "max": 155000, "currency": "USD", "period": "yearly"},
                            "lead": {"min": 160000, "max": 215000, "currency": "USD", "period": "yearly"}
                        }
                    },
                    "usa": {
                        "junior": "$75,000 - $95,000",
                        "middle": "$115,000 - $150,000",
                        "senior": "$165,000 - $225,000",
                        "lead": "$230,000 - $300,000+",
                        "structured": {
                            "junior": {"min": 75000, "max": 95000, "currency": "USD", "period": "yearly"},
                            "middle": {"min": 115000, "max": 150000, "currency": "USD", "period": "yearly"},
                            "senior": {"min": 165000, "max": 225000, "currency": "USD", "period": "yearly"},
                            "lead": {"min": 230000, "max": 300000, "currency": "USD", "period": "yearly"}
                        }
                    },
                    "europe": {
                        "junior": "€40,000 - €52,000",
                        "middle": "€62,000 - €88,000",
                        "senior": "€95,000 - €135,000",
                        "lead": "€140,000 - €185,000+",
                        "structured": {
                            "junior": {"min": 40000, "max": 52000, "currency": "EUR", "period": "yearly"},
                            "middle": {"min": 62000, "max": 88000, "currency": "EUR", "period": "yearly"},
                            "senior": {"min": 95000, "max": 135000, "currency": "EUR", "period": "yearly"},
                            "lead": {"min": 140000, "max": 185000, "currency": "EUR", "period": "yearly"}
                        }
                    },
                    "uk": {
                        "junior": "£35,000 - £48,000",
                        "middle": "£55,000 - £82,000",
                        "senior": "£90,000 - £130,000",
                        "lead": "£135,000 - £175,000+",
                        "structured": {
                            "junior": {"min": 35000, "max": 48000, "currency": "GBP", "period": "yearly"},
                            "middle": {"min": 55000, "max": 82000, "currency": "GBP", "period": "yearly"},
                            "senior": {"min": 90000, "max": 130000, "currency": "GBP", "period": "yearly"},
                            "lead": {"min": 135000, "max": 175000, "currency": "GBP", "period": "yearly"}
                        }
                    },
                    "ukraine": {
                        "junior": "$800 - $1,500 / міс",
                        "middle": "$2,200 - $3,800 / міс",
                        "senior": "$4,200 - $6,200 / міс",
                        "lead": "$6,500 - $8,500+ / міс",
                        "structured": {
                            "junior": {"min": 800, "max": 1500, "currency": "USD", "period": "monthly"},
                            "middle": {"min": 2200, "max": 3800, "currency": "USD", "period": "monthly"},
                            "senior": {"min": 4200, "max": 6200, "currency": "USD", "period": "monthly"},
                            "lead": {"min": 6500, "max": 8500, "currency": "USD", "period": "monthly"}
                        }
                    }
                },
                "market_stats": {
                    "demand_index": 93,
                    "remote_share": "79%",
                    "yoy_growth": "+16.1%",
                    "open_vacancies_est": "68,000+"
                },
                "tech_stack": [
                    "TypeScript", "React / Next.js", "Node.js / Express / NestJS",
                    "PostgreSQL / Prisma", "Tailwind CSS", "Redis", "Docker", "REST / GraphQL", "AWS"
                ],
                "pros": [
                    "Висока автономність: можливість створювати власні стартапи та MVP",
                    "Затребуваність у динамічних стартапах та продуктових студіях",
                    "Широкі перспективи кар'єрного зростання до Tech Lead / CTO",
                    "Відсутність монотонності в роботі"
                ],
                "cons": [
                    "Необхідність орієнтуватися у двох великих доменах (Frontend і Backend)",
                    "Ризик розпорошення уваги без достатньої глибини в кожній частині",
                    "Швидкий темп оновлень інструментів"
                ],
                "roadmap": [
                    {"phase": "Фаза 1: Універсальний TypeScript та Веб-основи", "duration": "4-5 тижнів", "topics": ["Сучасний TypeScript для клієнта і сервера", "HTML5, Tailwind CSS, основи дизайну компонентів"]},
                    {"phase": "Фаза 2: Клієнтська частина (React & Next.js)", "duration": "5-6 тижнів", "topics": ["React хуки, стейт-менеджмент, оптимізація", "Next.js App Router, SSR, клієнтські та серверні форми"]},
                    {"phase": "Фаза 3: Серверна частина та Бази даних", "duration": "6-7 тижнів", "topics": ["Node.js (NestJS / Express) або Python (FastAPI)", "PostgreSQL, моделювання зв'язків, міграції з Prisma/Drizzle", "JWT, OAuth 2.0, безпека API, CORS"]},
                    {"phase": "Фаза 4: Інтеграція, Кешування та Деплой", "duration": "4-5 тижнів", "topics": ["Redis кешування, черги завдань BullMQ", "Docker контейнеризація, CI/CD деплой у хмару"]}
                ]
            },
            {
                "slug": "data-engineer",
                "title": "Data Engineer & Big Data",
                "tagline": "Пайплайни даних, озера даних та обробка великих терабайтних потоків",
                "category": "Data & Cloud",
                "icon_type": "server",
                "badge_color": "indigo",
                "radar_learning_curve": 7.5,
                "radar_financial_vector": 8.8,
                "radar_architecture_visual": 1.5,
                "radar_company_scale": 3.0,
                "radar_stress_wlb": 5.5,
                "short_desc": "Проектування сховищ даних (DWH, Snowflake), розподілена обробка (Apache Spark, Kafka) та оркестрація пайплайнів (Airflow).",
                "full_desc": "Data Engineer будує магістралі даних для аналітики та AI. Фахівець забезпечує ETL/ELT процеси, стабільність потоків і якість збереження корпоративних даних.",
                "salaries": {
                    "global": {
                        "junior": "$38,000 - $60,000",
                        "middle": "$72,000 - $105,000",
                        "senior": "$120,000 - $170,000",
                        "lead": "$175,000 - $235,000+",
                        "structured": {
                            "junior": {"min": 38000, "max": 60000, "currency": "USD", "period": "yearly"},
                            "middle": {"min": 72000, "max": 105000, "currency": "USD", "period": "yearly"},
                            "senior": {"min": 120000, "max": 170000, "currency": "USD", "period": "yearly"},
                            "lead": {"min": 175000, "max": 235000, "currency": "USD", "period": "yearly"}
                        }
                    },
                    "usa": {
                        "junior": "$80,000 - $105,000",
                        "middle": "$125,000 - $160,000",
                        "senior": "$170,000 - $240,000",
                        "lead": "$240,000 - $320,000+",
                        "structured": {
                            "junior": {"min": 80000, "max": 105000, "currency": "USD", "period": "yearly"},
                            "middle": {"min": 125000, "max": 160000, "currency": "USD", "period": "yearly"},
                            "senior": {"min": 170000, "max": 240000, "currency": "USD", "period": "yearly"},
                            "lead": {"min": 240000, "max": 320000, "currency": "USD", "period": "yearly"}
                        }
                    },
                    "europe": {
                        "junior": "€42,000 - €56,000",
                        "middle": "€68,000 - €92,000",
                        "senior": "€105,000 - €145,000",
                        "lead": "€148,000 - €190,000+",
                        "structured": {
                            "junior": {"min": 42000, "max": 56000, "currency": "EUR", "period": "yearly"},
                            "middle": {"min": 68000, "max": 92000, "currency": "EUR", "period": "yearly"},
                            "senior": {"min": 105000, "max": 145000, "currency": "EUR", "period": "yearly"},
                            "lead": {"min": 148000, "max": 190000, "currency": "EUR", "period": "yearly"}
                        }
                    },
                    "uk": {
                        "junior": "£36,000 - £50,000",
                        "middle": "£62,000 - £88,000",
                        "senior": "£95,000 - £140,000",
                        "lead": "£145,000 - £185,000+",
                        "structured": {
                            "junior": {"min": 36000, "max": 50000, "currency": "GBP", "period": "yearly"},
                            "middle": {"min": 62000, "max": 88000, "currency": "GBP", "period": "yearly"},
                            "senior": {"min": 95000, "max": 140000, "currency": "GBP", "period": "yearly"},
                            "lead": {"min": 145000, "max": 185000, "currency": "GBP", "period": "yearly"}
                        }
                    },
                    "ukraine": {
                        "junior": "$900 - $1,700 / міс",
                        "middle": "$2,500 - $4,200 / міс",
                        "senior": "$4,800 - $7,000 / міс",
                        "lead": "$7,000 - $9,200+ / міс",
                        "structured": {
                            "junior": {"min": 900, "max": 1700, "currency": "USD", "period": "monthly"},
                            "middle": {"min": 2500, "max": 4200, "currency": "USD", "period": "monthly"},
                            "senior": {"min": 4800, "max": 7000, "currency": "USD", "period": "monthly"},
                            "lead": {"min": 7000, "max": 9200, "currency": "USD", "period": "monthly"}
                        }
                    }
                },
                "market_stats": {
                    "demand_index": 92,
                    "remote_share": "81%",
                    "yoy_growth": "+19.4%",
                    "open_vacancies_est": "39,000+"
                },
                "tech_stack": [
                    "Python / SQL (Advanced)", "Apache Spark", "Apache Kafka",
                    "Apache Airflow", "Snowflake / BigQuery", "dbt", "Docker", "AWS S3 / GCP"
                ],
                "pros": [
                    "Фундаментальна роль для роботи аналітичних та AI систем",
                    "Висока стабільність довгострокових контрактів",
                    "Гідна компенсація вже на Middle рівні",
                    "Глибоке розуміння розподілених систем"
                ],
                "cons": [
                    "Потрібне віртуозне володіння складними SQL-оптимізаціями",
                    "Нічні збої у важких ETL процесах",
                    "Робота повністю за лаштунками інтерфейсу"
                ],
                "roadmap": [
                    {"phase": "Фаза 1: Advanced SQL & Data Modeling", "duration": "5-6 тижнів", "topics": ["Віконні функції, оптимізація планів виконання (EXPLAIN ANALYZE)", "Моделювання даних: зірка, сніжинка, Data Vault, повільно змінювані виміри (SCD)", "Python для інженерії даних"]},
                    {"phase": "Фаза 2: Розподілена обробка (Big Data)", "duration": "6-7 тижнів", "topics": ["Apache Spark архітектура: RDD, DataFrames, партиціонування", "PySpark оптимізація пам'яті, shuffle, broadcast joins", "Робота з форматами Parquet, Delta Lake"]},
                    {"phase": "Фаза 3: Потокова передача та Оркестрація", "duration": "5-6 тижнів", "topics": ["Стрімінг з Apache Kafka (topics, partitions, consumer groups)", "Оркестрація пайплайнів з Apache Airflow (DAGs, operators, sensors)", "Трансформація даних з dbt"]},
                    {"phase": "Фаза 4: Хмарні DWH та Data Lakehouse", "duration": "4-5 тижнів", "topics": ["Snowflake / Google BigQuery / Databricks", "CI/CD для даних (DataOps), валідація якості даних (Great Expectations)"]}
                ]
            },
            {
                "slug": "devops-cloud",
                "title": "DevOps & Cloud Architect",
                "tagline": "Автоматизація інфраструктури, хмари та безперебійна доставка коду",
                "category": "Infrastructure & Cloud",
                "icon_type": "cloud",
                "badge_color": "sky",
                "radar_learning_curve": 8.0,
                "radar_financial_vector": 9.2,
                "radar_architecture_visual": 1.2,
                "radar_company_scale": 4.0,
                "radar_stress_wlb": 8.0,
                "short_desc": "Побудова CI/CD конвеєрів, оркестрація Kubernetes, Infrastructure as Code (Terraform) та хмари AWS/Azure/GCP.",
                "full_desc": "DevOps інженер об'єднує розробку та експлуатацію. Мета — зробити випуск коду надійним і масштабованим, а інфраструктуру — відмовостійкою (High Availability).",
                "salaries": {
                    "global": {
                        "junior": "$42,000 - $65,000",
                        "middle": "$75,000 - $110,000",
                        "senior": "$125,000 - $175,000",
                        "lead": "$180,000 - $240,000+",
                        "structured": {
                            "junior": {"min": 42000, "max": 65000, "currency": "USD", "period": "yearly"},
                            "middle": {"min": 75000, "max": 110000, "currency": "USD", "period": "yearly"},
                            "senior": {"min": 125000, "max": 175000, "currency": "USD", "period": "yearly"},
                            "lead": {"min": 180000, "max": 240000, "currency": "USD", "period": "yearly"}
                        }
                    },
                    "usa": {
                        "junior": "$85,000 - $110,000",
                        "middle": "$130,000 - $165,000",
                        "senior": "$175,000 - $245,000",
                        "lead": "$250,000 - $330,000+",
                        "structured": {
                            "junior": {"min": 85000, "max": 110000, "currency": "USD", "period": "yearly"},
                            "middle": {"min": 130000, "max": 165000, "currency": "USD", "period": "yearly"},
                            "senior": {"min": 175000, "max": 245000, "currency": "USD", "period": "yearly"},
                            "lead": {"min": 250000, "max": 330000, "currency": "USD", "period": "yearly"}
                        }
                    },
                    "europe": {
                        "junior": "€45,000 - €60,000",
                        "middle": "€70,000 - €95,000",
                        "senior": "€105,000 - €145,000",
                        "lead": "€150,000 - €195,000+",
                        "structured": {
                            "junior": {"min": 45000, "max": 60000, "currency": "EUR", "period": "yearly"},
                            "middle": {"min": 70000, "max": 95000, "currency": "EUR", "period": "yearly"},
                            "senior": {"min": 105000, "max": 145000, "currency": "EUR", "period": "yearly"},
                            "lead": {"min": 150000, "max": 195000, "currency": "EUR", "period": "yearly"}
                        }
                    },
                    "uk": {
                        "junior": "£40,000 - £55,000",
                        "middle": "£65,000 - £90,000",
                        "senior": "£100,000 - £145,000",
                        "lead": "£150,000 - £190,000+",
                        "structured": {
                            "junior": {"min": 40000, "max": 55000, "currency": "GBP", "period": "yearly"},
                            "middle": {"min": 65000, "max": 90000, "currency": "GBP", "period": "yearly"},
                            "senior": {"min": 100000, "max": 145000, "currency": "GBP", "period": "yearly"},
                            "lead": {"min": 150000, "max": 190000, "currency": "GBP", "period": "yearly"}
                        }
                    },
                    "ukraine": {
                        "junior": "$1,000 - $1,800 / міс",
                        "middle": "$2,800 - $4,500 / міс",
                        "senior": "$5,000 - $7,500 / міс",
                        "lead": "$7,500 - $10,000+ / міс",
                        "structured": {
                            "junior": {"min": 1000, "max": 1800, "currency": "USD", "period": "monthly"},
                            "middle": {"min": 2800, "max": 4500, "currency": "USD", "period": "monthly"},
                            "senior": {"min": 5000, "max": 7500, "currency": "USD", "period": "monthly"},
                            "lead": {"min": 7500, "max": 10000, "currency": "USD", "period": "monthly"}
                        }
                    }
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
                    "Один із найвищих показників зарплат та затребуваності в індустрії",
                    "Висока автономність та архітектурний вплив на інфраструктуру",
                    "Мінімальний ризик автоматизації простими моделями",
                    "Широкі перспективи консалтингу та контрактів"
                ],
                "cons": [
                    "Висока відповідальність (критичні аварії на продакшні)",
                    "On-call ротації та можливі термінові нічні виклики",
                    "Високий поріг входження в мережі, ядра ОС та безпеку"
                ],
                "roadmap": [
                    {"phase": "Фаза 1: Системні основи та мережі", "duration": "5-6 тижнів", "topics": ["Linux адміністрування (ядро, пам'ять, процеси, permissions)", "Комп'ютерні мережі: TCP/IP, DNS, SSL/TLS, HTTP/2, VPN, підмережі", "Bash скрипти та автоматизація на Python/Go"]},
                    {"phase": "Фаза 2: Контейнеризація та CI/CD", "duration": "6-7 тижнів", "topics": ["Docker: оптимізація образів, multi-stage збірки, безпека", "CI/CD: GitHub Actions, GitLab CI (пайплайни, артефакти, secrets)"]},
                    {"phase": "Фаза 3: Оркестрація та Хмари", "duration": "7-8 тижнів", "topics": ["Kubernetes: Pods, Services, Deployments, Ingress, Helm", "Хмарний провайдер (AWS або GCP): IAM, VPC, EKS, RDS, S3"]},
                    {"phase": "Фаза 4: IaC, GitOps та Observability", "duration": "5-6 тижнів", "topics": ["Terraform: модулі, remote state, Infrastructure as Code", "GitOps (ArgoCD, Flux)", "Моніторинг: Prometheus, Grafana, Alertmanager, Loki, OpenTelemetry"]}
                ]
            },
            {
                "slug": "game-dev",
                "title": "Game Developer (C++ / Unreal / Unity)",
                "tagline": "Віртуальні світи, комп'ютерна графіка, фізика та ігровий процес",
                "category": "Gaming & Simulation",
                "icon_type": "game",
                "badge_color": "purple",
                "radar_learning_curve": 8.2,
                "radar_financial_vector": 5.8,
                "radar_architecture_visual": 9.0,
                "radar_company_scale": 6.5,
                "radar_stress_wlb": 8.5,
                "short_desc": "Програмування механік, AI супротивників, рендерингу шейдерів та фізики на C++ (Unreal Engine) або C# (Unity).",
                "full_desc": "Розробник ігор поєднує низькорівневу оптимізацію пам'яті, лінійну алгебру (матриці, кватерніони), графічні конвеєри та художнє бачення інтерактивних світів.",
                "salaries": {
                    "global": {
                        "junior": "$30,000 - $48,000",
                        "middle": "$55,000 - $82,000",
                        "senior": "$95,000 - $140,000",
                        "lead": "$145,000 - $190,000+",
                        "structured": {
                            "junior": {"min": 30000, "max": 48000, "currency": "USD", "period": "yearly"},
                            "middle": {"min": 55000, "max": 82000, "currency": "USD", "period": "yearly"},
                            "senior": {"min": 95000, "max": 140000, "currency": "USD", "period": "yearly"},
                            "lead": {"min": 145000, "max": 190000, "currency": "USD", "period": "yearly"}
                        }
                    },
                    "usa": {
                        "junior": "$65,000 - $85,000",
                        "middle": "$95,000 - $135,000",
                        "senior": "$145,000 - $200,000",
                        "lead": "$205,000 - $275,000+",
                        "structured": {
                            "junior": {"min": 65000, "max": 85000, "currency": "USD", "period": "yearly"},
                            "middle": {"min": 95000, "max": 135000, "currency": "USD", "period": "yearly"},
                            "senior": {"min": 145000, "max": 200000, "currency": "USD", "period": "yearly"},
                            "lead": {"min": 205000, "max": 275000, "currency": "USD", "period": "yearly"}
                        }
                    },
                    "europe": {
                        "junior": "€32,000 - €45,000",
                        "middle": "€50,000 - €75,000",
                        "senior": "€85,000 - €120,000",
                        "lead": "€125,000 - €165,000+",
                        "structured": {
                            "junior": {"min": 32000, "max": 45000, "currency": "EUR", "period": "yearly"},
                            "middle": {"min": 50000, "max": 75000, "currency": "EUR", "period": "yearly"},
                            "senior": {"min": 85000, "max": 120000, "currency": "EUR", "period": "yearly"},
                            "lead": {"min": 125000, "max": 165000, "currency": "EUR", "period": "yearly"}
                        }
                    },
                    "uk": {
                        "junior": "£28,000 - £40,000",
                        "middle": "£48,000 - £72,000",
                        "senior": "£80,000 - £118,000",
                        "lead": "£120,000 - £160,000+",
                        "structured": {
                            "junior": {"min": 28000, "max": 40000, "currency": "GBP", "period": "yearly"},
                            "middle": {"min": 48000, "max": 72000, "currency": "GBP", "period": "yearly"},
                            "senior": {"min": 80000, "max": 118000, "currency": "GBP", "period": "yearly"},
                            "lead": {"min": 120000, "max": 160000, "currency": "GBP", "period": "yearly"}
                        }
                    },
                    "ukraine": {
                        "junior": "$600 - $1,200 / міс",
                        "middle": "$1,700 - $3,200 / міс",
                        "senior": "$3,800 - $5,500 / міс",
                        "lead": "$5,500 - $7,500+ / міс",
                        "structured": {
                            "junior": {"min": 600, "max": 1200, "currency": "USD", "period": "monthly"},
                            "middle": {"min": 1700, "max": 3200, "currency": "USD", "period": "monthly"},
                            "senior": {"min": 3800, "max": 5500, "currency": "USD", "period": "monthly"},
                            "lead": {"min": 5500, "max": 7500, "currency": "USD", "period": "monthly"}
                        }
                    }
                },
                "market_stats": {
                    "demand_index": 80,
                    "remote_share": "68%",
                    "yoy_growth": "+9.5%",
                    "open_vacancies_est": "24,000+"
                },
                "tech_stack": [
                    "C++ / C#", "Unreal Engine 5", "Unity",
                    "HLSL / Shaders", "3D Math & Physics", "Git LFS", "Networking", "DirectX / Vulkan"
                ],
                "pros": [
                    "Максимальний творчий драйв: створення емоцій для мільйонів гравців",
                    "Глибокі інженерні знання роботи заліза та GPU конвеєрів",
                    "Можливість запуску власних інді-ігор у Steam/Epic",
                    "Робота на перетині мистецтва, фізики та чистого коду"
                ],
                "cons": [
                    "Культура дедлайнів перед великими релізами ігор",
                    "Фінансові вилки дещо нижчі за фінтех та хмарні сервіси",
                    "Великі обсяги білдів та вимогливість до потужності робочих станцій"
                ],
                "roadmap": [
                    {"phase": "Фаза 1: Мова програмування та 3D Математика", "duration": "5-6 тижнів", "topics": ["C++20 (вказівники, посилання, керування пам'яттю, RAII, шаблони)", "Векторна алгебра, скалярний/векторний добуток, матриці, кватерніони"]},
                    {"phase": "Фаза 2: Рушій та Ігровий цикл", "duration": "6-7 тижнів", "topics": ["Unreal Engine 5 архітектура: Actors, Components, Blueprints & C++ зв'язка", "Game Loop, фізичні колізії, raycasting, анімаційні стейт-машини"]},
                    {"phase": "Фаза 3: Штучний інтелект та Графіка", "duration": "6-7 тижнів", "topics": ["Ігровий AI: Behavior Trees, Blackboard, Navigation Mesh", "Шейдери (HLSL), матеріали, освітлення Lumen, оптимізація Nanite"]},
                    {"phase": "Фаза 4: Мережевий код та Профайлінг", "duration": "5-6 тижнів", "topics": ["Мультиплеєр: реплікація змінних, RPC, компенсація лагу", "Профайлінг пам'яті та кадрів (Unreal Insights), оптимізація draw calls"]}
                ]
            },
            {
                "slug": "cybersecurity",
                "title": "Cybersecurity & InfoSec Specialist",
                "tagline": "Захист цифрових систем, пентестинг та протидія кіберзагрозам",
                "category": "Security & Defense",
                "icon_type": "shield",
                "badge_color": "rose",
                "radar_learning_curve": 8.8,
                "radar_financial_vector": 9.0,
                "radar_architecture_visual": 1.0,
                "radar_company_scale": 1.8,
                "radar_stress_wlb": 9.0,
                "short_desc": "Аналіз вразливостей, етичний хакінг (Red Team), побудова захисту (Blue Team) та моніторинг інцидентів.",
                "full_desc": "Фахівець з кібербезпеки захищає критичну інфраструктуру, мережі та дані бізнесу чи держави. Сфера охоплює етичний хакінг, реверс-інжиніринг, розслідування інцидентів (SOC) та дотримання стандартів.",
                "salaries": {
                    "global": {
                        "junior": "$42,000 - $65,000",
                        "middle": "$75,000 - $115,000",
                        "senior": "$130,000 - $185,000",
                        "lead": "$190,000 - $260,000+",
                        "structured": {
                            "junior": {"min": 42000, "max": 65000, "currency": "USD", "period": "yearly"},
                            "middle": {"min": 75000, "max": 115000, "currency": "USD", "period": "yearly"},
                            "senior": {"min": 130000, "max": 185000, "currency": "USD", "period": "yearly"},
                            "lead": {"min": 190000, "max": 260000, "currency": "USD", "period": "yearly"}
                        }
                    },
                    "usa": {
                        "junior": "$85,000 - $110,000",
                        "middle": "$135,000 - $175,000",
                        "senior": "$180,000 - $260,000",
                        "lead": "$260,000 - $350,000+",
                        "structured": {
                            "junior": {"min": 85000, "max": 110000, "currency": "USD", "period": "yearly"},
                            "middle": {"min": 135000, "max": 175000, "currency": "USD", "period": "yearly"},
                            "senior": {"min": 180000, "max": 260000, "currency": "USD", "period": "yearly"},
                            "lead": {"min": 260000, "max": 350000, "currency": "USD", "period": "yearly"}
                        }
                    },
                    "europe": {
                        "junior": "€45,000 - €60,000",
                        "middle": "€70,000 - €100,000",
                        "senior": "€110,000 - €155,000",
                        "lead": "€160,000 - €210,000+",
                        "structured": {
                            "junior": {"min": 45000, "max": 60000, "currency": "EUR", "period": "yearly"},
                            "middle": {"min": 70000, "max": 100000, "currency": "EUR", "period": "yearly"},
                            "senior": {"min": 110000, "max": 155000, "currency": "EUR", "period": "yearly"},
                            "lead": {"min": 160000, "max": 210000, "currency": "EUR", "period": "yearly"}
                        }
                    },
                    "uk": {
                        "junior": "£38,000 - £55,000",
                        "middle": "£65,000 - £95,000",
                        "senior": "£105,000 - £150,000",
                        "lead": "£155,000 - £205,000+",
                        "structured": {
                            "junior": {"min": 38000, "max": 55000, "currency": "GBP", "period": "yearly"},
                            "middle": {"min": 65000, "max": 95000, "currency": "GBP", "period": "yearly"},
                            "senior": {"min": 105000, "max": 150000, "currency": "GBP", "period": "yearly"},
                            "lead": {"min": 155000, "max": 205000, "currency": "GBP", "period": "yearly"}
                        }
                    },
                    "ukraine": {
                        "junior": "$900 - $1,700 / міс",
                        "middle": "$2,500 - $4,200 / міс",
                        "senior": "$4,800 - $7,200 / міс",
                        "lead": "$7,000 - $10,000+ / міс",
                        "structured": {
                            "junior": {"min": 900, "max": 1700, "currency": "USD", "period": "monthly"},
                            "middle": {"min": 2500, "max": 4200, "currency": "USD", "period": "monthly"},
                            "senior": {"min": 4800, "max": 7200, "currency": "USD", "period": "monthly"},
                            "lead": {"min": 7000, "max": 10000, "currency": "USD", "period": "monthly"}
                        }
                    }
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
                    "Cloud Security", "OWASP Top 10"
                ],
                "pros": [
                    "Критична важливість: бюджети на безпеку захищені від кризових скорочень",
                    "Високий міжнародний авторитет та стабільність",
                    "Надзвичайно цікава сфера для дослідників та реверсерів",
                    "Високі зарплатні вилки у банках та корпораціях"
                ],
                "cons": [
                    "Високий рівень стресу при інцидентах та атаках 0-day",
                    "Необхідність знати системи від фізичного рівня до прикладного коду",
                    "Часто вимагаються дорогі професійні сертифікати (OSCP, CISSP)"
                ],
                "roadmap": [
                    {"phase": "Фаза 1: Фундамент мереж та систем", "duration": "6-7 тижнів", "topics": ["Мережеві протоколи в деталях: DNS, BGP, ARP, TCP/UDP, TLS handshakes", "Аналіз трафіку з Wireshark, tcpdump", "Linux ядро, системні виклики, пам'ять"]},
                    {"phase": "Фаза 2: Веб-безпека та вразливості", "duration": "5-6 тижнів", "topics": ["OWASP Top 10 (SQLi, XSS, CSRF, SSRF, IDOR)", "Практика з Burp Suite, аудит веб-додатків", "Платформи PortSwigger Web Security Academy & TryHackMe"]},
                    {"phase": "Фаза 3: Blue Team & Моніторинг", "duration": "6-7 тижнів", "topics": ["SIEM системи (Splunk, Elastic SIEM, Wazuh)", "Аналіз логів, детекція аномалій, правила Sigma/YARA", "Incident Response та цифрова криміналістика (Forensics)"]},
                    {"phase": "Фаза 4: Хмарна безпека та Пентестинг", "duration": "5-6 тижнів", "topics": ["Cloud Security (AWS Security Hub, Kubernetes Pod Security)", "Етичний пентестинг, Metasploit, Privilege Escalation", "Підготовка до сертифікацій (CompTIA Security+ / eJPT / OSCP)"]}
                ]
            },
            {
                "slug": "data-science-ai",
                "title": "Data Scientist & AI/ML Engineer",
                "tagline": "Штучний інтелект, нейромережі, LLM та вища математика",
                "category": "Data & AI",
                "icon_type": "cpu",
                "badge_color": "purple",
                "radar_learning_curve": 9.5,
                "radar_financial_vector": 9.8,
                "radar_architecture_visual": 3.0,
                "radar_company_scale": 6.5,
                "radar_stress_wlb": 6.5,
                "short_desc": "Навчання нейромереж, побудова RAG систем для LLM, математичний аналіз великих даних за допомогою PyTorch.",
                "full_desc": "Фахівець з AI/ML розробляє прогнозні моделі, мовні моделі (LLM), алгоритми комп'ютерного зору (CV) та обробку природної мови (NLP). Поєднує вищу математику, статистику та інженерію коду.",
                "salaries": {
                    "global": {
                        "junior": "$45,000 - $70,000",
                        "middle": "$80,000 - $125,000",
                        "senior": "$135,000 - $195,000",
                        "lead": "$200,000 - $280,000+",
                        "structured": {
                            "junior": {"min": 45000, "max": 70000, "currency": "USD", "period": "yearly"},
                            "middle": {"min": 80000, "max": 125000, "currency": "USD", "period": "yearly"},
                            "senior": {"min": 135000, "max": 195000, "currency": "USD", "period": "yearly"},
                            "lead": {"min": 200000, "max": 280000, "currency": "USD", "period": "yearly"}
                        }
                    },
                    "usa": {
                        "junior": "$95,000 - $125,000",
                        "middle": "$145,000 - $190,000",
                        "senior": "$200,000 - $290,000",
                        "lead": "$300,000 - $420,000+",
                        "structured": {
                            "junior": {"min": 95000, "max": 125000, "currency": "USD", "period": "yearly"},
                            "middle": {"min": 145000, "max": 190000, "currency": "USD", "period": "yearly"},
                            "senior": {"min": 200000, "max": 290000, "currency": "USD", "period": "yearly"},
                            "lead": {"min": 300000, "max": 420000, "currency": "USD", "period": "yearly"}
                        }
                    },
                    "europe": {
                        "junior": "€48,000 - €65,000",
                        "middle": "€75,000 - €105,000",
                        "senior": "€115,000 - €160,000",
                        "lead": "€170,000 - €230,000+",
                        "structured": {
                            "junior": {"min": 48000, "max": 65000, "currency": "EUR", "period": "yearly"},
                            "middle": {"min": 75000, "max": 105000, "currency": "EUR", "period": "yearly"},
                            "senior": {"min": 115000, "max": 160000, "currency": "EUR", "period": "yearly"},
                            "lead": {"min": 170000, "max": 230000, "currency": "EUR", "period": "yearly"}
                        }
                    },
                    "uk": {
                        "junior": "£42,000 - £60,000",
                        "middle": "£70,000 - £100,000",
                        "senior": "£110,000 - £160,000",
                        "lead": "£165,000 - £220,000+",
                        "structured": {
                            "junior": {"min": 42000, "max": 60000, "currency": "GBP", "period": "yearly"},
                            "middle": {"min": 70000, "max": 100000, "currency": "GBP", "period": "yearly"},
                            "senior": {"min": 110000, "max": 160000, "currency": "GBP", "period": "yearly"},
                            "lead": {"min": 165000, "max": 220000, "currency": "GBP", "period": "yearly"}
                        }
                    },
                    "ukraine": {
                        "junior": "$1,000 - $1,900 / міс",
                        "middle": "$2,800 - $4,800 / міс",
                        "senior": "$5,200 - $8,000 / міс",
                        "lead": "$8,000 - $12,000+ / міс",
                        "structured": {
                            "junior": {"min": 1000, "max": 1900, "currency": "USD", "period": "monthly"},
                            "middle": {"min": 2800, "max": 4800, "currency": "USD", "period": "monthly"},
                            "senior": {"min": 5200, "max": 8000, "currency": "USD", "period": "monthly"},
                            "lead": {"min": 8000, "max": 12000, "currency": "USD", "period": "monthly"}
                        }
                    }
                },
                "market_stats": {
                    "demand_index": 98,
                    "remote_share": "76%",
                    "yoy_growth": "+34.5%",
                    "open_vacancies_est": "52,000+"
                },
                "tech_stack": [
                    "Python", "PyTorch", "Hugging Face", "LangChain / LlamaIndex",
                    "Pandas & NumPy", "Scikit-Learn", "Vector DBs", "MLflow", "Docker", "SQL"
                ],
                "pros": [
                    "Найбільш швидкозростаючий технологічний сегмент у світі",
                    "Максимальні верхні ліміти компенсацій та опціонів",
                    "Робота на передовій наукового та технологічного прогресу",
                    "Високий інтелектуальний драйв у вирішенні складних задач"
                ],
                "cons": [
                    "Вимагає сильної бази лінійної алгебри та теорії ймовірностей",
                    "Висока невизначеність результатів тренування моделей",
                    "Витрати на дорогу обчислювальну інфраструктуру (GPU кластери)"
                ],
                "roadmap": [
                    {"phase": "Фаза 1: Математика та аналіз даних", "duration": "6-8 тижнів", "topics": ["Лінійна алгебра, матриці, градієнтний спуск", "Теорія ймовірностей, математична статистика", "Pandas, NumPy, очищення та аналіз даних (EDA)"]},
                    {"phase": "Фаза 2: Класичне машинне навчання", "duration": "5-6 тижнів", "topics": ["Лінійна та логістична регресія, дерева рішень, Random Forest", "Градієнтний бустинг (XGBoost, LightGBM, CatBoost)", "Метрики якості (ROC-AUC, F1, RMSE), крос-валідація"]},
                    {"phase": "Фаза 3: Deep Learning & PyTorch", "duration": "7-8 тижнів", "topics": ["Архітектури нейромереж: MLP, CNN, RNN/LSTM, Transformers", "Фреймворк PyTorch, функції втрат, оптимізатори (AdamW)", "Hugging Face екосистема, токенізація, претреновані моделі"]},
                    {"phase": "Фаза 4: Сучасний GenAI, RAG та MLOps", "duration": "6-7 тижнів", "topics": ["Побудова RAG (Retrieval-Augmented Generation), векторні бази (Pinecone/Qdrant)", "Fine-tuning моделей (LoRA/QLoRA), квантизація", "MLOps пайплайни (MLflow, Docker, FastAPI для AI сервісів)"]}
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
