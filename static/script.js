const API_URL = "https://your-vercel-app.vercel.app/api"; // Replace with your actual Vercel URL

// Initialize Lucide Icons
lucide.createIcons();

// Tab Switching Logic
function switchTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    
    document.getElementById(`${tabName}-tab`).classList.add('active');
    event.currentTarget.classList.add('active');

    if (tabName === 'timeline') loadTimeline();
}

// Chat Functionality
const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    // Append User Message
    appendMessage(text, 'user');
    userInput.value = '';

    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        });
        
        const result = await response.json();
        appendMessage(result.data.response, 'ai');
    } catch (error) {
        appendMessage("Connection error. Check if backend is running!", 'ai');
    }
}

function appendMessage(text, sender) {
    const div = document.createElement('div');
    div.className = `message ${sender}`;
    div.innerHTML = text.replace(/\n/g, '<br>');
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Load Timeline from API
async function loadTimeline() {
    const container = document.getElementById('timeline-list');
    container.innerHTML = "Loading timeline...";
    
    try {
        const response = await fetch(`${API_URL}/timeline`);
        const result = await response.json();
        
        container.innerHTML = result.data.map(item => `
            <div class="timeline-item">
                <h3>${item.event}</h3>
                <p>${item.description}</p>
            </div>
        `).join('');
    } catch (error) {
        container.innerHTML = "Failed to load timeline.";
    }
}

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => { if(e.key === 'Enter') sendMessage(); });