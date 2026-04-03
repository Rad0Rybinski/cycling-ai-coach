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
    
    # 4. Lokalne funkcje z database.py
    ladder_data = database.get_comparison_data(user_wkg, data.terrain_type)
    recovery_data = database.analyze_fatigue_and_recovery(data.rpe_score, data.duration_min)

  # 5. PROMPT INJECTION
    prompt = f"""
    Jesteś profesjonalnym Trenerem Kolarstwa. Przeanalizuj poniższe dane amatora i napisz do niego odpowiedź.
    
    TWARDE DANE Z JAZDY I FIZYKI:
    - Wyliczone FTP: {logic_result['estimated_ftp']} W ({user_wkg} W/kg)
    - Zmęczenie mięśniowe wg systemu: {recovery_data['fatigue_level']}
    - Zalecenie regeneracyjne systemu: {recovery_data['recovery_advice']}

    MIEJSCE NA DRABINIE KOLARSKIEJ:
    - Obecna kategoria: {ladder_data['user_category']} ({ladder_data['category_desc']})
    - Brakuje mu: {ladder_data['gap_to_next_wkg']} W/kg, aby wejść o poziom wyżej.
    
    KOSMICZNY BENCHMARK (PRO):
    - Twój idol do porównania w tym terenie to: {ladder_data['pro_benchmark']} ({ladder_data['pro_desc']})

    TWOJE ZADANIE (Odpowiedz dokładnie w tych 7 punktach. PO KAŻDYM PUNKCIE OBOWIĄZKOWO DODAJ POZIOMĄ LINIĘ MARKDOWN `---`, aby oddzielić je od siebie):
    
    1. 📊 **Twój wynik**: Podaj wyliczone FTP i W/kg.
    2. 🦵 **Stan Twoich Nóg**: Użyj danych o regeneracji z systemu, by powiedzieć, jak bardzo się zajechał na tym treningu i doradź, co zrobić jutro.
    3. 🎯 **Twoje miejsce na Drabinie**: Powiedz mu, że jest obecnie w kategorii "{ladder_data['user_category']}". Zmotywuj go, mówiąc dokładnie, że brakuje mu {ladder_data['gap_to_next_wkg']} W/kg do kolejnego poziomu.
    4. 👽 **Przepaść do PRO**: Jako ciekawostkę zrzuć go na ziemię, porównując go z {ladder_data['pro_benchmark']}.
    5. 📅 **Konkretny Plan Treningowy**: Zamiast pytać czy chce, OD RAZU rozpisz mu konkretne 3 treningi na ten tydzień (krótko, zwięźle i na temat).
    6. 🔬 **Prawda o Twoim FTP (Jak to sprawdzić)**: 
       - Wyjaśnij krótko, że dzisiejszy wynik to bardzo dobra estymacja oparta o czystą fizykę i odczucie zmęczenia (RPE).
       - Tłumacząc prosto: "Chcesz poznać swoje w 100% prawdziwe FTP, ale nie masz miernika mocy w rowerze? Żaden problem! Zrób porządną rozgrzewkę, a potem jedź przez równe 20 minut na absolutnego maksa (aż do odcięcia prądu)."
       - Daj mu instrukcję powrotu: "Zapisz dystans i przewyższenie z tych 20 minut. Wróć do naszej aplikacji, wpisz te dane w formularz z prawej strony, czas ustaw na 20 min, a suwak Zmęczenia (RPE) wbij na równe 10 (Maks). Nasz algorytm wyliczy Twoje FTP za Ciebie i pokaże Ci Twoje prawdziwe miejsce na Drabinie Formy!"
    7. 🍝 **Baza to Talerz i Łóżko**: Przypomnij mu, żeby w ciągu 30-60 minut po mocnej jeździe zjadł posiłek węglowodanowo-białkowy. Uświadom go, że formę buduje się podczas snu i odpoczynku, a nie na siodełku.

    BARDZO WAŻNE ZASADY DLA CIEBIE:
    To jest system jednorazowej analizy bez możliwości czatu zwrotnego. 
    NIE ZADAWAJ na końcu żadnych pytań. NIE OFERUJ dodatkowej pomocy.
    Pamiętaj o wstawieniu `---` pomiędzy każdym z 7 punktów!
    Zakończ tekst mocnym, kolarskim pozdrowieniem.
    """

    # 6. INICJALIZACJA KLIENTA I WYSYŁKA DO OPENAI
    # Używamy klucza podanego przez użytkownika!
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