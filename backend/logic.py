
# ==========================================
# CYCLING PRO-AM ANALYZER - LOGIC MODULE
# Serce obliczeniowe aplikacji
# ==========================================

# --- SŁOWNIKI MNOŻNIKÓW (Nasze reguły gry) ---
# TUTAJ MOŻESZ ULEPSZYĆ LOGIKĘ FIZYKI W PRZYSZŁOŚCI

POSITION_MULTIPLIERS = {
    "Aero": 0.9,          # Dolny chwyt zmniejsza opór o 10%
    "Standard": 1.0,      # Baza (ręce na klamkach)
    "Wyprostowany": 1.2   # Sylwetka jak żagiel, opór rośnie o 20%
}

BIKE_ROLLING_RESISTANCE = {
    "Szosa": 1.0,         # Cienkie opony, wysokie ciśnienie
    "Gravel": 1.15,       # Szersza opona, niższe ciśnienie
    "MTB": 1.35           # Szeroka kostka (traktor)
}


# ==========================================
# 1. BRAMKARZ (SANITY CHECK)
# ==========================================
def validate_input(data: dict) -> list:
    """
    Sprawdza, czy dane wpisane przez użytkownika mają fizyczny sens.
    Zwraca listę błędów. Jeśli lista jest pusta, dane są poprawne.
    """
    errors = []
    
    # Przeliczamy czas na godziny do szybkich sprawdzeń
    hours = data['duration_min'] / 60
    
    # 1. Sprawdzenie czasu
    if data['duration_min'] < 5:
        errors.append("Zbyt krótka jazda. Podaj trening trwający minimum 5 minut.")
    elif data['duration_min'] <= 0:
        errors.append("Czas musi być większy niż zero!")
        return errors # Przerywamy, by nie dzielić przez zero w kolejnych krokach
        
    # 2. Sprawdzenie prędkości
    avg_speed_kmh = data['distance_km'] / hours
    if avg_speed_kmh > 65:
        errors.append(f"Prędkość {avg_speed_kmh:.1f} km/h? Chyba jechałeś w aucie lub zapomniałeś wyłączyć licznik!")
    elif avg_speed_kmh < 5:
        errors.append("Prędkość poniżej 5 km/h. To raczej spacer z rowerem.")

    # 3. Sprawdzenie wagi zestawu
    if data['weight_total'] < 40 or data['weight_total'] > 160:
        errors.append("Podaj realną łączną wagę (Twoja waga + około 10kg rower).")

    # 4. Sprawdzenie VAM (metry w pionie na godzinę)
    vam = data['elevation_gain'] / hours
    if vam > 2000:
        errors.append(f"Twój VAM to {vam:.0f} m/h. Najlepsi zawodowcy mają 1800 m/h. Sprawdź, czy nie dodałeś zera w przewyższeniach!")

    return errors


# ==========================================
# 2. SILNIKI OBLICZENIOWE (Modele fizyczne)
# ==========================================
def calculate_vam_model(weight: float, elevation: int, duration_min: int) -> float:
    """ Oblicza moc na podstawie pokonywania grawitacji (dla terenów górskich). """
    hours = duration_min / 60
    vam = elevation / hours
    
    # Wzór amatora: W/kg = VAM / 250
    w_per_kg = vam / 250
    power = w_per_kg * weight
    return power

def calculate_aero_model(weight: float, distance_km: float, duration_min: int, position: str, bike: str) -> float:
    """ Oblicza moc na podstawie pokonywania wiatru i tarcia opon (na płaskim). """
    # Stałe fizyczne (uproszczone)
    rho = 1.225         # Gęstość powietrza
    base_cda = 0.38     # Baza aerodynamiczna dla pozycji Standard
    base_crr = 0.005    # Baza tarcia opon szosowych
    
    # Pobieramy mnożniki z naszych słowników
    cda = base_cda * POSITION_MULTIPLIERS.get(position, 1.0)
    crr = base_crr * BIKE_ROLLING_RESISTANCE.get(bike, 1.0)
    
    # Przeliczenie na system metryczny (metry i sekundy)
    v_ms = (distance_km * 1000) / (duration_min * 60)
    
    # Wzór na moc oporu powietrza: 0.5 * rho * CdA * v^3
    power_air = 0.5 * rho * cda * (v_ms ** 3)
    
    # Wzór na moc oporu toczenia: Crr * masa * g * v
    power_rolling = crr * weight * 9.81 * v_ms
    
    return power_air + power_rolling


# ==========================================
# 3. MÓZG OPERACYJNY (Główna funkcja)
# ==========================================
def estimate_performance(data: dict) -> dict:
    """
    Przyjmuje słownik z odpowiedziami z quizu.
    Zwraca słownik z wynikami lub listą błędów.
    """
    # KROK 1: Pytamy strażnika o zgodę
    validation_errors = validate_input(data)
    if validation_errors:
        return {"status": "error", "messages": validation_errors}

    # KROK 2: Drzewo decyzyjne - Góry czy Płasko?
    if data['terrain_type'] == "Góry":
        raw_power = calculate_vam_model(data['weight_total'], data['elevation_gain'], data['duration_min'])
    else:
        # Płasko lub Pagórki
        raw_power = calculate_aero_model(data['weight_total'], data['distance_km'], data['duration_min'], data['position_type'], data['bike_type'])
        
        # Jeśli są to "Pagórki", dodajemy drobną premię za grawitację (opcjonalnie)
        if data['terrain_type'] == "Pagórki":
            raw_power += calculate_vam_model(data['weight_total'], data['elevation_gain'], data['duration_min']) * 0.3 # 30% wpływu gór

    # KROK 3: Nakładamy mnożnik RPE (skala 1-10)
    # RPE 10 to nasz maks (100%). Każdy punkt mniej w dół dodaje 5% do teoretycznego FTP.
    rpe = data['rpe_score']
    ftp_multiplier = 1.0 + ((10 - rpe) * 0.05)
    
    estimated_ftp = raw_power * ftp_multiplier

    # KROK 4: Pakujemy wyniki do ładnego słownika
    return {
        "status": "success",
        "avg_power": round(raw_power, 1),
        "estimated_ftp": round(estimated_ftp, 1),
        "w_kg": round(estimated_ftp / data['weight_total'], 2)
    }

