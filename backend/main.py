# ==========================================
# CYCLING PRO-AM ANALYZER - GŁÓWNY SERWER API (FastAPI)
# ==========================================

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI, AuthenticationError

# Importujemy naszą logikę fizyczną i bazę danych
import logic
import database 

app = FastAPI(title="Cycling AI Coach API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=False, 
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuizData(BaseModel):
    weight_total: float
    distance_km: float
    duration_min: int
    elevation_gain: int
    terrain_type: str
    position_type: str
    bike_type: str
    rpe_score: int
    openai_api_key: str 

@app.post("/api/analyze")
async def analyze_ride(data: QuizData):
    
    # 1. Walidacja klucza API z formularza
    if not data.openai_api_key or not data.openai_api_key.startswith("sk-"):
        raise HTTPException(status_code=400, detail=["Nieprawidłowy klucz API. Klucz OpenAI musi zaczynać się od 'sk-'."])

    # 2. Pydantic -> Słownik
    user_dict = data.model_dump() if hasattr(data, 'model_dump') else data.dict()
    
    # 3. Fizyka i Strażnik (logic.py)
    logic_result = logic.estimate_performance(user_dict)
    if logic_result["status"] == "error":
        raise HTTPException(status_code=400, detail=logic_result["messages"])
        
    user_wkg = logic_result['w_kg']
    
    # --- Obliczenie średniej prędkości ---
    avg_speed = round(data.distance_km / (data.duration_min / 60), 1)
    
    # NOWOŚĆ: Tworzymy "Żelazne Zdanie" prosto z Pythona
    forced_intro = f"Twoje wyliczone FTP z tego treningu to **{logic_result['estimated_ftp']} W**, co daje stosunek **{user_wkg} W/kg**. Twoja średnia prędkość wyniosła **{avg_speed} km/h**."
    
    # 4. Lokalne funkcje z database.py
    ladder_data = database.get_comparison_data(user_wkg, data.terrain_type)
    recovery_data = database.analyze_fatigue_and_recovery(data.rpe_score, data.duration_min)

   # 5. PROMPT INJECTION (Nowa logiczna kolejność + Wyróżniony Plan Treningowy)
    prompt = f"""
    Jesteś profesjonalnym Trenerem Kolarstwa. Przeanalizuj poniższe dane amatora i napisz do niego odpowiedź.
    
    TWARDE DANE Z JAZDY I FIZYKI:
    - Zmęczenie mięśniowe wg systemu: {recovery_data['fatigue_level']}
    - Zalecenie regeneracyjne systemu: {recovery_data['recovery_advice']}

    MIEJSCE NA DRABINIE KOLARSKIEJ:
    - Obecna kategoria: {ladder_data['user_category']} ({ladder_data['category_desc']})
    - Brakuje mu: {ladder_data['gap_to_next_wkg']} W/kg, aby wejść o poziom wyżej.
    - Twój idol do porównania w tym terenie to: {ladder_data['pro_benchmark']} ({ladder_data['pro_desc']})

    TWOJE ZADANIE:
    Masz wygenerować odpowiedź używając BARDZO CZYTELNEGO i przewiewnego formatowania.
    Każdy z 7 punktów MUSI zaczynać się od nagłówka poziomu 3 (czyli użyj: ### ).
    Używaj list punktowanych (myślników), aby łamać bloki tekstu.
    
    Oto DOKŁADNA STRUKTURA I KOLEJNOŚĆ, której musisz użyć:

    ### 📊 1. Twój wynik z dzisiejszej jazdy
    {forced_intro}
    - Skomentuj krótko tę prędkość w kontekście terenu ({data.terrain_type}).

    ---
    ### 🎯 2. Twoje miejsce na Drabinie Formy
    - Jesteś obecnie w kategorii: **{ladder_data['user_category']}**.
    - Brakuje Ci dokładnie **{ladder_data['gap_to_next_wkg']} W/kg**, aby wejść poziom wyżej. Zmotywuj go do tego.

    ---
    ### 👽 3. Przepaść do PRO
    - Twój punkt odniesienia to **{ladder_data['pro_benchmark']}**.
    - Napisz krótki, złośliwy lub zabawny komentarz o różnicy Waszych poziomów.

    ---
    ### 🦵 4. Stan Twoich Nóg
    - Otrzymany sygnał od organizmu: **{recovery_data['fatigue_level']}**.
    - Skomentuj krótko, jak bardzo się zajechał i doradź konkretnie, co ma zrobić na następnym treningu.

    ---
    ### 📅 5. Plan Treningowy na ten tydzień
    - Rozpisz 3 proponowane dni treningowe. Użyj DOKŁADNIE takiego formatowania z użyciem znaku cytatu (>) dla każdego dnia:
    > 🔹 **Pierwszy trening (np. Wtorek - Interwały):** *[Krótki opis co ma robić]*
    > 🔹 **Drugi trening (np. Czwartek - Tlen):** *[Krótki opis co ma robić]*
    > 🔹 **Trzeci trening (np. Weekend - Long Run):** *[Krótki opis co ma robić]*

    ---
    ### 🍝 6. Baza to Talerz i Łóżko
    - Przypomnij o zjedzeniu posiłku węglowodanowo-białkowego do 60 minut po jeździe.
    - Forma rośnie podczas snu, a nie na siodełku.

    ---
    ### 🔬 7. Prawda o Twoim FTP (Jak to sprawdzić)
    - Wyjaśnij, że dzisiejszy wynik to bardzo dobra estymacja.
    - Jeśli chcesz poznać w 100% prawdziwe FTP: Zrób porządną rozgrzewkę, a potem jedź przez równe **20 minut na absolutnego maksa** (aż do odcięcia prądu).
    - **Instrukcja powrotu:** Zapisz dystans i przewyższenie z tych 20 minut. Wróć do naszej aplikacji, wpisz te dane z prawej strony, czas ustaw na 20 min, a suwak Zmęczenia (RPE) wbij na równe 10 (Maks). Algorytm wyliczy Twoje FTP za Ciebie!

    BARDZO WAŻNE ZASADY DLA CIEBIE:
    To jest system jednorazowej analizy bez możliwości czatu zwrotnego. NIE ZADAWAJ na końcu żadnych pytań.
    TRZYMAJ SIĘ SZTYWNO POWYŻSZYCH NAGŁÓWKÓW (###) ORAZ ZNAKÓW LINII (---).
    """

    # 6. INICJALIZACJA KLIENTA I WYSYŁKA DO OPENAI
    try:
        client = OpenAI(api_key=data.openai_api_key)
        
        response = client.chat.completions.create(
            model="gpt-5.4-mini", 
            messages=[
                {"role": "system", "content": "Jesteś wspierającym trenerem kolarstwa. Znasz klimat ustawek, używasz słów jak 'łydka', 'wypruwać flaki', 'kręcić waty'."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8 
        )
        ai_coach_message = response.choices[0].message.content
        
    except AuthenticationError:
        raise HTTPException(status_code=401, detail=["Podano błędny klucz API OpenAI. Sprawdź, czy skopiowałeś go poprawnie."])
    except Exception as e:
        raise HTTPException(status_code=500, detail=[f"Błąd połączenia z AI: {str(e)}"])

    # 7. Zwracamy paczkę danych do przeglądarki
    return {
        "status": "success",
        "calculations": logic_result,
        "ladder_data": ladder_data, 
        "ai_coach_advice": ai_coach_message
    }