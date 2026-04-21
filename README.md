# 🇮🇳 Election Guide AI
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-009688?logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker)

### 🧠 AI-Powered Assistant for the Indian Election Process

**Election Guide AI** is an interactive, intelligent assistant built to simplify the complexities of the Indian electoral system. Designed for first-time voters and civic-minded citizens, it provides real-time guidance on registration, timelines, and voting procedures.

---

## 🚀 Key Features

### 💬 Conversational "Chunav Guide"
* **Persona-Driven AI:** Powered by Google Gemini with a helpful "Hinglish"-aware persona.
* **Intelligent Intent Detection:** Automatically routes queries like *"How do I register?"* or *"Where is my booth?"* to the correct data module.

### 🧭 Structured Guidance
* **Step-by-Step Flows:** Detailed instructions for Voter Registration (Form 6) and EVM/VVPAT voting processes.
* **ID Requirements:** Instant access to the list of 12+ ECI-approved identification documents.

### 🛡️ Reliable Fallback System
* **100% Uptime:** Even if the Gemini API is unavailable or unconfigured, the system seamlessly switches to a local knowledge base to provide accurate ECI information.

### 📅 Timeline Explorer
* **Phased Tracking:** Visualize the election journey from Roll Revision to Counting Day.

---

## 🏗️ Tech Stack

| Layer      | Technology                       |
| ---------- | -------------------------------- |
| **Backend** | FastAPI (Python 3.11)            |
| **AI/LLM** | Google Gemini 1.5 Flash          |
| **Architecture** | Modular Service-Oriented         |
| **Container** | Docker (Non-root security)       |
| **Cloud** | Vercel (Serverless ready)        |

---

## 📂 Project Structure

```bash
app/
├── data/              # 🗄️ Local ECI Knowledge Base (JSON)
├── routes/            # 🌐 API Endpoints (Chat, Steps, Timeline)
├── services/          # ⚙️ Core Logic (Gemini, Intent, Step providers)
├── models.py          # 📝 Pydantic Data Schemas
└── main.py            # 🚀 FastAPI Entry Point