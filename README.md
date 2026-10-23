# Vremea CLI — aplicație de consultare a vremii în terminal

## Descriere

**Vremea CLI** este o aplicație simplă de linie de comandă, scrisă în Python, care afișează starea curentă a vremii pentru orice oraș introdus de utilizator. Aplicația folosește API-ul public **OpenWeatherMap**: mai întâi transformă numele orașului în coordonate geografice (latitudine/longitudine), apoi interoghează serviciul de vreme curentă și afișează descrierea vremii, temperatura și viteza vântului, în limba română.

## Tehnologii utilizate

| Tehnologie | Rol |
|---|---|
| **Python 3.8+** | Limbajul de programare al aplicației |
| **requests** | Bibliotecă pentru cereri HTTP către API-ul OpenWeatherMap |
| **python-dotenv** | Încărcarea cheii API din fișierul `.env`, fără a o scrie în cod |
| **OpenWeatherMap API** | Sursa datelor meteo (Geocoding API + Current Weather API) |

## Problema pe care o rezolvă aplicația

Verificarea rapidă a vremii presupune de obicei deschiderea unui browser sau a unei aplicații mobile pline de reclame. Această aplicație oferă o metodă **rapidă, minimală și fără distrageri** de a afla vremea direct din terminal, prin introducerea unui singur cuvânt — numele orașului. Este utilă dezvoltatorilor, utilizatorilor care lucrează mult în terminal sau ca exemplu didactic de integrare a unui API REST în Python.

## Funcționalități

- Introducerea numelui unui oraș de la tastatură (orice oraș din lume, în orice limbă acceptată de OpenWeatherMap);
- Conversia automată a numelui orașului în coordonate geografice (geocoding);
- Afișarea stării vremii (ex. „cer senin”, „ploaie ușoară”) în limba română;
- Afișarea temperaturii curente în grade Celsius;
- Afișarea vitezei vântului în m/s;
- Mesaj de eroare clar dacă orașul nu a fost găsit;
- Curățarea ecranului terminalului la pornire (compatibil Windows, Linux și macOS);
- Păstrarea cheii API în fișierul `.env`, în afara codului sursă.

## Motivarea alegerii tehnologiilor

- **Python** — sintaxă simplă și lizibilă, ecosistem bogat de biblioteci, ideal pentru aplicații mici de tip utilitar și pentru scopuri didactice.
- **requests** — este standardul de facto pentru cereri HTTP în Python; API-ul său este mult mai simplu și mai sigur decât modulul standard `urllib`, iar metoda `.json()` parsează răspunsul direct într-un dicționar.
- **python-dotenv** — permite separarea datelor sensibile (cheia API) de cod. Astfel codul poate fi publicat pe GitHub fără riscul de a expune cheia, iar fiecare utilizator își folosește propria cheie.
- **OpenWeatherMap** — oferă un plan gratuit generos (1 000 de cereri/zi), documentație bună, suport pentru limba română și un API separat de geocoding, ceea ce face rezultatele mai precise decât căutarea directă după nume.

## Arhitectura aplicației

Aplicația are o arhitectură liniară, într-un singur fișier (`main.py`), și urmează fluxul de mai jos:

```
┌──────────────────────┐
│ 1. Încărcare config  │  load_dotenv() → citește API_KEY din .env
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ 2. Intrare utilizator│  input("Introduceti orasul: ")
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ 3. Geocoding API     │  GET /geo/1.0/direct?q=<oras>&limit=1
│    (oraș → lat, lon) │  → [{lat, lon, ...}]  sau  []  (oraș negăsit)
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ 4. Weather API       │  GET /data/2.5/weather?lat=&lon=&units=metric&lang=ro
│    (lat, lon → vreme)│  → {weather, main, wind, ...}
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ 5. Afișare rezultat  │  descriere, temperatură (°C), vânt (m/s)
└──────────────────────┘
```

**Componente:**

| Componentă | Descriere |
|---|---|
| `.env` | Fișier de configurare local; conține `API_KEY`. Nu se urcă în repozitoriu. |
| `main.py` | Logica aplicației: citire config, input, două apeluri HTTP, afișare. |
| OpenWeatherMap Geocoding API | Serviciu extern — transformă numele orașului în coordonate. |
| OpenWeatherMap Current Weather API | Serviciu extern — returnează vremea curentă pentru coordonate. |

Structura proiectului:

```
vremea-cli/
├── main.py          # codul aplicației
├── .env             # cheia API (NU se publică)
├── .env.example     # model pentru .env
├── requirements.txt # dependențe Python
└── README.md        # această documentație
```

## Instalare și rulare (ce trebuie să facă o altă persoană)

### 1. Cerințe preliminare

- Python 3.8 sau mai nou instalat (`python --version`);
- `pip` (vine odată cu Python);
- Un cont gratuit pe [openweathermap.org](https://openweathermap.org/) și o cheie API (secțiunea *My API keys*). Cheia devine activă la câteva minute–ore după creare.

### 2. Descărcarea proiectului

```bash
git clone https://github.com/<utilizator>/vremea-cli.git
cd vremea-cli
```

### 3. Crearea unui mediu virtual (recomandat)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### 4. Instalarea dependențelor

Creați fișierul `requirements.txt` cu conținutul:

```
requests
python-dotenv
```

apoi rulați:

```bash
pip install -r requirements.txt
```

### 5. Configurarea cheii API

Creați în rădăcina proiectului un fișier numit `.env` cu următorul conținut (înlocuiți cu propria cheie):

```
API_KEY=cheia_voastra_openweathermap
```

> ⚠️ Nu puneți niciodată cheia API direct în cod și nu publicați fișierul `.env`. Adăugați `.env` în `.gitignore`.

### 6. Rularea aplicației

```bash
python main.py
```

Exemplu de utilizare:

```
Introduceti orasul: Chisinau
Starea vremii in Chisinau este: cer senin. Temperatura este de 14.3°C, iar viteza vantului este de 3.6 m/s.
```

## Limitele aplicației

- **Necesită conexiune la internet** — fără internet aplicația nu poate obține datele.
- **Depinde de un serviciu extern** — dacă OpenWeatherMap este indisponibil sau cheia API este invalidă/inactivă, aplicația nu funcționează.
- **Limita planului gratuit** — maximum 60 de cereri/minut și 1 000 de cereri/zi; fiecare consultare consumă 2 cereri (geocoding + vreme).
- **Doar vremea curentă** — nu oferă prognoză pe mai multe zile sau date istorice.
- **Ambiguitatea orașelor** — se folosește doar primul rezultat al geocodării (`limit=1`); pentru orașe cu același nume (ex. „Paris” din Franța vs. Texas) se poate alege un oraș greșit. Se poate specifica țara: `Paris,FR`.
- **Tratare limitată a erorilor** — în versiunea curentă, dacă orașul nu este găsit, variabila `raspuns` nu este definită, iar liniile de după blocul `else` generează o eroare (`NameError`). De asemenea, erorile de rețea (timeout, lipsă conexiune) și cheia API invalidă nu sunt gestionate explicit. Recomandare: mutarea afișării în interiorul blocului `else` și folosirea `try/except`.
- **Interfață doar în consolă** — nu există interfață grafică.
- **Fără cache** — fiecare rulare face cereri noi către API.

## Autori

- **Fiodorov Vladimir** — proiectare, implementare, documentație

## Licențiere și copierea codului

Acest proiect este distribuit sub licența **MIT**.

Aceasta înseamnă că oricine poate **copia, modifica, distribui și folosi codul**, inclusiv în scopuri comerciale, cu următoarele condiții:

1. Notificarea de copyright și textul licenței trebuie păstrate în toate copiile sau porțiunile substanțiale ale codului;
2. Codul este furnizat „ca atare”, **fără nicio garanție**; autorii nu răspund pentru eventuale daune rezultate din utilizarea lui.

```
MIT License

Copyright (c) 2026 Fiodorov Vladimir

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

> **Notă:** datele meteo aparțin OpenWeatherMap și sunt supuse [termenilor lor de utilizare](https://openweathermap.org/terms). Licența MIT acoperă doar codul acestui proiect, nu și datele furnizate de API.