// -----------------------------
// 🧠 SESSION + STATE
// -----------------------------
const sessionId = "sess_" + Date.now();
let currentMode = "guide";

// DOM
const chatBox = document.getElementById("chat-messages");
const inputBox = document.getElementById("user-input");
const sendBtn = document.querySelector("button[onclick='sendMessage()']");
const suggestionsContainer = document.getElementById("suggestions-container");
const sourcesContainer = document.getElementById("sources-container");
const sourcesList = document.getElementById("sources-list");


// -----------------------------
// 💬 MESSAGE RENDERING
// -----------------------------
function addMessage(text, role) {
    const wrapper = document.createElement("div");
    wrapper.className = `message ${role}`;

    const content = document.createElement("div");
    content.className = "message-content";

    content.innerHTML = text
        .replace(/\*\*(.*?)\*\*/g, "<b>$1</b>")
        .replace(/\n/g, "<br>");

    wrapper.appendChild(content);
    chatBox.appendChild(wrapper);
    chatBox.scrollTop = chatBox.scrollHeight;
}


// -----------------------------
// ⏳ TYPING INDICATOR
// -----------------------------
function showTyping() {
    const div = document.createElement("div");
    div.className = "message assistant";
    div.id = "typing";

    div.innerHTML = `<div class="typing-indicator">
        <span></span><span></span><span></span>
    </div>`;

    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function hideTyping() {
    const el = document.getElementById("typing");
    if (el) el.remove();
}


// -----------------------------
// 🧭 MODE SWITCHING
// -----------------------------
function setMode(mode) {
    currentMode = mode;
    addMessage(`🔄 Switched to **${mode} mode**`, "assistant");
}


// -----------------------------
// 💡 SUGGESTIONS
// -----------------------------
function updateSuggestions(list = []) {
    suggestionsContainer.innerHTML = "";

    list.forEach(item => {
        const btn = document.createElement("button");
        btn.className = "suggestion-btn";
        btn.innerText = item;
        btn.onclick = () => sendQuick(item);
        suggestionsContainer.appendChild(btn);
    });
}

function sendQuick(text) {
    inputBox.value = text;
    sendMessage();
}


// -----------------------------
// 📚 SOURCES
// -----------------------------
function updateSources(sources = []) {
    if (!sources.length) {
        sourcesContainer.style.display = "none";
        return;
    }

    sourcesContainer.style.display = "block";
    sourcesList.innerHTML = "";

    sources.forEach(src => {
        const li = document.createElement("li");
        li.textContent = src;
        sourcesList.appendChild(li);
    });
}


// -----------------------------
// 📊 RENDER STRUCTURED DATA
// -----------------------------
function renderData(data) {
    if (!data) return;

    const container = document.createElement("div");
    container.className = "data-card";

    // Timeline
    if (Array.isArray(data)) {
        data.forEach(item => {
            const el = document.createElement("div");
            el.className = "timeline-item";
            el.innerHTML = `<b>${item.event || ""}</b><br>${item.description || ""}`;
            container.appendChild(el);
        });
    }

    // Step guide
    else if (data.actions) {
        const title = document.createElement("h4");
        title.innerText = data.title;
        container.appendChild(title);

        data.actions.forEach(step => {
            const li = document.createElement("div");
            li.innerText = "👉 " + step;
            container.appendChild(li);
        });
    }

    chatBox.appendChild(container);
}


// -----------------------------
// ⌨️ INPUT HANDLING
// -----------------------------
function handleKeyPress(e) {
    if (e.key === "Enter") sendMessage();
}


// -----------------------------
// 🚀 MAIN SEND FUNCTION
// -----------------------------
async function sendMessage() {
    const text = inputBox.value.trim();
    if (!text) return;

    addMessage(text, "user");
    inputBox.value = "";

    inputBox.disabled = true;
    sendBtn.disabled = true;

    showTyping();

    try {
        const res = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                message: text,
                session_id: sessionId,
                mode: currentMode
            })
        });

        if (!res.ok) throw new Error("API error");

        const data = await res.json();

        hideTyping();

        // 💬 Response
        addMessage(data.response, "assistant");

        // 📊 Structured UI
        renderData(data.data);

        // 💡 Suggestions
        updateSuggestions(data.follow_up_suggestions);

        // 📚 Sources
        updateSources(data.sources);

    } catch (err) {
        console.error(err);
        hideTyping();
        addMessage("⚠️ Something went wrong. Please try again.", "assistant");
    } finally {
        inputBox.disabled = false;
        sendBtn.disabled = false;
        inputBox.focus();
    }
}