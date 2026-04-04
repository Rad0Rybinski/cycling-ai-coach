const SUPABASE_URL = 'https://geadqvspdsassmvlpixr.supabase.co'; 
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdlYWRxdnNwZHNhc3NtdmxwaXhyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzUyOTcwNzMsImV4cCI6MjA5MDg3MzA3M30.5pkKOWoN7LFyqilBj_zzBxIbg_u7CkhskH1LCijvKeU';

const supabaseClient = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

const loginBtn = document.getElementById('login-btn');
const logoutBtn = document.getElementById('logout-btn');
const userProfile = document.getElementById('user-profile');
const userNameDisplay = document.getElementById('user-name');

function updateAuthUI(user) {
    if (user) {
        loginBtn.classList.add('hidden');
        userProfile.classList.remove('hidden');
        userProfile.classList.add('flex');
        
        const fullName = user.user_metadata?.full_name || 'Kolarzu';
        userNameDisplay.innerText = fullName.split(' ')[0];
    } else {
        loginBtn.classList.remove('hidden');
        userProfile.classList.add('hidden');
        userProfile.classList.remove('flex');
    }
}

async function checkSession() {
    const { data: { session } } = await supabaseClient.auth.getSession();
    updateAuthUI(session?.user);

    supabaseClient.auth.onAuthStateChange((_event, session) => {
        updateAuthUI(session?.user);
    });
}

loginBtn.addEventListener('click', async () => {
    const { error } = await supabaseClient.auth.signInWithOAuth({
        provider: 'google',
        options: {
            redirectTo: window.location.origin + window.location.pathname,
            queryParams: { prompt: 'select_account' }
        }
    });
    if (error) console.error("Błąd logowania:", error.message);
});

logoutBtn.addEventListener('click', async () => {
    const { error } = await supabaseClient.auth.signOut();
    if (error) console.error("Błąd wylogowania:", error.message);
});

checkSession();


// ==========================================
// 1. LOGIKA EDUKATORA, WZORÓW I DRABINY
// ==========================================

function autoDetectTerrain() {
    const dist = parseFloat(document.getElementById('q-dist').value) || 1;
    const elev = parseFloat(document.getElementById('q-elev').value) || 0;
    
    const ratio = elev / dist;
    const terrainSelect = document.getElementById('q-terrain');
    const oldTerrain = terrainSelect.value;
    let newTerrain = 'Płasko';

    if (ratio >= 15) {
        newTerrain = 'Góry';
    } else if (ratio >= 8) {
        newTerrain = 'Pagórki';
    }

    if (oldTerrain !== newTerrain) {
        terrainSelect.value = newTerrain;
        terrainSelect.classList.add('bg-blue-100', 'border-blue-500');
        setTimeout(() => {
            terrainSelect.classList.remove('bg-blue-100', 'border-blue-500');
        }, 500);
    }
}

function updateEducatorAndLadderLive() {
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

    const weight = parseFloat(document.getElementById('edu-weight').value);
    const power = parseFloat(document.getElementById('edu-power').value);
    
    document.getElementById('edu-weight-val').innerText = weight;
    document.getElementById('edu-power-val').innerText = power;

    const wkg = power / weight;
    const wkgFormatted = wkg.toFixed(2);
    document.getElementById('edu-wkg-formula').innerText = `W/kg = ${power}W / ${weight}kg = ${wkgFormatted} W/kg`;
    
    document.getElementById('user-wkg-final').innerText = wkgFormatted;

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

['edu-elev', 'edu-time', 'edu-weight'].forEach(id => {
    document.getElementById(id).addEventListener('input', (e) => {
        const rightSideId = id.replace('edu-', 'q-');
        document.getElementById(rightSideId).value = e.target.value;
        updateEducatorAndLadderLive();
        if (id === 'edu-elev') autoDetectTerrain();
    });
});
document.getElementById('edu-power').addEventListener('input', updateEducatorAndLadderLive);

['q-elev', 'q-time', 'q-weight', 'q-dist'].forEach(id => {
    const el = document.getElementById(id);
    if(el) {
        el.addEventListener('input', (e) => {
            if (id !== 'q-dist') {
                const leftSideId = id.replace('q-', 'edu-');
                const slider = document.getElementById(leftSideId);
                if (slider) slider.value = e.target.value;
            }
            updateEducatorAndLadderLive();
            if (id === 'q-elev' || id === 'q-dist') autoDetectTerrain();
        });
    }
});

const rpeSlider = document.getElementById('q-rpe');
if (rpeSlider) {
    rpeSlider.addEventListener('input', (e) => {
        document.getElementById('q-rpe-val').innerText = e.target.value + ' / 10';
    });
}

updateEducatorAndLadderLive();
autoDetectTerrain();


// ==========================================
// 2. KOMUNIKACJA Z API I ZAPIS DO BAZY
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
        const response = await fetch('https://cycling-ai-coach.onrender.com/api/analyze', { 
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

            // Zapis do Supabase
            const { data: { session } } = await supabaseClient.auth.getSession();
            if (session) {
                const calculatedVAM = Math.round(payload.elevation_gain / (payload.duration_min / 60));
                const { error: dbError } = await supabaseClient
                    .from('workouts')
                    .insert([{
                        duration_min: payload.duration_min,
                        distance_km: payload.distance_km,
                        ftp: calculatedFTP,
                        vam: calculatedVAM,
                        ai_advice: data.ai_coach_advice
                    }]);
                if (dbError) console.error("Błąd zapisu do bazy:", dbError.message);
                else console.log("Trening zapisany pomyślnie w bazie!");
            }
        } else {
            loadingDiv.classList.add('hidden');
            responseDiv.innerHTML = `<h3 class="text-red-400 font-bold text-xl mb-2">Błąd z danych wejściowych:</h3>
                                     <ul class="list-disc pl-5 text-red-300">
                                        ${data.detail.map(err => `<li>${err}</li>`).join('')}
                                     </ul>`;
        }
    } catch (error) {
        loadingDiv.classList.add('hidden');
        responseDiv.innerHTML = `<p class="text-red-500 font-bold">Błąd połączenia z serwerem API!</p>`;
        console.error("Błąd API:", error);
    } finally {
        submitBtn.disabled = false;
        submitBtn.classList.remove('opacity-50', 'cursor-not-allowed');
    }
});


// ==========================================
// 3. OBSŁUGA MODALA I WYŚWIETLANIE HISTORII
// ==========================================

const historyBtn = document.getElementById('history-btn');
const closeHistoryBtn = document.getElementById('close-history-btn');
const historyModal = document.getElementById('history-modal');
const historyContent = document.getElementById('history-content');

// Otwieranie Modala
historyBtn.addEventListener('click', async () => {
    historyModal.classList.remove('hidden');
    
    // Pobieranie danych (Posortowane od najnowszego)
    const { data: workouts, error } = await supabaseClient
        .from('workouts')
        .select('*')
        .order('created_at', { ascending: false });

    if (error) {
        historyContent.innerHTML = `<div class="text-red-500 text-center py-10 font-bold">Błąd pobierania danych: ${error.message}</div>`;
        return;
    }

    if (!workouts || workouts.length === 0) {
        historyContent.innerHTML = `
            <div class="text-center text-slate-500 py-12 flex flex-col items-center">
                <span class="text-4xl mb-3">📭</span>
                <p class="font-bold">Brak treningów w kartotece.</p>
                <p class="text-sm">Dodaj swój pierwszy trening, by AI Coach zaczął budować Twoją historię!</p>
            </div>`;
        return;
    }

    // Generowanie Kafelków (Kart) dla każdego treningu
    historyContent.innerHTML = workouts.map(workout => {
        // Formatowanie daty na przyjazną (np. 12.10.2023, 15:30)
        const dateObj = new Date(workout.created_at);
        const formattedDate = dateObj.toLocaleDateString('pl-PL', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' });

        return `
            <div class="bg-white p-5 rounded-xl shadow-sm border border-slate-200 hover:shadow-md transition-shadow">
                <div class="flex flex-col md:flex-row md:justify-between border-b border-slate-100 pb-3 mb-4 gap-2">
                    <span class="font-extrabold text-slate-700 bg-slate-100 px-3 py-1 rounded w-fit">🗓️ ${formattedDate}</span>
                    <span class="text-blue-700 font-black flex items-center gap-2">
                        <span class="bg-blue-50 px-2 py-1 rounded border border-blue-100">⚡ FTP: ${workout.ftp} W</span>
                        <span class="bg-emerald-50 px-2 py-1 rounded border border-emerald-100 text-emerald-700">⛰️ VAM: ${workout.vam}</span>
                    </span>
                </div>
                
                <div class="text-sm text-slate-600 flex gap-4 mb-4 font-bold uppercase tracking-wide">
                    <span class="flex items-center gap-1"><span class="text-lg">⏱️</span> ${workout.duration_min} min</span>
                    <span class="flex items-center gap-1"><span class="text-lg">📏</span> ${workout.distance_km} km</span>
                </div>
                
                <div class="text-sm bg-slate-50 p-4 rounded-lg border border-slate-100 prose prose-sm max-w-none prose-headings:text-orange-500 prose-p:leading-relaxed">
                    ${marked.parse(workout.ai_advice)}
                </div>
            </div>
        `;
    }).join('');
});

// Zamykanie Modala
closeHistoryBtn.addEventListener('click', () => {
    historyModal.classList.add('hidden');
    // Czyścimy zawartość przy zamykaniu, żeby przy kolejnym otwarciu załadować świeżą listę
    historyContent.innerHTML = '<div class="text-center text-slate-500 py-10 font-medium">Ładowanie historii...</div>';
});

// Zamykanie kliknięciem w ciemne tło (poza białym oknem)
historyModal.addEventListener('click', (e) => {
    if (e.target === historyModal) {
        closeHistoryBtn.click();
    }
});