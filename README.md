# 🚴‍♂️ Cycling Pro-Am Analyzer (AI Coach)


Profesjonalna aplikacja webowa typu Full-Stack (Frontend + Backend API + Baza Danych) zaprojektowana dla kolarzy. Projekt pozwala na analizę treningów w oparciu o prawdziwe wzory fizyczne (opory powietrza, tarcie, grawitacja), obliczanie kluczowych wskaźników (FTP, VAM, W/kg) oraz generowanie spersonalizowanych porad za pomocą sztucznej inteligencji (OpenAI).

---

## ✨ Główne Funkcje (Features)

- **🧠 Silnik Fizyczny w Czasie Rzeczywistym:** Kalkulacja mocy na podstawie nachylenia, pozycji aerodynamicznej, rodzaju roweru i masy.
- **🤖 Trener AI:** Integracja z OpenAI API. Wirtualny trener analizuje wyliczone dane i współczynnik odczuwanego zmęczenia (RPE), dostarczając złośliwe, ale merytoryczne porady (w stylu "Koneser Kawiarni" vs "Lokalny Dzik").
- **🔐 Autoryzacja Google (SSO):** Bezpieczne i błyskawiczne logowanie za pomocą konta Google.
- **🗂️ Chmurowa Baza Danych:** Automatyczny zapis historii treningów dla każdego zalogowanego użytkownika (zabezpieczone przez Row Level Security).
- **📈 Drabina Formy (UI):** Interaktywny, płynny interfejs pokazujący aktualny poziom kolarza w oparciu o wyliczony stosunek W/kg.

---

## 🛠️ Tech Stack

Aplikacja została zbudowana w architekturze oddzielonego Frontendu i Backendu.

**Frontend:**
- **HTML5 / JavaScript (ES6+)** - Czysty, wydajny "Vanilla" JS bez ciężkich frameworków.
- **Tailwind CSS** - Ultraszybkie i responsywne stylowanie.
- **Supabase JS SDK** - Komunikacja z autoryzacją i bazą danych.
- **Marked.js** - Formatowanie odpowiedzi AI (Markdown do HTML).
- **Hosting:** Vercel

**Backend (REST API):**
- **Python 3.10+** - Główny język logiki serwera.
- **FastAPI** - Nowoczesny, niezwykle szybki framework do budowy API.
- **Pydantic** - Walidacja danych przychodzących z Frontendu.
- **OpenAI (GPT)** - Generowanie analizy tekstowej.
- **Hosting:** Render

**Baza Danych & Autoryzacja:**
- **Supabase (PostgreSQL)** - Tabele z politykami RLS (Row Level Security).
- **Google OAuth 2.0** - Dostawca tożsamości (Identity Provider).

---

## 🧮 Silnik Fizyczny (Jak to działa?)

Aplikacja opiera się na podstawowym równaniu fizyki ruchu rowerzysty. Aby utrzymać prędkość na rowerze, kolarz musi pokonać trzy główne siły. Serwer przelicza czas, dystans i przewyższenie na prędkość, a następnie wylicza moc ze wzoru:

**P_całkowita = P_grawitacji + P_toczenia + P_aero**

1. **Opór Grawitacji ($P_{grawitacji}$):** `m * g * v * sin(kąt)`
   Zależny od podanej masy (kolarz + rower) i wyliczonego z trasy nachylenia.
2. **Opór Toczenia ($P_{toczenia}$):** `m * g * v * Crr * cos(kąt)`
   Zależny od wybranego wariantu roweru (Szosa, Gravel, MTB), który dynamicznie zmienia współczynnik `Crr`.
3. **Opór Powietrza ($P_{aero}$):** `0.5 * rho * v^3 * CdA`
   Opór rośnie z **sześcianem prędkości**! Wybrana pozycja (Aero, Standard, Wyprostowana) modyfikuje pole powierzchni czołowej (`CdA`).

Na podstawie wyliczonej Mocy Średniej z treningu oraz wskaźnika RPE (Zmęczenie 1-10), algorytm szacuje ostateczne **FTP (Functional Threshold Power)** oraz **VAM (Prędkość wznoszenia w m/h)**.

---

## 📂 Struktura Projektu

cycling-pro-am-analyzer/
│
├── frontend/
│   ├── index.html       # Główny widok aplikacji, formularze, modal
│   └── app.js           # Logika UI, kalkulacje na żywo, API calls, Supabase
│
├── backend/
│   ├── main.py          # Główny plik serwera FastAPI (API, OpenAI prompt)
│   ├── logic.py         # Silnik fizyczny (kalkulacje FTP, W/kg, VAM)
│   ├── database.py      # Lokalna "baza" danych (drabina formy, regeneracja)
│   └── requirements.txt # Zależności Pythona (fastapi, openai, uvicorn)
│
├── .gitignore           # Ignorowane pliki systemowe i wirtualne środowiska
└── README.md            # Dokumentacja projektu


🚀 Roadmapa Projektu: Kierunki Rozwoju Aplikacji
Celem długofalowym projektu jest stworzenie kompleksowego ekosystemu analityczno-treningowego dla kolarzy amatorów, łączącego rzetelną fizykę z zaawansowaną sztuczną inteligencją. Główne założenia rozwojowe na kolejne etapy życia produktu:

1. Weryfikacja Treningów (Integracja ze Strava API)

Koncepcja: Zastąpienie ręcznego wprowadzania danych automatycznym pobieraniem aktywności z platformy Strava.

Wartość: Gwarantuje to autentyczność wyników (dystans, czas, przewyższenie), zapobiega fałszowaniu statystyk i uwiarygadnia całą platformę.

2. Globalny Ranking Użytkowników (Leaderboard / Grywalizacja)

Koncepcja: Wprowadzenie opcjonalnego, publicznego zestawienia kolarzy na podstawie wyliczonego stosunku W/kg oraz FTP.

Wartość: Wprowadza element zdrowej rywalizacji. Użytkownicy mogą śledzić swoje postępy na tle innych zawodników, co znacząco zwiększa retencję i zaangażowanie w aplikacji.

3. Wirtualne Ligi i Lokalne Segmenty

Koncepcja: Stworzenie bazy legendarnych podjazdów i popularnych pętli kolarskich (z przypisanymi na sztywno danymi o dystansie i przewyższeniu).

Wartość: Aplikacja, opierając się na aktualnym FTP użytkownika, estymuje czas przejazdu konkretnego segmentu. AI analizuje brakujący czas do "pobicia rekordu" i rozpisuje precyzyjny plan treningowy, przekształcając suche statystyki w mierzalne, inspirujące cele.

4. Detektyw Aerodynamiki (Test współczynnika CdA)

Koncepcja: Funkcja premium dla użytkowników posiadających fizyczne mierniki mocy w rowerach.

Wartość: Algorytm porównuje moc rzeczywistą (odczyt z korby) z mocą estymowaną przez silnik fizyczny aplikacji przy danej prędkości. Pozwala to na obliczenie strat aerodynamicznych i udzielenie wskazówek dotyczących poprawy pozycji na rowerze (np. "zbyt wyprostowana sylwetka kosztuje Cię 40W").

5. Interaktywna Wizualizacja Postępów

Koncepcja: Rozbudowa panelu historii o zaawansowane wykresy liniowe i słupkowe (np. z wykorzystaniem biblioteki Chart.js).

Wartość: Przekształcenie surowych kafelków z danymi w czytelną oś czasu, pokazującą trend wzrostowy formy i pomagającą w planowaniu szczytów formy w sezonie.

6. Generowanie "Wizytówek" Społecznościowych

Koncepcja: Wbudowany generator estetycznych grafik (kwadratów / pionowych plansz) podsumowujących ostatnią jazdę wraz z najciekawszym cytatem od AI Coacha.

Wartość: Użytkownicy mogą łatwo udostępniać swoje wyniki na Instagram Stories lub Strava. Działa to jako potężny silnik marketingu wirusowego (viral) i buduje organiczny zasięg aplikacji.

7. Eksport Treningów do Komputerów Rowerowych (.zwo / .fit)

Koncepcja: Automatyczna konwersja planów treningowych rozpisanych przez sztuczną inteligencję do formatów obsługiwanych przez urządzenia zewnętrzne (Garmin, Wahoo) oraz symulatory (Zwift).

Wartość: Pełna automatyzacja procesu: od analizy, przez ułożenie planu, aż po jego fizyczną realizację, co czyni aplikację w pełni profesjonalnym narzędziem trenerskim.

