# ==========================================
# BAZA WIEDZY I LOGIKA ANALIZY
# ==========================================

CYCLING_TIERS = {
    # --- AMATORZY ---
    "amator_d": {"name": "☕ Koneser Kawiarni", "min": 1.0, "max": 2.5, "desc": "Więcej przerw na kawę niż pedałowania w trupa. Serce rośnie, forma powoli też!"},
    "amator_c": {"name": "🚴 Weekendowy Wycinak", "min": 2.5, "max": 3.2, "desc": "Łydka zaczyna pracować. Średnia 30 km/h w peletonie to już nie problem."},
    "amator_b": {"name": "🐗 Lokalny Dzik Ustawkowy", "min": 3.2, "max": 4.0, "desc": "Dajesz mocne zmiany, a koledzy z ustawek zaczynają Cię nienawidzić na podjazdach."},
    "amator_a": {"name": "👽 Szosowy Rzeźnik (Top)", "min": 4.0, "max": 5.5, "desc": "Pół-zawodowiec. Golisz nogi i urywasz peleton na wyścigach o puchar wójta."},
    # --- ZAWODOWCY ---
    "pro_goral": {"name": "🇵🇱 Rafał Majka / 🇸🇮 Tadej Pogačar", "min": 6.0, "max": 7.0, "desc": "Górskie kozice. Przy 60-66 kg generują ponad 400W na godzinnych podjazdach w Alpach."},
    "pro_klasyk": {"name": "🇳🇱 Mathieu van der Poel", "min": 5.5, "max": 6.5, "desc": "Cięższy, wybuchowy walec (75kg). Na płaskim bruku i krótkich ściankach nikt nie ma z nim szans."}
}

# ---------------------------------------------------------
# FUNKCJA 1: Analiza Drabiny i dobór przeciwników
# ---------------------------------------------------------
def get_comparison_data(user_wkg: float, terrain_type: str) -> dict:
    """
    Znajduje kategorię użytkownika, liczy ile mu brakuje do następnej 
    i dobiera odpowiedniego PRO do porównania.
    """
    current_tier = None
    next_tier_wkg = None
    
    # Szukamy, w której kategorii jest użytkownik
    if user_wkg < 2.5:
        current_tier = CYCLING_TIERS["amator_d"]
        next_tier_wkg = 2.5
    elif user_wkg < 3.2:
        current_tier = CYCLING_TIERS["amator_c"]
        next_tier_wkg = 3.2
    elif user_wkg < 4.0:
        current_tier = CYCLING_TIERS["amator_b"]
        next_tier_wkg = 4.0
    else:
        current_tier = CYCLING_TIERS["amator_a"]
        next_tier_wkg = 5.5 # Sufit dla amatorów
        
    # Dobieramy zawodowca na podstawie terenu z formularza
    if "Gór" in terrain_type:
        pro_tier = CYCLING_TIERS["pro_goral"]
    else:
        pro_tier = CYCLING_TIERS["pro_klasyk"]
        
    gap_to_next = round(next_tier_wkg - user_wkg, 2) if next_tier_wkg else 0

    return {
        "user_category": current_tier["name"],
        "category_desc": current_tier["desc"],
        "gap_to_next_wkg": gap_to_next,
        "pro_benchmark": pro_tier["name"],
        "pro_desc": pro_tier["desc"]
    }

# ---------------------------------------------------------
# FUNKCJA 2: Estymacja Zmęczenia (TSS) i Regeneracji
# ---------------------------------------------------------
def analyze_fatigue_and_recovery(rpe: int, duration_min: int) -> dict:
    """
    Oblicza jak bardzo trening "wszedł w nogi" na podstawie 
    subiektywnego zmęczenia (RPE) i czasu jazdy.
    """
    # Prosty wzór na obciążenie organizmu: RPE * czas w godzinach
    duration_hours = duration_min / 60
    load_score = rpe * duration_hours
    
    recovery_advice = ""
    
    if load_score < 5:
        fatigue_level = "🟢 Bardzo niskie (Aktywna regeneracja)"
        recovery_advice = "Jutro możesz śmiało robić mocny trening interwałowy."
    elif load_score < 12:
        fatigue_level = "🟡 Średnie (Solidny trening)"
        recovery_advice = "Zadbaj o białko po jeździe. Jutro zalecana spokojna jazda (tzw. tlen)."
    else:
        fatigue_level = "🔴 Ekstremalne (Zajechanie)"
        recovery_advice = "Nogi będą jutro jak z betonu! Obowiązkowo dzień wolny od roweru, dobre nawodnienie i sen."

    return {
        "load_score": round(load_score, 1),
        "fatigue_level": fatigue_level,
        "recovery_advice": recovery_advice
    }