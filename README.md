# Cycling Pro-Am Analyzer 🚴‍♂️ 🇳🇱

Interaktywna aplikacja webowa dla kolarzy amatorów, łącząca zaawansowaną fizykę sportu z mocą Sztucznej Inteligencji (OpenAI). Sprawdź swoje miejsce na Drabinie Formy i zdobądź spersonalizowany plan treningowy!

## 🌟 Główne Funkcje

* **Fizyka pod maską:** Aplikacja oblicza VAM (Prędkość Wznoszenia) oraz estymuje FTP (W/kg) na podstawie wprowadzonych danych, uwzględniając opory powietrza, tarcie opon i nachylenie terenu.
* **Magiczne Lustro (Synchronizacja UI):** Lewa kolumna edukacyjna (suwaki) i prawy formularz treningowy "rozmawiają" ze sobą w czasie rzeczywistym.
* **Auto-Detekcja Terenu:** Algorytm automatycznie rozpoznaje, czy Twój trening odbył się na płaskim, w pagórkach, czy w prawdziwych górach (na podstawie stosunku przewyższenia do dystansu).
* **Interaktywna Drabina Formy:** Animowany wykres wizualizujący Twoją kategorię (od "Konesera Kawiarni" do "Pro").
* **AI Coach (BYOK - Bring Your Own Key):** Generowanie spersonalizowanych porad i planów treningowych z użyciem OpenAI API. Klawisz API jest podawany przez użytkownika i bezpiecznie przechowywany tylko w pamięci lokalnej przeglądarki (`localStorage`).

## 🛠️ Technologie

* **Frontend:** HTML5, Vanilla JavaScript, Tailwind CSS (motyw kolarski "Oranje"), Marked.js
* **Backend:** Python 3, FastAPI, Pydantic, Uvicorn
* **AI:** OpenAI API (gpt-5.4-mini)

## 📁 Struktura Projektu

```text
├── frontend/
│   ├── index.html        # Główny interfejs użytkownika
│   └── app.js            # Logika UI i komunikacja z API
├── backend/
│   ├── main.py           # Serwer FastAPI i integracja OpenAI
│   ├── logic.py          # Obliczenia fizyczne i estymacja FTP
│   └── database.py       # Słowniki kategoryzacji i benchmarki PRO
├── .gitignore
└── README.md