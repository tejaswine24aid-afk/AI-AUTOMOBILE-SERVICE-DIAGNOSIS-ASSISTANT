# 🚗 Automobile Service Diagnosis Assistant

A clean, lightweight, and complete **1-Credit College Mini Project** for preliminary automotive fault identification and service guidance.

---

## 📌 Project Overview

The **Automobile Service Diagnosis Assistant** is an educational, web-based expert decision-support tool. It assists vehicle owners and drivers in identifying potential automotive issues by analyzing reported symptoms against a rule-based automobile knowledge base. 

The application follows an **API-driven architecture** separating the **Streamlit** user interface from the **FastAPI** diagnosis engine, with diagnosis records stored in an embedded **SQLite** database.

---

## 🎯 Project Objective

> *"To provide a simple, clean, and user-friendly tool for preliminary automobile problem identification, severity assessment, basic DIY checks, and professional service guidance."*

---

## 🚀 Key Features

* **🔍 Symptom Diagnosis:** Enter custom symptom descriptions or select from 10 common automotive problem categories.
* **⚙️ Rule-Based Knowledge Engine:** Intelligent keyword matching analyzing symptoms for root causes without complex or heavy machine learning models.
* **🚦 4-Level Severity Indicator:** Clear categorization of issues (`Urgent 🔴`, `High 🟠`, `Medium 🟡`, `Low 🟢`).
* **🔧 Actionable Service Guidance:** Provides practical under-the-hood inspection steps and recommended corrective actions.
* **📋 Persistent Diagnosis History:** Automatically stores all diagnosis sessions into an SQLite database (`data/automobile.db`).
* **🛡️ Built-in Disclaimer:** Informs users that the system provides preliminary guidance and advises professional mechanic consultation.
* **🎨 Modern Automotive Dark UI:** Professional dark navy theme with clean cards, responsive layout, and intuitive navigation.

---

## 🛠️ Technologies Used

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Language** | Python 3.10+ | Core programming language |
| **Backend API** | FastAPI | High-performance RESTful API endpoints |
| **ASGI Server** | Uvicorn | Web server for FastAPI |
| **Frontend** | Streamlit | Interactive web application UI |
| **Database** | SQLite3 | Embedded database for history tracking |
| **Validation** | Pydantic | Request/response data validation |
| **HTTP Client** | Requests | Streamlit-to-FastAPI communication |

---

## 📐 System Architecture

```text
       ┌────────────────────────┐
       │   User / Web Browser   │
       └───────────┬────────────┘
                   │
                   ▼
       ┌────────────────────────┐
       │   Streamlit Frontend   │  (Port 8501)
       │    (frontend/app.py)   │
       └───────────┬────────────┘
                   │  HTTP REST (JSON)
                   ▼
       ┌────────────────────────┐
       │    FastAPI Backend     │  (Port 8000)
       │   (backend/main.py)    │
       └─────┬────────────┬─────┘
             │            │
             ▼            ▼
┌──────────────────┐  ┌──────────────────┐
│ Diagnosis Engine │  │ SQLite Database  │
│ (diagnosis.py)   │  │ (automobile.db)  │
└──────────────────┘  └──────────────────┘
```

---

## 📂 Project Structure

```text
automobile-diagnosis/
│
├── backend/
│   ├── __init__.py
│   ├── main.py             # FastAPI REST endpoints & lifecycle
│   ├── diagnosis.py        # Knowledge base & symptom matching logic
│   └── database.py         # SQLite connection & database operations
│
├── frontend/
│   ├── __init__.py
│   └── app.py              # Streamlit web interface & dark automotive UI
│
├── data/
│   └── automobile.db       # SQLite database (auto-created on startup)
│
├── requirements.txt        # Minimal project dependencies
├── README.md               # Project documentation
└── run_app.bat             # One-click startup script for Windows
```

---

## 🧠 Automotive Knowledge Base (10 Supported Issues)

The system covers 10 primary automotive failure modes:

1. **Battery Problem:** Depleted battery, terminal corrosion, or starter motor issues.
2. **Engine Overheating:** Coolant loss, radiator leak, or broken cooling fan.
3. **Brake Problem:** Worn brake pads, warped rotors, or low brake fluid.
4. **Flat Tyre:** Punctures, valve stem leaks, or pressure loss.
5. **Engine Oil Problem:** Low engine oil level, oil leaks, or oil filter clogs.
6. **AC Not Cooling:** Refrigerant leak, clogged cabin filter, or compressor failure.
7. **Engine Misfire:** Bad spark plugs, failing ignition coils, or fuel injector issues.
8. **Poor Acceleration:** Dirty air filter, faulty MAF sensor, or fuel line restriction.
9. **Check Engine Light:** Loose fuel cap, failing O2 sensor, or emissions fault.
10. **Alternator Problem:** Charging system failure, loose serpentine belt, or bad diodes.

---

## ⚙️ Installation & Setup

### Prerequisites

* Python 3.10 or higher installed.

### 1. Install Dependencies

Open a terminal in the project directory and run:

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run the Application

### Option 1: One-Click Script (Windows)

Double-click or run:
```cmd
run_app.bat
```

### Option 2: Manual Start (Two Terminals)

**Terminal 1 — Start FastAPI Backend:**
```bash
uvicorn backend.main:app --reload --port 8000
```

**Terminal 2 — Start Streamlit Frontend:**
```bash
streamlit run frontend/app.py
```

### 🌐 Access URLs

* **Streamlit Web App:** [http://localhost:8501](http://localhost:8501)
* **FastAPI Backend Root:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
* **Interactive Swagger API Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📡 REST API Documentation

### 1. Health Check
* **Endpoint:** `GET /api/health`
* **Response:**
  ```json
  {
    "status": "running"
  }
  ```

### 2. Vehicle Diagnosis
* **Endpoint:** `POST /api/diagnose`
* **Request Body:**
  ```json
  {
    "vehicle": "Car",
    "symptom": "Engine is overheating and coolant is leaking"
  }
  ```
* **Response:**
  ```json
  {
    "vehicle": "Car",
    "symptom": "Engine is overheating and coolant is leaking",
    "problem": "Engine Overheating",
    "possible_cause": "Low coolant level, radiator hose leak, defective radiator cooling fan, or stuck closed thermostat.",
    "severity": "Urgent",
    "basic_checks": [
      "Check coolant expansion tank level ONLY after the engine has completely cooled down.",
      "Inspect underneath the engine bay for visible bright colored fluid puddles (coolant).",
      "Check if the radiator electric cooling fan activates when the engine warms up."
    ],
    "recommended_action": "Stop using the vehicle immediately in a safe spot, switch off the engine, and avoid opening the radiator cap while hot. Seek towing or professional inspection.",
    "disclaimer": "This is a preliminary diagnosis assistant. Consult a qualified mechanic for final inspection and repair."
  }
  ```

### 3. Diagnosis History
* **Endpoint:** `GET /api/history`
* **Response:**
  ```json
  [
    {
      "id": 1,
      "date": "2026-09-29 21:50:28",
      "vehicle": "Car",
      "symptom": "Engine is overheating",
      "diagnosis": "Engine Overheating",
      "severity": "Urgent"
    }
  ]
  ```

---

## 🔮 Future Enhancements

1. **OBD-II Bluetooth / Wi-Fi Integration:** Reading live sensor data (DTC codes, RPM, coolant temp) directly from the vehicle's ECU.
2. **Audio Diagnosis:** Using audio processing to recognize distinct engine knock, belt squeal, or exhaust sounds.
3. **Multi-Language Support:** Localizing symptom input and guidance into regional languages.
4. **Nearby Workshop Locator:** Integrating OpenStreetMap / Google Maps API to locate verified mechanics nearby.

---

## 🛡️ Academic Disclaimer

This project is created strictly as a 1-credit academic mini project demonstration. It offers preliminary troubleshooting advice and should not replace formal vehicle inspection by certified mechanics.
