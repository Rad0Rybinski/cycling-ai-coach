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