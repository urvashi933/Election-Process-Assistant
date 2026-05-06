# 🇮🇳 Election Guide AI: Enterprise-Grade Civic Assistant
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-009688?logo=fastapi)
![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Integrated-4285F4?logo=google-cloud)
![Accessibility](https://img.shields.io/badge/Accessibility-WCAG%202.1-orange)

**Election Guide AI** is a state-of-the-art interactive assistant designed to simplify the Indian electoral system. Built for the PromptWars Challenge, it combines the power of **Google Gemini 1.5 Flash** with enterprise security, accessibility, and high-availability patterns.

---

## 🌟 Key Features

### 💎 Premium AI Interaction
*   **Chunav Guide Persona:** A sophisticated "Hinglish"-aware AI that explains complex ECI rules in simple, conversational language.
*   **Async Content Generation:** Optimized for speed using asynchronous Gemini API calls.
*   **Safety First:** Integrated Google AI Safety filters to ensure neutral, unbiased, and safe civic education.

### ♿ Accessibility & Inclusion (WCAG 2.1)
*   **Screen Reader Ready:** Fully semantic HTML5 structure with ARIA landmarks and labels.
*   **High Contrast UI:** Modern glassmorphism design with a carefully curated "Indian Flag" inspired palette that meets WCAG 2.1 contrast standards.
*   **Keyboard Navigable:** Complete keyboard support for all interactive elements.

### 🛡️ Enterprise Security & Reliability
*   **XSS & Injection Protection:** Multi-layer sanitization using `bleach` and custom regex patterns to block prompt injection and malicious scripts.
*   **Security Headers:** Hardened FastAPI middleware with HSTS, X-Frame-Options, and Content-Type sniffing prevention.
*   **100% Uptime Architecture:** A robust local RAG (Retrieval-Augmented Generation) fallback ensures accurate answers even during API outages.

### ⚡ Performance Optimized
*   **Intelligent Caching:** Response caching using `TTLCache` to reduce API latency and costs.
*   **Payload Compression:** GZip middleware enabled for lightning-fast UI responses.

---

## 🏗️ Advanced Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Backend** | FastAPI (Python 3.11) |
| **AI Engine** | Google Gemini 1.5 Flash (via `google-generativeai`) |
| **Observability** | **Google Cloud Logging** (Integrated) |
| **Storage** | **Google Cloud Storage** (Metadata Ready) |
| **Security** | Bleach, Pydantic v2, Security Headers |
| **Testing** | Pytest, Pytest-Asyncio (High Coverage) |

---

## 📂 Project Structure

```bash
app/
├── data/              # 🗄️ Grounding data for AI (ECI Knowledge)
├── routes/            # 🌐 Hardened API Endpoints
├── services/          # ⚙️ Business Logic (Gemini, Intent, Caching)
├── templates/         # ♿ Accessible HTML5 Templates
├── utils/             # 🛡️ Validators & Sanitizers
├── models.py          # 📝 Strict Pydantic Schemas
└── main.py            # 🚀 Entry point with Security Middleware
```

## 🛠️ Getting Started

1.  **Clone the Repo**
2.  **Install Deps:** `pip install -r requirements.txt`
3.  **Set Env:** Create a `.env` with `GOOGLE_API_KEY`
4.  **Run:** `uvicorn app.main:app --reload`
5.  **Test:** `pytest`