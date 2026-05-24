# 🇮🇳 Election Guide AI: Enterprise-Grade Civic Assistant
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-009688?logo=fastapi)
![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Integrated-4285F4?logo=google-cloud)
![Accessibility](https://img.shields.io/badge/Accessibility-WCAG%202.1-orange)
![Responsive](https://img.shields.io/badge/Responsive-All%20Devices-purple)

**Election Guide AI** is a state-of-the-art interactive assistant designed to simplify the Indian electoral system. Built for the PromptWars Challenge, it combines the power of **Google Gemini 1.5 Flash** with enterprise security, accessibility, and high-availability patterns. 

It features a stunning, premium **Single-Page Application (SPA) Web Dashboard** designed with modern glassmorphic aesthetics that brings high-end, responsive full-stack features to civic education.

---

## 🌟 Key Features

### 💎 State-of-the-Art Interactive UI (MERN-Stack Quality)
*   **Vibrant Glassmorphic Aesthetics:** Elegant dark-theme dashboard with a curated HSL color palette drawing inspiration from the Indian tricolor (saffron, emerald green, and tech-cyan gradients) with glowing active states and custom transitions.
*   **Horizontal Suggestion Chips:** Horizontal scrollable capsule list containing highly relevant ECI queries. Users can click any chip to instantly fill the input box and fire the AI prompt with springy tap animations.
*   **Safe AI Rich-Text Rendering:** Safe markdown-to-HTML parser using `marked.js` and `purify.js` CDNs, securely displaying headers, bold texts, lists, and hyperlinks while avoiding XSS vulnerabilities.
*   **Web Speech Synthesis (Text-to-Speech):** Fully integrated native TTS read-aloud controls on AI responses, helping visually impaired citizens listen to guidelines with play/stop toggle capability.

### 🗳️ Dynamic Step Checklists (State Persistence)
*   **Interactive Task Lists:** Dynamically fetches ECI voter instructions (e.g., Form 6 online registration, EVM/VVPAT voting compartment steps) and renders them as checklist cards.
*   **Progress Tracking:** Citizens can check off steps as they complete them (e.g., "Upload photograph and age proof", "Verify name on Electoral Roll").
*   **`localStorage` Synchronization:** Checkbox state is stored locally inside the browser. Progress is preserved across page refreshes and server updates, animating completion percentages on click.

### 📍 Glowing Chronological Timeline
*   **Vertical Connected Track:** Sleek timeline representing the official ECI schedule (Revision, Announcement, Nominations, Campaigns, Polling, Counting).
*   **Visual State Anchors:** Pulsing, glowing phase indicators utilizing distinct Lucide icons for each phase to make schedules easy to scan.

### 🏆 Gamified Democracy Trivia Quiz
*   **Interactive Challenge:** Engaging 5-question trivia module testing citizens' election knowledge.
*   **Real-time Visual Feedback:** Visual buttons highlighting correct choices in emerald green and incorrect selections in crimson red with elastic shake animations.
*   **Civic Explanations:** Explains the history or constitutional details behind every single question (e.g., the 61st Constitutional Amendment of 1988).
*   **Lightweight Celebration Confetti:** Triggers local, animated CSS confetti explosions on scoring a perfect 5/5, presenting an ECI Scholar badge.

---

## 🏗️ Technical Stack

| Layer | Technology | Key Features |
| :--- | :--- | :--- |
| **Frontend Frame** | HTML5, JavaScript (ES6+), Jinja2 | Accessible SPA, DOMPurify, Marked.js |
| **Styling & CSS** | Vanilla CSS (Flexbox, Grid, Variables) | Glassmorphic cards, HSL Tricolor gradient, keyframe micro-animations |
| **Backend** | FastAPI (Python 3.11) | High-speed async routes, compressed GZip payloads, CORS rules |
| **AI Engine** | Google Gemini 1.5 Flash | Conversational Hinglish, context grounding, safety guardrails |
| **Observability** | **Google Cloud Logging** | Real-time backend tracing, logs sync |
| **Cache & Security** | TTLCache (Memory), Bleach | 10-min memory caching, multi-layer XSS sanitization |

---

## 📂 Project Structure

```bash
app/
├── data/              # 🗄️ Grounding data for AI (election_knowledge.json)
├── routes/            # 🌐 Hardened API Endpoints (chat.py, steps.py, timeline.py)
├── services/          # ⚙️ Business Logic (assistant_service.py, gemini_service.py)
├── templates/         # ♿ index.html - Rich HTML5 template with Speech synthesis
├── utils/             # 🛡️ Validators & Sanitizers
├── models.py          # 📝 Strict Pydantic Schemas
└── main.py            # 🚀 Entry point with GZip compression and security headers
static/
├── script.js          # 🧠 Client Engine, Local Checklists, TTS & Quiz Logic
└── style.css          # 🎨 Premium HSL Glassmorphism, Timelines & Animations
```

---

## 🛠️ Getting Started

1.  **Clone the Repository**
2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure API Keys:**
    Create a local `.env` file in the root directory:
    ```env
    GOOGLE_API_KEY=your_gemini_api_key_here
    GEMINI_MODEL=gemini-2.0-flash
    ENV=development
    LOG_LEVEL=INFO
    ```
4.  **Launch the Server:**
    ```bash
    uvicorn app.main:app --reload
    ```
5.  **Access the Dashboard:**
    Open `http://localhost:8000` in your web browser.
6.  **Run Tests:**
    ```bash
    pytest
    ```