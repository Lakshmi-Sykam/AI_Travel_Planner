# ✈️ AI Travel Planning Agent

An autonomous Multi-Agent AI system designed to understand natural language travel requests and generate end-to-end travel plans with logistics, accommodation, curated day-by-day itineraries, and smart budget balancing.

---

## 🏗️ Architecture

```text
               User Input (Streamlit UI)
                         │
                         ▼
             FastAPI Backend API Router
                         │
                         ▼
               LangGraph Orchestrator
                         │
      ┌──────────────────┼──────────────────┐
      ▼                  ▼                  ▼
 [Travel Agent]     [Hotel Agent]    [Activity Agent]
  - Transport        - Hotels         - Attractions
  - Routes & Timing  - Budget tier    - Food & Dining
      │                  │                  │
      └──────────────────┼──────────────────┘
                         │
                         ▼
             [Synthesizer & Budget Node]
            - Unified Day-by-Day Plan
            - Budget Breakdown & Validation
                         │
                         ▼
             SQLite DB (Saved Trips)
                         │
                         ▼
         Rendered in Streamlit Frontend
       (Interactive Timeline, Cost Charts, PDF/MD Export)
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit, Plotly, Custom CSS |
| **Backend** | FastAPI, Uvicorn, Pydantic v2 |
| **Orchestration** | LangGraph, LangChain |
| **LLM Inference** | Groq API (`llama-3.3-70b-versatile`) + Fallback Mode |
| **Database** | SQLite + SQLAlchemy |
| **Exports** | PDF (ReportLab), Markdown, JSON |

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Python 3.10+ installed

### 2. Environment Setup
Clone the repository and install dependencies:

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.\.venv\Scripts\activate
# Linux/macOS:
# source .venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 3. Configure API Key
Copy `.env.example` to `.env` and insert your free Groq API key:
```ini
GROQ_API_KEY=gsk_your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```
*(Note: If no API key is provided, the application automatically runs in Smart Fallback Mode so all features continue to function.)*

---

## 🏃 Running the Application

### Step 1: Start FastAPI Backend
```bash
.\.venv\Scripts\python -m uvicorn backend.app.main:app --reload --port 8000
```
Backend Swagger Documentation will be available at: `http://127.0.0.1:8000/docs`

### Step 2: Start Streamlit Frontend (In a separate terminal)
```bash
.\.venv\Scripts\streamlit run frontend/app.py
```
Open your browser at: `http://localhost:8501`

---

## 🧪 Testing the Workflow

You can test planning a trip with an example query:
- **Origin:** Mumbai
- **Destination:** Goa
- **Duration:** 4 Days
- **Budget:** ₹20,000
- **Style:** Budget / Backpacker
- **Interests:** Beaches, Local Food, Heritage

---
*Created with ❤️ for intelligent, autonomous travel planning.*
