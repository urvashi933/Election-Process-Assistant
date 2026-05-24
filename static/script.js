// Configuration: Use relative paths so it works on any host (Vercel, Docker, Local)
const API_BASE = "/api";

// Initialize Lucide Icons
lucide.createIcons();

/**
 * Tab Switching Logic with Accessibility Support
 */
function switchTab(tabName) {
    // 1. Hide all sections
    document.querySelectorAll('.tab-content').forEach(t => {
        t.classList.remove('active');
        t.style.display = 'none';
        t.setAttribute('aria-hidden', 'true');
    });
    
    // 2. Deactivate all buttons
    document.querySelectorAll('.nav-item').forEach(n => {
        n.classList.remove('active');
        n.removeAttribute('aria-current');
    });
    
    // 3. Activate target section
    const targetTab = document.getElementById(`${tabName}-tab`);
    if (targetTab) {
        targetTab.classList.add('active');
        targetTab.style.display = 'flex';
        targetTab.setAttribute('aria-hidden', 'false');
    }
    
    // 4. Activate clicked button
    const activeBtn = document.querySelector(`button[onclick*="'${tabName}'"]`);
    if (activeBtn) {
        activeBtn.classList.add('active');
        activeBtn.setAttribute('aria-current', 'page');
    }

    // 5. Special load triggers
    if (tabName === 'timeline') loadTimeline();
    
    // 6. Refresh icons
    lucide.createIcons();
}

/**
 * Chat Functionality with Loading States
 */
const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const chatForm = document.getElementById('chat-form');

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text || sendBtn.disabled) return;

    // Toggle loading state
    sendBtn.disabled = true;
    sendBtn.innerHTML = '<i data-lucide="loader" class="spin"></i>';
    lucide.createIcons();

    // Append User Message
    appendMessage(text, 'user');
    userInput.value = '';

    try {
        const response = await fetch(`${API_BASE}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text, session_id: "user_123" })
        });
        
        const result = await response.json();
        
        if (result.success) {
            appendMessage(result.data.response, 'ai');
        } else {
            appendMessage("I'm sorry, I couldn't process that. " + (result.error || ""), 'ai');
        }
    } catch (error) {
        console.error("Chat error:", error);
        appendMessage("Namaste! I'm having trouble connecting to my knowledge base.", 'ai');
    } finally {
        sendBtn.disabled = false;
        sendBtn.innerHTML = '<i data-lucide="send"></i>';
        lucide.createIcons();
        userInput.focus();
    }
}

function appendMessage(text, sender) {
    const div = document.createElement('div');
    div.className = `message ${sender}`;
    div.setAttribute('role', 'article');
    
    // Convert newlines and simple markdown-like bolding for the UI
    let formattedText = text.replace(/\n/g, '<br>');
    formattedText = formattedText.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    div.innerHTML = formattedText;
    chatBox.appendChild(div);
    
    // Smooth scroll to bottom
    chatBox.scrollTo({
        top: chatBox.scrollHeight,
        behavior: 'smooth'
    });
}

/**
 * Timeline Loader with Professional Cards
 */
async function loadTimeline() {
    const container = document.getElementById('timeline-list');
    container.innerHTML = '<div class="loading">Fetching official ECI timeline...</div>';
    
    try {
        const response = await fetch(`${API_BASE}/timeline`);
        const result = await response.json();
        
        if (result.success && result.data) {
            container.innerHTML = result.data.map(item => `
                <div class="timeline-card" role="listitem">
                    <div class="timeline-date">${item.date || 'Upcoming'}</div>
                    <h3>${item.event}</h3>
                    <p>${item.description}</p>
                </div>
            `).join('');
        }
    } catch (error) {
        container.innerHTML = '<div class="error">Failed to load timeline data.</div>';
    }
}

// Event Listeners
if (chatForm) {
    chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        sendMessage();
    });
}

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        e.preventDefault();
        sendMessage();
    }
});

// Initialize first tab
document.addEventListener('DOMContentLoaded', () => {
    switchTab('chat');
});
