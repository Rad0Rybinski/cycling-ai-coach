// ==========================================
// 1. LOGIKA EDUKATORA, WZORÓW I DRABINY
// ==========================================

// --- NOWOŚĆ: Funkcja do automatycznego wykrywania terenu ---
function autoDetectTerrain() {
    const dist = parseFloat(document.getElementById('q-dist').value) || 1; // Zabezpieczenie przed dzieleniem przez zero
    const elev = parseFloat(document.getElementById('q-elev').value) || 0;
    
    // Obliczamy ile metrów w górę przypada na każdy kilometr
    const ratio = elev / dist;
    
    const terrainSelect = document.getElementById('q-terrain');
    const oldTerrain = terrainSelect.value;
    let newTerrain = 'Płasko';

    if (ratio >= 15) {
        newTerrain = 'Góry';
    } else if (ratio >= 8) {
        newTerrain = 'Pagórki';
    }

    // Aplikujemy nowy teren i delikatnie migamy kolorem, by użytkownik to zauważył
    if (oldTerrain !== newTerrain) {
        terrainSelect.value = newTerrain;
        terrainSelect.classList.add('bg-blue-100', 'border-blue-500');
        setTimeout(() => {
            terrainSelect.classList.remove('bg-blue-100', 'border-blue-500');
        }, 500);
    }
}

function updateEducatorAndLadderLive() {
    // --- 1. OBSŁUGA VAM ---
    const elev = parseFloat(document.getElementById('edu-elev').value);
    const timeMin = parseFloat(document.getElementById('edu-time').value);
    
    if (timeMin > 0) {
        const timeHours = (timeMin / 60).toFixed(2);
        document.getElementById('edu-elev-val').innerText = elev;
        document.getElementById('edu-time-val').innerText = timeMin;
        
        const vam = (elev / (timeMin / 60)).toFixed(0);
        document.getElementById('edu-vam-formula').innerText = `VAM = ${elev}m / ${timeHours}h = ${vam} m/h`;
        
        let vamRank = '';
        if (vam < 500) vamRank = '🐌 Poziom: Turystyka górska';
        else if (vam < 800) vamRank = '🚴 Poziom: Solidny Amator';
        else if (vam < 1100) vamRank = '🐐 Poziom: Górska Kozica';
        else if (vam < 1500) vamRank = '👽 Poziom: Elita / Pro';
        else vamRank = '🚀 Poziom: Kosmita (Tadej Pogačar)';
        
        document.getElementById('edu-vam-rank').innerText = vamRank;
    }

    // --- 2. OBSŁUGA W/kg I WZORU ---
    const weight = parseFloat(document.getElementById('edu-weight').value);
    const power = parseFloat(document.getElementById('edu-power').value);
    
    document.getElementById('edu-weight-val').innerText = weight;
    document.getElementById('edu-power-val').innerText = power;

    const wkg = power / weight;
    const wkgFormatted = wkg.toFixed(2);
    document.getElementById('edu-wkg-formula').innerText = `W/kg = ${power}W / ${weight}kg = ${wkgFormatted} W/kg`;
    
    document.getElementById('user-wkg-final').innerText = wkgFormatted;

    // --- 3. OBSŁUGA DRABINY ---
    const minWkgScale = 1.0;
    const maxWkgScale = 6.5; 
    let clampedWkg = Math.max(minWkgScale, Math.min(maxWkgScale, wkg));
    let percentage = ((clampedWkg - minWkgScale) / (maxWkgScale - minWkgScale)) * 100;

    document.getElementById('user-marker').style.bottom = `${percentage}%`;

    const categories = ['cat-d', 'cat-c', 'cat-b', 'cat-a', 'cat-pro'];
    categories.forEach(id => {
        const el = document.getElementById(id);
        el.classList.remove('bg-emerald-950', 'text-emerald-100', 'border', 'border-emerald-500', 'shadow-[0_0_15px_rgba(16,185,129,0.5)]', 'scale-105', 'z-10');
        el.classList.add('bg-slate-900/50', 'text-slate-300');
        if (id === 'cat-pro') el.classList.add('text-red-300');
    });

    let currentCatId = '';
    if (wkg < 2.5) currentCatId = 'cat-d';
    else if (wkg < 3.2) currentCatId = 'cat-c';
    else if (wkg < 4.0) currentCatId = 'cat-b';
    else if (wkg < 5.5) currentCatId = 'cat-a';
    else currentCatId = 'cat-pro';

    const activeEl = document.getElementById(currentCatId);
    activeEl.classList.remove('bg-slate-900/50', 'text-slate-300', 'text-red-300');
    activeEl.classList.add('scale-105', 'z-10'); 
    
    if (currentCatId === 'cat-pro') {
        activeEl.classList.add('bg-red-950', 'text-red-100', 'border', 'border-red-500', 'shadow-[0_0_15px_rgba(239,68,68,0.7)]');
    } else {
        activeEl.classList.add('bg-emerald-950', 'text-emerald-100', 'border', 'border-emerald-500', 'shadow-[0_0_15px_rgba(16,185,129,0.7)]');
    }
}

// Synchronizacja Suwaków (Lewa strona) -> Pola tekstowe (Prawa strona)
['edu-elev', 'edu-time', 'edu-weight'].forEach(id => {
    document.getElementById(id).addEventListener('input', (e) => {
        const rightSideId = id.replace('edu-', 'q-');
        document.getElementById(rightSideId).value = e.target.value;
        updateEducatorAndLadderLive();
        
        // Jeśli przesuwamy suwak przewyższenia, sprawdzamy teren!
        if (id === 'edu-elev') {
            autoDetectTerrain();
        }
    });
});
document.getElementById('edu-power').addEventListener('input', updateEducatorAndLadderLive);

// Synchronizacja Pól tekstowych (Prawa strona) -> Suwaki (Lewa strona)
['q-elev', 'q-time', 'q-weight', 'q-dist'].forEach(id => {
    const el = document.getElementById(id);
    if(el) {
        el.addEventListener('input', (e) => {
            // Dystans nie ma swojego suwaka po lewej, więc go pomijamy w synchronizacji
            if (id !== 'q-dist') {
                const leftSideId = id.replace('q-', 'edu-');
                const slider = document.getElementById(leftSideId);
                if (slider) slider.value = e.target.value;
            }
            updateEducatorAndLadderLive();
            
            // Jeśli wpisujemy nowe przewyższenie lub dystans, sprawdzamy teren!
            if (id === 'q-elev' || id === 'q-dist') {
                autoDetectTerrain();
            }
        });
    }
});

// Suwak RPE
const rpeSlider = document.getElementById('q-rpe');
if (rpeSlider) {
    rpeSlider.addEventListener('input', (e) => {
        document.getElementById('q-rpe-val').innerText = e.target.value + ' / 10';
    });
}

// Inicjalizacja na start
updateEducatorAndLadderLive();
autoDetectTerrain(); // Od razu ustawiamy odpowiedni teren na bazie domyślnych 40km i 500m!


// ==========================================
// 2. KOMUNIKACJA Z API I WYSYŁKA FORMULARZA
// ==========================================

const savedApiKey = localStorage.getItem('cycling_api_key');
if(savedApiKey) {
    document.getElementById('q-api-key').value = savedApiKey;
}

document.getElementById('quiz-form').addEventListener('submit', async (e) => {
    e.preventDefault(); 

    const payload = {
        weight_total: parseFloat(document.getElementById('q-weight').value),
        distance_km: parseFloat(document.getElementById('q-dist').value),
        duration_min: parseInt(document.getElementById('q-time').value),
        elevation_gain: parseInt(document.getElementById('q-elev').value),
        terrain_type: document.getElementById('q-terrain').value,
        position_type: document.getElementById('q-pos').value,
        bike_type: document.getElementById('q-bike').value,
        rpe_score: parseInt(document.getElementById('q-rpe').value),
        openai_api_key: document.getElementById('q-api-key').value
    };

    localStorage.setItem('cycling_api_key', payload.openai_api_key);

    const resultSection = document.getElementById('result-section');
    const loadingDiv = document.getElementById('loading');
    const responseDiv = document.getElementById('ai-response');
    const submitBtn = document.getElementById('submit-btn');

    resultSection.classList.remove('hidden');
    responseDiv.innerHTML = ''; 
    loadingDiv.classList.remove('hidden'); 
    submitBtn.disabled = true;
    submitBtn.classList.add('opacity-50', 'cursor-not-allowed');

    resultSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

    try {
        const response = await fetch('http://127.0.0.1:8000/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (response.ok) {
            loadingDiv.classList.add('hidden');
            
            responseDiv.innerHTML = marked.parse(data.ai_coach_advice);

            const calculatedFTP = Math.round(data.calculations.estimated_ftp);
            const userWeight = payload.weight_total; 
            
            document.getElementById('edu-weight').value = userWeight;
            document.getElementById('edu-power').value = calculatedFTP;
            document.getElementById('q-weight').value = userWeight;
            
            updateEducatorAndLadderLive();

        } else {
            loadingDiv.classList.add('hidden');
            responseDiv.innerHTML = `<h3 class="text-red-400 font-bold text-xl mb-2">Błąd z danych wejściowych:</h3>
                                     <ul class="list-disc pl-5 text-red-300">
                                        ${data.detail.map(err => `<li>${err}</li>`).join('')}
                                     </ul>`;
        }
    } catch (error) {
        loadingDiv.classList.add('hidden');
        responseDiv.innerHTML = `<p class="text-red-500 font-bold">Błąd połączenia z serwerem. Upewnij się, że Twój serwer Python (FastAPI) jest uruchomiony!</p>`;
        console.error("Błąd API:", error);
    } finally {
        submitBtn.disabled = false;
        submitBtn.classList.remove('opacity-50', 'cursor-not-allowed');
    }
});