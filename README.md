![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-009688?logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker)
![Tests](https://img.shields.io/badge/Tests-Pytest-green?logo=pytest)
![License](https://img.shields.io/badge/License-MIT-yellow)

# 🇮🇳 Election Guide AI

### 🧠 AI-Powered Assistant for Understanding the Indian Election Process

An interactive, intelligent assistant that helps users **understand voter registration, election timelines, voting steps, and requirements in India** — in a simple, conversational way.

Built for clarity, accessibility, and real-world usability.

---

## 🚀 Features

### 💬 Conversational AI Assistant

* Ask questions like:

  * *“How do I register to vote in India?”*
  * *“What documents are required?”*
  * *“When are elections happening?”*
* Powered by Gemini (with smart fallback system)

---

### 🧭 Step-by-Step Guidance

* Clear instructions for:

  * Voter Registration
  * Voting Process
  * Required Documents
* Designed for **first-time voters**

---

### 📅 Election Timeline Explorer

* View key election phases:

  * Notification
  * Nomination
  * Polling
  * Counting
* Dynamic timeline support

---

### 🧠 Smart Intent Detection

* Automatically understands user queries:

  * `registration`
  * `timeline`
  * `voting`
  * `documents`
  * `polling`
  * `results`

---

### 🎨 Modern UI/UX

* Glassmorphism design
* Smooth animations
* Interactive suggestions
* Responsive layout

---

### 🛡️ Reliable Fallback System

* Works even without API key
* Template-based responses ensure **100% uptime**

---

## 🏗️ Tech Stack

| Layer      | Technology                       |
| ---------- | -------------------------------- |
| Backend    | FastAPI                          |
| AI/LLM     | Google Gemini                    |
| Frontend   | HTML, CSS (Glass UI), JavaScript |
| Testing    | Pytest                           |
| Deployment | Docker                           |
| Config     | Python-dotenv                    |

---

## 📂 Project Structure

```bash
app/
│── routes/            # API endpoints
│── services/          # Core logic (AI, timeline, steps)
│── models/            # Pydantic schemas
│── templates/         # HTML frontend
│── static/            # CSS + JS
│── utils/             # Helpers & validation
│── config.py          # Environment config
│── main.py            # Entry point

tests/
│── test_chat.py
│── test_timeline.py
│── test_intent.py

Dockerfile
requirements.txt
.env
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/election-guide-ai.git
cd election-guide-ai
```

---

### 2️⃣ Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

---

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Configure environment

Create a `.env` file:

```env
GOOGLE_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-1.5-pro

ELECTION_COUNTRY=India
ELECTION_TYPE=lok_sabha

ENV=development
```

---

### 5️⃣ Run the app

```bash
uvicorn app.main:app --reload
```

Visit:
👉 http://localhost:8000

---

## 🐳 Run with Docker

```bash
docker build -t election-ai .
docker run -p 8080:8080 election-ai
```

---

## 🧪 Running Tests

```bash
pytest
```

---

## 🧠 How It Works

1. User sends a query
2. Intent is classified (AI or keyword fallback)
3. Relevant context is fetched
4. Response generated via:

   * Gemini API (if available)
   * Template fallback (if not)
5. Suggestions + sources returned

---

## 🎯 Use Cases

* 🧑‍🎓 First-time voters
* 🏫 Educational institutions
* 🧑‍💼 Civic awareness platforms
* 🗳️ Election awareness campaigns

---

## 🔐 Security & Best Practices

* `.env` is ignored via `.gitignore`
* API keys are never exposed
* Runs as non-root user in Docker
* Input validation implemented

---

## 🌟 Future Enhancements

* 📍 Location-based polling booth finder
* 🧾 Real-time voter ID verification
* 📊 Election results dashboard
* 🎮 Quiz mode for civic education
* 🌐 Multi-language support (Hindi + regional)

---

## 🤝 Contributing

Pull requests are welcome!
For major changes, please open an issue first.

---

## 📜 License

MIT License

---

## 💡 Inspiration

Making civic processes **simple, transparent, and accessible** through AI.

---

## 👨‍💻 Author

Built with precision and intent for **PromptWars Challenge** 🚀

---

## ⭐ Show your support

If you found this useful:
👉 Star the repo
👉 Share with others
👉 Contribute ideas

---
