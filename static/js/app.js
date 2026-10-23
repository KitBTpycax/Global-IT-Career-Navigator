/**
 * Global IT Career Navigator - Frontend Application Logic
 * Deep Graphite & Noble Cherry (Crimson) Palette
 * Custom dynamic range sliders with live gradient tracks and fluid micro-animations.
 * Chart.js Radar with strict 1-10 scale and clear step graduation.
 */

document.addEventListener('DOMContentLoaded', () => {
    // Ініціалізація компонентів залежно від поточної сторінки
    if (document.getElementById('priorityRadarChart')) {
        initNavigatorPage();
    }

    if (document.getElementById('detailRadarChart')) {
        initDetailPage();
    }

    initGlobalRegionSync();
});

// ==============================================================================
// 1. Логіка Головної Сторінки: Кастомні Слайдери, Радар (шкала 1-10), DSS
// ==============================================================================

let priorityRadar = null;
let matchDebounceTimer = null;

const SLIDERS = [
    { id: 'slider_learning_curve', valId: 'val_learning_curve', key: 'learning_curve', label: 'CS & Теорія' },
    { id: 'slider_financial_vector', valId: 'val_financial_vector', key: 'financial_vector', label: 'Фінансова стеля' },
    { id: 'slider_architecture_visual', valId: 'val_architecture_visual', key: 'architecture_visual', label: 'Візуал / UI-UX' },
    { id: 'slider_company_scale', valId: 'val_company_scale', key: 'company_scale', label: 'Стартапи vs Корп' },
    { id: 'slider_stress_wlb', valId: 'val_stress_wlb', key: 'stress_wlb', label: 'Драйв & Стрес' }
];

function initNavigatorPage() {
    setupRadarChart();
    setupSliderListeners();
    setupPresetButtons();
    setupResetButton();
    setupCatalogToggle();

    // Початкове оновлення градієнтних треків слайдерів
    initSliderTracks();

    // Початковий розрахунок із дефолтними значеннями
    triggerMatchCalculation();
}

/**
 * Ініціалізація та налаштування інтерактивного Chart.js Radar
 * у глибокій графітово-вишневій палітрі зі шкалою 0-10
 */
function setupRadarChart() {
    const canvas = document.getElementById('priorityRadarChart');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    const initialValues = SLIDERS.map(s => {
        const el = document.getElementById(s.id);
        return el ? parseFloat(el.value) : 5.0;
    });

    priorityRadar = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: [
                'CS & Теорія',
                'Фінансова стеля',
                'Візуал / UI-UX',
                'Стартапи & Свобода',
                'Драйв & Стрес'
            ],
            datasets: [
                {
                    label: 'Ваш вектор пріоритетів',
                    data: initialValues,
                    backgroundColor: 'rgba(190, 18, 60, 0.28)', // Шляхетний вишневий (Noble Cherry)
                    borderColor: '#be123c',
                    pointBackgroundColor: '#fb7185',
                    pointBorderColor: '#0b0d12',
                    pointHoverBackgroundColor: '#ffffff',
                    pointHoverBorderColor: '#e11d48',
                    pointRadius: 4.5,
                    pointHoverRadius: 6.5,
                    borderWidth: 2.2
                },
                {
                    label: 'Еталон Топ-1 треку',
                    data: [5, 5, 5, 5, 5],
                    backgroundColor: 'rgba(148, 163, 184, 0.08)', // Стриманий графітовий
                    borderColor: 'rgba(148, 163, 184, 0.55)',
                    borderDash: [4, 4],
                    pointBackgroundColor: '#94a3b8',
                    pointBorderColor: '#0b0d12',
                    pointRadius: 3,
                    borderWidth: 1.5,
                    hidden: false
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            animation: {
                duration: 250
            },
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#9fa5b4',
                        font: {
                            family: "'Inter', sans-serif",
                            size: 11
                        },
                        boxWidth: 12,
                        padding: 14
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(16, 19, 26, 0.96)',
                    titleColor: '#fda4af',
                    bodyColor: '#e4e6ea',
                    borderColor: '#2b2f3a',
                    borderWidth: 1,
                    padding: 9,
                    bodyFont: { family: "'JetBrains Mono', monospace" }
                }
            },
            scales: {
                r: {
                    min: 0,
                    max: 10,
                    beginAtZero: true,
                    ticks: {
                        stepSize: 2,         // Кроки: 0, 2, 4, 6, 8, 10
                        display: true,       // Чітка видимість градації
                        color: '#757c8e',    // Графітовий відтінок міток
                        backdropColor: 'transparent',
                        font: {
                            family: "'JetBrains Mono', monospace",
                            size: 10,
                            weight: '500'
                        },
                        z: 2
                    },
                    angleLines: {
                        display: true,
                        color: 'rgba(255, 255, 255, 0.08)',
                        lineWidth: 1
                    },
                    grid: {
                        display: true,
                        color: 'rgba(255, 255, 255, 0.08)',
                        circular: false,
                        lineWidth: 1
                    },
                    pointLabels: {
                        color: '#e4e6ea',
                        font: {
                            family: "'Inter', sans-serif",
                            size: 11,
                            weight: '500'
                        },
                        padding: 8
                    }
                }
            }
        }
    });
}

/**
 * Оновлення візуального градієнта треку повзунка
 * (активна частина — шляхетний вишневий, решта — графіт)
 * та синхронізація інтерактивних насічок 1-10
 */
function updateSliderTrack(slider, valEl) {
    const val = parseFloat(slider.value);
    const percent = ((val - 1) / (10 - 1)) * 100;
    
    // Плавний насичений вишневий градієнт
    slider.style.background = `linear-gradient(to right, #9f1239 0%, #be123c ${Math.max(0, percent - 5)}%, #e11d48 ${percent}%, #1a1e28 ${percent}%, #1a1e28 100%)`;
    
    // Анімація мікро-імпульсу на числовому бейджі
    if (valEl) {
        valEl.textContent = val.toFixed(1) + ' / 10';
        valEl.classList.remove('val-pulse');
        void valEl.offsetWidth; // перезапуск css-анімації
        valEl.classList.add('val-pulse');
    }

    // Підсвічування відповідних насічок шкали
    const ticksRow = document.querySelector(`.slider-ticks-row[data-slider="${slider.id}"]`);
    if (ticksRow) {
        ticksRow.querySelectorAll('.slider-tick').forEach(tick => {
            const tickVal = parseFloat(tick.dataset.val);
            if (tickVal <= val) {
                tick.classList.add('active');
            } else {
                tick.classList.remove('active');
            }
        });
    }
}

/**
 * Початкове фарбування всіх слайдерів
 */
function initSliderTracks() {
    SLIDERS.forEach(s => {
        const slider = document.getElementById(s.id);
        const valEl = document.getElementById(s.valId);
        if (slider) {
            updateSliderTrack(slider, valEl);
        }
    });
}

/**
 * Прослуховування подій переміщення 5 слайдерів та кліків по шкалі
 */
function setupSliderListeners() {
    SLIDERS.forEach(slider => {
        const inputEl = document.getElementById(slider.id);
        const valEl = document.getElementById(slider.valId);

        if (!inputEl) return;

        inputEl.addEventListener('input', (e) => {
            updateSliderTrack(e.target, valEl);
            updateUserRadarDataset();
            debounceMatchCalculation();
        });
    });

    // Можливість кліку по будь-якій насічці (1..10) для точного миттєвого стрибка
    document.querySelectorAll('.slider-ticks-row .slider-tick').forEach(tick => {
        tick.addEventListener('click', () => {
            const row = tick.closest('.slider-ticks-row');
            if (!row) return;
            const sliderId = row.dataset.slider;
            const targetVal = parseFloat(tick.dataset.val);
            const slider = document.getElementById(sliderId);
            const valEl = document.getElementById(sliderId.replace('slider_', 'val_'));
            if (slider) {
                slider.value = targetVal;
                updateSliderTrack(slider, valEl);
                updateUserRadarDataset();
                debounceMatchCalculation();
            }
        });
    });
}

/**
 * Оновлення векторних даних у Chart.js
 */
function updateUserRadarDataset() {
    if (!priorityRadar) return;

    const currentValues = SLIDERS.map(s => {
        const el = document.getElementById(s.id);
        return el ? parseFloat(el.value) : 5.0;
    });

    priorityRadar.data.datasets[0].data = currentValues;
    priorityRadar.update('none'); // миттєвий рендеринг без затримок
}

/**
 * Дебаунс для оптимізації запитів до API (180ms)
 */
function debounceMatchCalculation() {
    const indicator = document.getElementById('statusIndicator');
    if (indicator) {
        indicator.innerHTML = `
            <span class="w-1.5 h-1.5 rounded-full bg-cherry-400"></span>
            <span class="text-graphite-400">Розрахунок...</span>
        `;
    }

    clearTimeout(matchDebounceTimer);
    matchDebounceTimer = setTimeout(() => {
        triggerMatchCalculation();
    }, 180);
}

/**
 * Збір значень слайдерів (діапазон 1-10)
 */
function getCurrentSliderVector() {
    const vector = {};
    SLIDERS.forEach(s => {
        const el = document.getElementById(s.id);
        vector[s.key] = el ? parseFloat(el.value) : 5.0;
    });
    return vector;
}

/**
 * Отримання поточного активного регіону
 */
function getSelectedRegion() {
    const regionSelect = document.getElementById('globalRegionSelect');
    return regionSelect ? regionSelect.value : 'global';
}

/**
 * Асинхронний виклик бекенду /api/match
 */
async function triggerMatchCalculation() {
    const sliders = getCurrentSliderVector();
    const region = getSelectedRegion();

    try {
        const response = await fetch('/api/match', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                sliders: sliders,
                region: region
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }

        const data = await response.json();
        renderMatches(data);
        updateTopTrackRadar(data.top_matches[0]);
        updateTrendsSection(data.trends, data.region);

        const indicator = document.getElementById('statusIndicator');
        if (indicator) {
            indicator.innerHTML = `
                <span class="w-1.5 h-1.5 rounded-full bg-cherry-500"></span>
                <span class="text-graphite-300">Синхронізовано</span>
            `;
        }
    } catch (err) {
        console.error('Помилка розрахунку матчингу:', err);
        const indicator = document.getElementById('statusIndicator');
        if (indicator) {
            indicator.innerHTML = `<span class="text-rose-400">Помилка мережі</span>`;
        }
    }
}

/**
 * Оновлення аури еталонного треку (Dataset 1) у радарній діаграмі
 */
function updateTopTrackRadar(topTrack) {
    if (!priorityRadar || !topTrack) return;

    const profile = topTrack.radar_profile;
    const radarData = [
        profile.learning_curve,
        profile.financial_vector,
        profile.architecture_visual,
        profile.company_scale,
        profile.stress_wlb
    ];

    priorityRadar.data.datasets[1].data = radarData;
    priorityRadar.data.datasets[1].label = `Еталон: ${topTrack.title}`;
    priorityRadar.update();

    const topBadge = document.getElementById('liveTopMatchName');
    if (topBadge) {
        topBadge.textContent = `${topTrack.title} (${topTrack.match_percentage}%)`;
    }
}

/**
 * Рендеринг карток Топ-3 у шляхетному графітово-вишневому стилі
 */
function renderMatches(data) {
    const container = document.getElementById('topMatchesContainer');
    if (!container) return;

    const matches = data.top_matches;
    const sliders = getCurrentSliderVector();
    const region = data.region;

    const queryParams = new URLSearchParams({
        region: region,
        learn: sliders.learning_curve,
        fin: sliders.financial_vector,
        arch: sliders.architecture_visual,
        scale: sliders.company_scale,
        stress: sliders.stress_wlb
    }).toString();

    let html = '';

    matches.forEach((item, index) => {
        // Конфігурація карток з вишневим акцентом на #1
        const rankConfigs = [
            {
                border: 'border-cherry-600/70 bg-graphite-850 shadow-cherry-subtle',
                badgeClass: 'bg-cherry-950/90 text-cherry-300 border border-cherry-800/70',
                badgeText: '#1 Рекомендовано',
                matchColor: 'text-cherry-400',
                btnClass: 'bg-cherry-700 hover:bg-cherry-600 text-white shadow-sm'
            },
            {
                border: 'border-graphite-700/70 bg-graphite-850/80 hover:border-graphite-600',
                badgeClass: 'bg-graphite-800 text-graphite-300 border border-graphite-600/70',
                badgeText: '#2 Альтернатива',
                matchColor: 'text-graphite-200',
                btnClass: 'bg-graphite-800 hover:bg-graphite-700 text-graphite-200 border border-graphite-600/70 hover:border-cherry-600/50'
            },
            {
                border: 'border-graphite-700/70 bg-graphite-850/80 hover:border-graphite-600',
                badgeClass: 'bg-graphite-800 text-graphite-300 border border-graphite-600/70',
                badgeText: '#3 Перспектива',
                matchColor: 'text-graphite-200',
                btnClass: 'bg-graphite-800 hover:bg-graphite-700 text-graphite-200 border border-graphite-600/70 hover:border-cherry-600/50'
            }
        ];

        const cfg = rankConfigs[index] || rankConfigs[1];
        const salary = item.regional_salary || {};
        const cardClass = index === 0 ? 'card-top-match' : 'card-noble';

        html += `
            <div class="relative rounded-2xl p-6 ${cardClass} flex flex-col justify-between transition-all duration-200">
                
                <div>
                    <!-- Заголовок та бейдж матчу -->
                    <div class="flex items-start justify-between gap-3 mb-3">
                        <span class="text-[11px] font-mono font-medium px-2 py-0.5 rounded-md ${cfg.badgeClass}">
                            ${cfg.badgeText}
                        </span>
                        
                        <div class="text-right">
                            <span class="text-2xl font-bold font-mono ${cfg.matchColor}">
                                ${item.match_percentage}%
                            </span>
                            <span class="block text-[10px] text-graphite-400 font-mono">сумісність</span>
                        </div>
                    </div>

                    <h3 class="text-lg font-bold text-white mb-0.5">
                        ${item.title}
                    </h3>
                    <p class="text-xs text-graphite-400 font-mono mb-3">
                        Категорія: <span class="text-graphite-300">${item.category}</span>
                    </p>

                    <!-- Аргументи алгоритму -->
                    <div class="bg-graphite-900/60 rounded-lg p-3 border border-graphite-700/60 text-xs text-graphite-300 mb-3 space-y-1">
                        <strong class="text-cherry-300 block font-mono text-[11px] uppercase">Чому цей трек:</strong>
                        ${item.match_reasons.map(r => `<p class="leading-relaxed text-graphite-300">• ${r}</p>`).join('')}
                    </div>

                    <!-- Зарплатна сітка -->
                    <div class="bg-graphite-900/60 rounded-lg p-3 border border-graphite-700/60 mb-4">
                        <span class="text-[10px] font-mono uppercase text-graphite-400 block mb-1">
                            Зарплата (${region.toUpperCase()}):
                        </span>
                        <div class="flex justify-between items-center text-xs font-mono">
                            <span class="text-graphite-400">Junior: <strong class="text-graphite-200">${salary.junior || 'N/A'}</strong></span>
                            <span class="text-graphite-400">Senior: <strong class="text-cherry-400 font-semibold">${salary.senior || 'N/A'}</strong></span>
                        </div>
                    </div>

                    <!-- Стек технологій -->
                    <div class="flex flex-wrap gap-1 mb-5">
                        ${item.tech_stack.slice(0, 5).map(tech => `
                            <span class="px-2 py-0.5 rounded bg-graphite-900 text-graphite-300 text-[11px] font-mono border border-graphite-700/70">
                                ${tech}
                            </span>
                        `).join('')}
                        ${item.tech_stack.length > 5 ? `<span class="px-1.5 py-0.5 text-[10px] font-mono text-graphite-400">+${item.tech_stack.length - 5}</span>` : ''}
                    </div>
                </div>

                <!-- Кнопка перегляду дорожньої карти -->
                <a href="/career/${item.slug}?${queryParams}" 
                   class="w-full text-center py-2.5 px-4 rounded-lg text-xs font-mono font-medium ${cfg.btnClass} transition-colors flex items-center justify-center space-x-2">
                    <span>Дорожня карта & Деталі</span>
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/>
                    </svg>
                </a>

            </div>
        `;
    });

    container.innerHTML = html;

    // Оновлюємо також повний каталог нижче
    renderFullCatalog(data.all_matches, queryParams);
}

/**
 * Рендеринг повного каталогу (10 треків)
 */
function renderFullCatalog(allTracks, queryParams) {
    const grid = document.getElementById('allTracksGrid');
    if (!grid) return;

    let html = '';
    allTracks.forEach(track => {
        html += `
            <div class="bg-graphite-850/85 rounded-xl p-4 border border-graphite-700/70 hover:border-graphite-600 flex flex-col justify-between">
                <div>
                    <div class="flex justify-between items-start mb-2">
                        <span class="text-[10px] font-mono px-1.5 py-0.5 rounded bg-graphite-800 text-graphite-300">${track.category}</span>
                        <span class="text-xs font-mono font-semibold text-cherry-400">${track.match_percentage}%</span>
                    </div>
                    <h4 class="text-sm font-bold text-white mb-1">${track.title}</h4>
                    <p class="text-xs text-graphite-400 leading-relaxed mb-3">${track.short_desc}</p>
                </div>
                <a href="/career/${track.slug}?${queryParams}" class="text-xs font-mono text-cherry-400 hover:text-cherry-300 font-medium inline-flex items-center space-x-1">
                    <span>Детальніше →</span>
                </a>
            </div>
        `;
    });
    grid.innerHTML = html;
}

/**
 * Оновлення блоку ринкових трендів
 */
function updateTrendsSection(trends, region) {
    if (!trends) return;

    const regNameEl = document.getElementById('trendRegionName');
    const vacEl = document.getElementById('trendVacancies');
    const demandEl = document.getElementById('trendDemandIndex');
    const demandBar = document.getElementById('trendDemandBar');
    const remoteEl = document.getElementById('trendRemoteShare');
    const skillEl = document.getElementById('trendHotSkill');
    const sentEl = document.getElementById('trendSentiment');
    const radarRegBadge = document.getElementById('radarRegionBadge');
    const labelCurrentRegion = document.getElementById('labelCurrentRegion');

    if (regNameEl) regNameEl.textContent = region.toUpperCase();
    if (vacEl) vacEl.textContent = trends.active_vacancies;
    if (demandEl) demandEl.textContent = `${trends.demand_index} / 100`;
    if (demandBar) demandBar.style.width = `${trends.demand_index}%`;
    if (remoteEl) remoteEl.textContent = trends.remote_share;
    if (skillEl) skillEl.textContent = trends.hot_skill;
    if (sentEl) sentEl.textContent = trends.market_sentiment;
    if (radarRegBadge) radarRegBadge.textContent = region.toUpperCase();
    if (labelCurrentRegion) labelCurrentRegion.textContent = region.toUpperCase();
}

/**
 * Налаштування кнопок швидких пресетів
 */
function setupPresetButtons() {
    const buttons = document.querySelectorAll('.preset-btn');
    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            const learn = parseFloat(btn.dataset.learn);
            const fin = parseFloat(btn.dataset.fin);
            const arch = parseFloat(btn.dataset.arch);
            const scale = parseFloat(btn.dataset.scale);
            const stress = parseFloat(btn.dataset.stress);

            setSliderValue('slider_learning_curve', 'val_learning_curve', learn);
            setSliderValue('slider_financial_vector', 'val_financial_vector', fin);
            setSliderValue('slider_architecture_visual', 'val_architecture_visual', arch);
            setSliderValue('slider_company_scale', 'val_company_scale', scale);
            setSliderValue('slider_stress_wlb', 'val_stress_wlb', stress);

            updateUserRadarDataset();
            triggerMatchCalculation();
        });
    });
}

function setSliderValue(sliderId, valId, value) {
    const slider = document.getElementById(sliderId);
    const valEl = document.getElementById(valId);
    if (slider) {
        slider.value = value;
        updateSliderTrack(slider, valEl);
    }
}

/**
 * Кнопка скидання слайдерів
 */
function setupResetButton() {
    const resetBtn = document.getElementById('resetSlidersBtn');
    if (!resetBtn) return;

    resetBtn.addEventListener('click', () => {
        setSliderValue('slider_learning_curve', 'val_learning_curve', 5.0);
        setSliderValue('slider_financial_vector', 'val_financial_vector', 7.0);
        setSliderValue('slider_architecture_visual', 'val_architecture_visual', 5.0);
        setSliderValue('slider_company_scale', 'val_company_scale', 6.0);
        setSliderValue('slider_stress_wlb', 'val_stress_wlb', 5.0);

        updateUserRadarDataset();
        triggerMatchCalculation();
    });
}

/**
 * Перемикач розгортання повного каталогу
 */
function setupCatalogToggle() {
    const btn = document.getElementById('toggleAllTracksBtn');
    const grid = document.getElementById('allTracksGrid');
    const arrow = document.getElementById('allTracksArrow');

    if (!btn || !grid) return;

    btn.addEventListener('click', () => {
        const isHidden = grid.classList.contains('hidden');
        if (isHidden) {
            grid.classList.remove('hidden');
            btn.querySelector('span').textContent = 'Згорнути каталог';
            if (arrow) arrow.classList.add('rotate-180');
        } else {
            grid.classList.add('hidden');
            btn.querySelector('span').textContent = 'Розгорнути повний каталог (10 напрямів)';
            if (arrow) arrow.classList.remove('rotate-180');
        }
    });
}

// ==============================================================================
// 2. Глобальний селектор регіону
// ==============================================================================

function initGlobalRegionSync() {
    const select = document.getElementById('globalRegionSelect');
    if (!select) return;

    select.addEventListener('change', (e) => {
        const newRegion = e.target.value;
        const footerBadge = document.getElementById('footerActiveRegion');
        if (footerBadge) footerBadge.textContent = newRegion.toUpperCase();

        if (document.getElementById('priorityRadarChart')) {
            triggerMatchCalculation();
        } else {
            const currentUrl = new URL(window.location.href);
            currentUrl.searchParams.set('region', newRegion);
            window.location.href = currentUrl.toString();
        }
    });
}

// ==============================================================================
// 3. Логіка Детальної Сторінки (/career/<slug>): Порівняльний Радар 1-10 & Зарплати
// ==============================================================================

function initDetailPage() {
    setupDetailRadarChart();
    setupSalaryTabs();
}

/**
 * Побудова порівняльного радара з чіткою шкалою 0-10 та кроками розмітки
 */
function setupDetailRadarChart() {
    const canvas = document.getElementById('detailRadarChart');
    if (!canvas || !window.DETAIL_TRACK_DATA) return;

    const data = window.DETAIL_TRACK_DATA;
    const ctx = canvas.getContext('2d');

    const datasets = [
        {
            label: `Еталон: ${data.title}`,
            data: [
                data.radar.learning_curve,
                data.radar.financial_vector,
                data.radar.architecture_visual,
                data.radar.company_scale,
                data.radar.stress_wlb
            ],
            backgroundColor: 'rgba(190, 18, 60, 0.28)', // Шляхетний вишневий
            borderColor: '#be123c',
            pointBackgroundColor: '#fb7185',
            pointBorderColor: '#0b0d12',
            pointRadius: 4.5,
            borderWidth: 2.2
        }
    ];

    // Якщо користувач перейшов з калькулятора, додаємо його вектор для порівняння
    if (data.user_vector && data.user_vector.learning_curve !== null) {
        datasets.push({
            label: 'Ваш особистий вектор',
            data: [
                data.user_vector.learning_curve,
                data.user_vector.financial_vector,
                data.user_vector.architecture_visual,
                data.user_vector.company_scale,
                data.user_vector.stress_wlb
            ],
            backgroundColor: 'rgba(16, 185, 129, 0.16)', // Смарагдовий контраст
            borderColor: '#10b981',
            borderDash: [4, 4],
            pointBackgroundColor: '#34d399',
            pointBorderColor: '#0b0d12',
            pointRadius: 4,
            borderWidth: 2
        });
    }

    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: [
                'CS & Теорія',
                'Фінансова стеля',
                'Візуал / UI-UX',
                'Стартапи & Свобода',
                'Драйв & Стрес'
            ],
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#9fa5b4',
                        font: { family: "'Inter', sans-serif", size: 11 },
                        padding: 12
                    }
                }
            },
            scales: {
                r: {
                    min: 0,
                    max: 10,
                    beginAtZero: true,
                    ticks: {
                        stepSize: 2,         // Шкала: 0, 2, 4, 6, 8, 10
                        display: true,       // Чітка видимість градації
                        color: '#757c8e',
                        backdropColor: 'transparent',
                        font: {
                            family: "'JetBrains Mono', monospace",
                            size: 10,
                            weight: '500'
                        },
                        z: 2
                    },
                    angleLines: {
                        display: true,
                        color: 'rgba(255, 255, 255, 0.08)',
                        lineWidth: 1
                    },
                    grid: {
                        display: true,
                        color: 'rgba(255, 255, 255, 0.08)',
                        circular: false,
                        lineWidth: 1
                    },
                    pointLabels: {
                        color: '#e4e6ea',
                        font: { family: "'Inter', sans-serif", size: 11, weight: '500' },
                        padding: 8
                    }
                }
            }
        }
    });
}

/**
 * Перемикання вкладок зарплат по регіонах
 */
function setupSalaryTabs() {
    const tabButtons = document.querySelectorAll('.salary-tab-btn');
    const salaryBlocks = document.querySelectorAll('.salary-region-block');

    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetRegion = btn.dataset.regionTarget;

            tabButtons.forEach(b => {
                b.classList.remove('bg-cherry-700', 'text-white', 'font-medium', 'shadow-sm');
                b.classList.add('text-graphite-400');
            });
            btn.classList.add('bg-cherry-700', 'text-white', 'font-medium', 'shadow-sm');
            btn.classList.remove('text-graphite-400');

            salaryBlocks.forEach(block => {
                if (block.id === `salaryCard_${targetRegion}`) {
                    block.classList.remove('hidden');
                } else {
                    block.classList.add('hidden');
                }
            });
        });
    });
}
