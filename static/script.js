// ==========================================================================
// ⚙️ CHUNAV GUIDE AI: JAVASCRIPT ENGINE WITH RICH INTERACTION
// ==========================================================================

const API_BASE = "/api";

// Initialize Lucide Icons on start
lucide.createIcons();

// Custom suggestion questions list
const suggestions = [
    { text: "🗳️ Register as new voter", query: "How to register as a new voter and fill Form 6?" },
    { text: "📝 Correct Voter Card details", query: "How to correct entries or shift residence using Form 8?" },
    { text: "📍 Locate polling booth", query: "How do I locate my assigned polling booth?" },
    { text: "🤖 EVM & VVPAT guidance", query: "Explain how EVM and VVPAT work together on voting day." },
    { text: "🆔 Alternative ID documents", query: "What valid documents can I bring to vote if I don't have my Voter ID card?" }
];

/**
 * Tab Switching Logic with Dynamic Component Loading
 */
function switchTab(tabName) {
    // 1. Hide all sections
    document.querySelectorAll('.tab-content').forEach(t => {
        t.classList.remove('active');
        t.style.display = 'none';
        t.setAttribute('aria-hidden', 'true');
    });
    
    // 2. Deactivate all navigation items
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
    
    // 4. Activate current navigation button
    const activeBtn = document.querySelector(`button[onclick*="'${tabName}'"]`);
    if (activeBtn) {
        activeBtn.classList.add('active');
        activeBtn.setAttribute('aria-current', 'page');
    }

    // 5. Title & Header context shift for immersive experience
    const mainTitle = document.getElementById('main-title');
    if (mainTitle) {
        const titleMap = {
            'chat': 'Indian Election AI Guide',
            'timeline': 'ECI Official Election Timeline',
            'guide': 'Interactive Voter Checklists',
            'quiz': 'Chunav Democracy Quiz'
        };
        mainTitle.innerText = titleMap[tabName] || 'Indian Election Guide';
    }
    
    // 6. Special load triggers
    if (tabName === 'timeline') loadTimeline();
    if (tabName === 'guide') loadGuides();
    if (tabName === 'quiz') loadQuiz();
    
    // 7. Refresh Lucide Icons
    lucide.createIcons();
}

/* ==========================================================================
   💬 CHAT FUNCTIONALITY & SECURE RICH RENDERING
   ========================================================================== */
const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const chatForm = document.getElementById('chat-form');

// Text-to-speech current voice reference
let currentSpeechUtterance = null;
let currentSpeechBtn = null;

/**
 * Visual Markdown and HTML Sanitization Engine
 */
function renderMarkdown(text) {
    if (typeof marked !== 'undefined' && typeof DOMPurify !== 'undefined') {
        try {
            // Marked parser configured with default secure settings
            const rawHtml = marked.parse(text);
            return DOMPurify.sanitize(rawHtml);
        } catch (e) {
            console.warn("Markdown rendering failed, falling back:", e);
        }
    }
    
    // Hardened client-side fallback formatting regex
    let formatted = text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/\n/g, '<br>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/### (.*?)(?:<br>|$)/g, '<h3>$1</h3>')
        .replace(/## (.*?)(?:<br>|$)/g, '<h2>$1</h2>');
    return formatted;
}

/**
 * native Speech Synthesis Controller (TTS)
 */
function speakResponse(text, btnId) {
    const btn = document.getElementById(btnId);
    if (!btn) return;
    
    // Toggle Speech Stop
    if (window.speechSynthesis.speaking) {
        window.speechSynthesis.cancel();
        if (currentSpeechBtn) {
            currentSpeechBtn.innerHTML = '<i data-lucide="volume-2"></i>';
            currentSpeechBtn.title = "Read aloud";
        }
        
        // If we clicked the same speaker that was reading, stop here
        if (currentSpeechBtn === btn) {
            currentSpeechBtn = null;
            lucide.createIcons();
            return;
        }
    }
    
    // Remove markdown indicators so the reader talks naturally
    const naturalText = text
        .replace(/\*\*|\*|###|#|`/g, '')
        .replace(/Form 6/gi, 'Form Six')
        .replace(/Form 8/gi, 'Form Eight')
        .replace(/ECI/gi, 'E C I')
        .replace(/EPIC/gi, 'Epic');

    const utterance = new SpeechSynthesisUtterance(naturalText);
    utterance.lang = 'hi-IN'; // Settle on English/Hindi Indian localization if available
    utterance.rate = 1.05;
    
    utterance.onend = () => {
        btn.innerHTML = '<i data-lucide="volume-2"></i>';
        lucide.createIcons();
        currentSpeechBtn = null;
    };
    
    utterance.onerror = () => {
        btn.innerHTML = '<i data-lucide="volume-2"></i>';
        lucide.createIcons();
        currentSpeechBtn = null;
    };
    
    currentSpeechBtn = btn;
    btn.innerHTML = '<i data-lucide="square" class="stop-icon"></i>';
    lucide.createIcons();
    window.speechSynthesis.speak(utterance);
}

/**
 * Copy to Clipboard Helper with UI Alert Feedback
 */
function copyResponse(text, btnId) {
    const btn = document.getElementById(btnId);
    if (!btn) return;
    
    // Clean markdown helper
    navigator.clipboard.writeText(text).then(() => {
        const originalContent = btn.innerHTML;
        btn.innerHTML = '<i data-lucide="check" style="color:var(--green)"></i> Copied!';
        lucide.createIcons();
        
        setTimeout(() => {
            btn.innerHTML = originalContent;
            lucide.createIcons();
        }, 2200);
    }).catch(err => {
        console.error("Clipboard copy failed: ", err);
    });
}

/**
 * Dispatches query from chat box
 */
async function sendMessage() {
    const text = userInput.value.trim();
    if (!text || sendBtn.disabled) return;

    // Trigger loader state
    sendBtn.disabled = true;
    sendBtn.innerHTML = '<i data-lucide="loader" class="spin"></i>';
    lucide.createIcons();

    // Render User Message card
    appendMessage(text, 'user');
    userInput.value = '';

    // Render skeleton/thinking bubble
    const thinkingId = `ai-think-${Date.now()}`;
    const skeletonDiv = document.createElement('div');
    skeletonDiv.className = 'message ai thinking-bubble';
    skeletonDiv.id = thinkingId;
    skeletonDiv.innerHTML = `
        <div class="loading" style="padding:0; font-size:0.85rem;">
            <span>Chunav Guide is gathering ECI information...</span>
        </div>
    `;
    chatBox.appendChild(skeletonDiv);
    chatBox.scrollTo({ top: chatBox.scrollHeight, behavior: 'smooth' });

    try {
        const response = await fetch(`${API_BASE}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text, session_id: "chunav_assistant_urvashi" })
        });
        
        const result = await response.json();
        
        // Remove the skeleton loading bubble
        const bubble = document.getElementById(thinkingId);
        if (bubble) bubble.remove();

        if (result.success && result.data) {
            appendMessage(result.data.response, 'ai');
            
            // Proactively load checklists if the AI detects an actionable intent
            if (result.data.intent === 'registration' || result.data.intent === 'voting') {
                setTimeout(() => {
                    // Let user know they can track these in the guide tab
                    const toast = document.createElement('div');
                    toast.className = 'chip';
                    toast.style.position = 'absolute';
                    toast.style.bottom = '110px';
                    toast.style.left = '50%';
                    toast.style.transform = 'translateX(-50%)';
                    toast.style.border = '1px solid var(--cyan)';
                    toast.style.boxShadow = '0 0 10px var(--cyan-glow)';
                    toast.innerHTML = `<i data-lucide="check-circle" style="color:var(--cyan)"></i> Tracking checklist unlocked under 'Step Guide'!`;
                    document.getElementById('chat-tab').appendChild(toast);
                    lucide.createIcons();
                    setTimeout(() => toast.remove(), 4000);
                }, 1000);
            }
        } else {
            appendMessage("Namaste! I hit a block while checking my ECI guidelines. " + (result.error || ""), 'ai');
        }
    } catch (error) {
        console.error("Chat error:", error);
        // Remove the skeleton loading bubble
        const bubble = document.getElementById(thinkingId);
        if (bubble) bubble.remove();
        
        appendMessage("Namaste! I'm currently having issues connecting to my local offline database. Please make sure uvicorn is running correctly.", 'ai');
    } finally {
        sendBtn.disabled = false;
        sendBtn.innerHTML = '<i data-lucide="send"></i>';
        lucide.createIcons();
        userInput.focus();
    }
}

/**
 * Appends standard message card
 */
function appendMessage(text, sender) {
    const div = document.createElement('div');
    div.className = `message ${sender}`;
    div.setAttribute('role', 'article');
    
    if (sender === 'ai') {
        const msgId = `ai-msg-${Date.now()}`;
        const cleanTextForSpeech = text.replace(/"/g, '&quot;');
        
        div.innerHTML = `
            <div class="message-text">${renderMarkdown(text)}</div>
            <div class="message-actions">
                <button class="msg-btn" id="copy-${msgId}" onclick="copyResponse(\`${cleanTextForSpeech}\`, 'copy-${msgId}')" title="Copy to clipboard">
                    <i data-lucide="copy"></i> Copy
                </button>
                <button class="msg-btn" id="speak-${msgId}" onclick="speakResponse(\`${cleanTextForSpeech}\`, 'speak-${msgId}')" title="Read Aloud">
                    <i data-lucide="volume-2"></i> Listen
                </button>
            </div>
        `;
    } else {
        // Safe user input escaping
        const escapedDiv = document.createElement('div');
        escapedDiv.className = 'message-text';
        escapedDiv.innerText = text;
        div.appendChild(escapedDiv);
    }
    
    chatBox.appendChild(div);
    
    // Smooth scroll down
    chatBox.scrollTo({
        top: chatBox.scrollHeight,
        behavior: 'smooth'
    });
    
    lucide.createIcons();
}

/**
 * Suggestion Chips Loading Panel
 */
function loadSuggestions() {
    const chipContainer = document.getElementById('suggestion-chips');
    if (!chipContainer) return;
    
    chipContainer.innerHTML = suggestions.map((s, index) => `
        <button class="chip" onclick="clickSuggestion(${index})" aria-label="Ask suggestion: ${s.text}">
            ${s.text}
        </button>
    `).join('');
}

function clickSuggestion(index) {
    const target = suggestions[index];
    if (!target) return;
    
    userInput.value = target.query;
    sendMessage();
}

/* ==========================================================================
   🗳️ STEP CHECKLISTS SYSTEM (localStorage Persistence)
   ========================================================================== */
async function loadGuides() {
    const container = document.getElementById('guide-list');
    if (!container) return;
    
    container.innerHTML = '<div class="loading">Fetching step-by-step ECI checklists...</div>';
    
    try {
        const response = await fetch(`${API_BASE}/steps`);
        const result = await response.json();
        
        if (result.success && result.data) {
            container.innerHTML = result.data.map(guide => {
                const savedChecked = JSON.parse(localStorage.getItem(`chunav_guide_${guide.step_id}`) || '[]');
                
                const actionItems = guide.actions.map((act, index) => {
                    const isChecked = savedChecked.includes(index);
                    const checkedAttr = isChecked ? 'checked' : '';
                    const itemClass = isChecked ? 'checklist-item checked' : 'checklist-item';
                    return `
                        <label class="${itemClass}" id="label-${guide.step_id}-${index}">
                            <input type="checkbox" ${checkedAttr} onchange="toggleCheck('${guide.step_id}', ${index}, ${guide.actions.length})" aria-label="Mark completed: ${act}">
                            <span>${act}</span>
                        </label>
                    `;
                }).join('');

                const resourceLinks = guide.resources.map(res => {
                    let name = res;
                    let url = "#";
                    if (res.includes("http")) {
                        const parts = res.split(": ");
                        name = parts[0];
                        url = parts.slice(1).join(": ");
                    }
                    return `<a href="${url}" target="_blank" class="resource-btn"><i data-lucide="external-link"></i> ${name}</a>`;
                }).join('');

                return `
                    <div class="guide-card" role="listitem">
                        <span class="estimated-badge"><i data-lucide="clock"></i> ${guide.estimated_time}</span>
                        <h3>${guide.title}</h3>
                        <p>${guide.description}</p>
                        
                        <div class="progress-section">
                            <div class="progress-header">
                                <span>Checklist Completion</span>
                                <span id="progress-text-${guide.step_id}">0% Complete</span>
                            </div>
                            <div class="progress-bar-track">
                                <div class="progress-bar-fill" id="progress-fill-${guide.step_id}"></div>
                            </div>
                        </div>
                        
                        <div class="checklist">
                            ${actionItems}
                        </div>
                        
                        <div class="resource-section">
                            <h4>Official Resources</h4>
                            <div class="resource-links">
                                ${resourceLinks}
                            </div>
                        </div>
                    </div>
                `;
            }).join('');
            
            // Fire initial progress calculators for each guide card
            result.data.forEach(guide => {
                updateProgress(guide.step_id, guide.actions.length);
            });
            
            lucide.createIcons();
        } else {
            container.innerHTML = '<div class="error">ECI steps couldn\'t load from data models.</div>';
        }
    } catch (error) {
        console.error(error);
        container.innerHTML = '<div class="error">Failed to synchronize guides with backend uvicorn server.</div>';
    }
}

function toggleCheck(stepId, index, total) {
    const label = document.getElementById(`label-${stepId}-${index}`);
    if (!label) return;
    const checkbox = label.querySelector('input[type="checkbox"]');
    const savedKey = `chunav_guide_${stepId}`;
    let savedChecked = JSON.parse(localStorage.getItem(savedKey) || '[]');
    
    if (checkbox.checked) {
        label.classList.add('checked');
        if (!savedChecked.includes(index)) {
            savedChecked.push(index);
        }
    } else {
        label.classList.remove('checked');
        savedChecked = savedChecked.filter(item => item !== index);
    }
    
    localStorage.setItem(savedKey, JSON.stringify(savedChecked));
    updateProgress(stepId, total);
}

function updateProgress(stepId, total) {
    const savedChecked = JSON.parse(localStorage.getItem(`chunav_guide_${stepId}`) || '[]');
    const count = savedChecked.length;
    const percent = total > 0 ? Math.round((count / total) * 100) : 0;
    
    const textEl = document.getElementById(`progress-text-${stepId}`);
    const fillEl = document.getElementById(`progress-fill-${stepId}`);
    
    if (textEl) textEl.innerText = `${percent}% Complete (${count}/${total})`;
    if (fillEl) fillEl.style.width = `${percent}%`;
}

/* ==========================================================================
   📍 ELECTIONS GLOWING TIMELINE COMPONENT
   ========================================================================== */
async function loadTimeline() {
    const container = document.getElementById('timeline-list');
    if (!container) return;
    container.innerHTML = '<div class="loading">Loading official ECI schedule...</div>';
    
    const timelineIcons = {
        "Electoral Roll Revision": "edit-3",
        "Election Notification": "megaphone",
        "Nomination Phase": "file-text",
        "Campaign Period": "users",
        "Polling Day": "check-square",
        "Counting Day": "award"
    };

    try {
        const response = await fetch(`${API_BASE}/timeline`);
        const result = await response.json();
        
        if (result.success && result.data) {
            container.innerHTML = result.data.map((item, index) => {
                const iconName = timelineIcons[item.event] || 'calendar';
                return `
                    <div class="timeline-card" role="listitem">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                            <span class="timeline-index">Phase ${index + 1}</span>
                        </div>
                        <h3><i data-lucide="${iconName}"></i> ${item.event}</h3>
                        <p>${item.description}</p>
                    </div>
                `;
            }).join('');
            lucide.createIcons();
        } else {
            container.innerHTML = '<div class="error">Failed to parse timeline details.</div>';
        }
    } catch (error) {
        container.innerHTML = '<div class="error">Timeline data unavailable. Verify Python service.</div>';
    }
}

/* ==========================================================================
   🗳️ GAMIFIED TRIVIA QUIZ (Democracy Challenge)
   ========================================================================== */
const quizQuestions = [
    {
        question: "What is the minimum voting age for an Indian citizen?",
        options: ["16 years", "18 years", "21 years", "25 years"],
        answer: 1, 
        explanation: "The minimum voting age was reduced from 21 to 18 years by the 61st Constitutional Amendment Act of 1988."
    },
    {
        question: "Which form is used for new voter registration in India?",
        options: ["Form 6", "Form 7", "Form 8", "Form 6A"],
        answer: 0, 
        explanation: "Form 6 is dedicated for the application of new voters to get their name included in the Electoral Roll."
    },
    {
        question: "What is the full form of VVPAT in ECI elections?",
        options: [
            "Voter Verified Paper Audit Trail",
            "Voter Verification Post Audit Transfer",
            "Voter Valued Paper Account Track",
            "Voter Visual Paper Action Tracker"
        ],
        answer: 0,
        explanation: "VVPAT stands for Voter Verified Paper Audit Trail. It allows voters to physically verify that their cast ballot went to the intended candidate."
    },
    {
        question: "How long is a printed VVPAT slip visible behind the glass window?",
        options: ["3 seconds", "5 seconds", "7 seconds", "10 seconds"],
        answer: 2,
        explanation: "The printed VVPAT slip is visible through a glass window for exactly 7 seconds before automatically dropping into the sealed ballot collection box."
    },
    {
        question: "Which official is responsible for updating the voter list at the polling booth level?",
        options: ["Returning Officer (RO)", "District Election Officer (DEO)", "Booth Level Officer (BLO)", "Chief Electoral Officer (CEO)"],
        answer: 2, 
        explanation: "The Booth Level Officer (BLO) is a local ECI representative who verifies local voter registries, handles Form submissions, and works closely with residents."
    }
];

let quizState = {
    currentQuestionIndex: 0,
    score: 0,
    answers: []
};

function loadQuiz() {
    const box = document.getElementById('quiz-box');
    if (!box) return;
    
    // Check if quiz is completed
    if (quizState.currentQuestionIndex >= quizQuestions.length) {
        renderQuizScore();
        return;
    }
    
    const q = quizQuestions[quizState.currentQuestionIndex];
    const optionsHTML = q.options.map((opt, idx) => `
        <button class="option-btn" onclick="selectQuizOption(${idx})" id="opt-${idx}">
            ${idx + 1}. &nbsp; ${opt}
        </button>
    `).join('');
    
    box.innerHTML = `
        <div class="quiz-header">
            <h2>🗳️ Chunav Quiz Challenge</h2>
            <p>Showcase your democratic awareness!</p>
        </div>
        <div class="quiz-question-box">
            <div class="question-meta">
                <span>Question ${quizState.currentQuestionIndex + 1} of ${quizQuestions.length}</span>
                <span style="color:var(--saffron)">Score: ${quizState.score}</span>
            </div>
            <div class="question-text">${q.question}</div>
        </div>
        <div class="quiz-options" id="quiz-options-container">
            ${optionsHTML}
        </div>
        <div id="quiz-feedback-box" style="margin-top:15px; z-index:1; display:none;">
            <!-- Triggered on click -->
        </div>
    `;
    lucide.createIcons();
}

function selectQuizOption(selectedIdx) {
    const q = quizQuestions[quizState.currentQuestionIndex];
    const container = document.getElementById('quiz-options-container');
    const feedbackBox = document.getElementById('quiz-feedback-box');
    
    if (!container || !feedbackBox) return;
    
    // Disable all options buttons to prevent multiple clicks
    container.querySelectorAll('.option-btn').forEach((btn, idx) => {
        btn.disabled = true;
        if (idx === q.answer) {
            btn.classList.add('correct');
        }
    });
    
    const chosenBtn = document.getElementById(`opt-${selectedIdx}`);
    let isCorrect = selectedIdx === q.answer;
    
    if (isCorrect) {
        quizState.score++;
    } else {
        if (chosenBtn) chosenBtn.classList.add('incorrect');
    }
    
    // Save selection
    quizState.answers.push(selectedIdx);
    
    // Display feedback & explanation
    feedbackBox.style.display = 'block';
    feedbackBox.innerHTML = `
        <div style="background:rgba(255,255,255,0.03); border:1px solid ${isCorrect ? 'var(--green)' : 'rgba(239, 68, 68, 0.4)'}; padding:15px; border-radius:16px; margin-bottom:12px;">
            <div style="color:${isCorrect ? 'var(--green)' : '#ef4444'}; font-weight:700; font-size:0.95rem; margin-bottom:6px; display:flex; align-items:center; gap:6px;">
                <i data-lucide="${isCorrect ? 'check-circle-2' : 'alert-circle'}"></i>
                ${isCorrect ? 'Correct Answer! Excellent!' : 'Oops, that is incorrect.'}
            </div>
            <p style="font-size:0.85rem; color:var(--text-muted); line-height:1.5;">${q.explanation}</p>
        </div>
        <button class="quiz-btn" style="width:100%" onclick="nextQuizQuestion()">
            ${quizState.currentQuestionIndex + 1 === quizQuestions.length ? 'View Final Results 🏆' : 'Next Question ➡️'}
        </button>
    `;
    
    lucide.createIcons();
}

function nextQuizQuestion() {
    quizState.currentQuestionIndex++;
    loadQuiz();
}

function renderQuizScore() {
    const box = document.getElementById('quiz-box');
    if (!box) return;
    
    const percentage = Math.round((quizState.score / quizQuestions.length) * 100);
    let feedback = "Democratic Citizen! 🇮🇳";
    let subFeedback = "You have a solid awareness of voter guidelines. Share this assistant to help family and friends!";
    
    if (percentage === 100) {
        feedback = "ECI Constitution Scholar! 🏛️";
        subFeedback = "Flawless score! You fully understand the processes of the Election Commission of India. You are ready to champion democracy!";
    } else if (percentage < 60) {
        feedback = "Aspiring Democracy Champion 🗳️";
        subFeedback = "Great effort! Review the 'Step Guide' tab or ask Chunav Guide questions to sharpen your voter knowledge.";
    }
    
    box.innerHTML = `
        <div class="quiz-score-card">
            <div class="badge-wrapper">
                <svg class="badge-svg" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="12" cy="12" r="10" fill="url(#saffronGreen)" stroke="var(--cyan)" stroke-width="0.5"/>
                    <path d="M12 7L13.85 10.75L18 11.35L15 14.28L15.7 18.4L12 16.45L8.3 18.4L9 14.28L6 11.35L10.15 10.75L12 7Z" fill="var(--text)"/>
                    <defs>
                        <linearGradient id="saffronGreen" x1="0" y1="0" x2="1" y2="1">
                            <stop offset="0%" stop-color="var(--saffron)" />
                            <stop offset="50%" stop-color="rgba(255,255,255,0.4)" />
                            <stop offset="100%" stop-color="var(--green)" />
                        </linearGradient>
                    </defs>
                </svg>
            </div>
            <h2 style="color:var(--saffron)">Challenge Finished!</h2>
            <div class="score-num">${quizState.score} / ${quizQuestions.length}</div>
            <div class="quiz-feedback">${feedback}</div>
            <div class="quiz-sub-feedback">${subFeedback}</div>
            <button class="quiz-btn" onclick="resetQuiz()">Restart Quiz 🔄</button>
        </div>
    `;
    
    // Celebrate complete/perfect score with subtle visual elements
    if (percentage === 100) {
        triggerLocalConfetti();
    }
}

function resetQuiz() {
    quizState = {
        currentQuestionIndex: 0,
        score: 0,
        answers: []
    };
    loadQuiz();
}

/**
 * pure CSS/JS Lightweight Confetti Celebration
 */
function triggerLocalConfetti() {
    const quizTab = document.getElementById('quiz-tab');
    if (!quizTab) return;
    
    for (let i = 0; i < 40; i++) {
        const confetti = document.createElement('div');
        confetti.style.position = 'absolute';
        confetti.style.width = '8px';
        confetti.style.height = '8px';
        confetti.style.backgroundColor = ['var(--saffron)', 'var(--cyan)', 'var(--green)', '#ffffff'][Math.floor(Math.random() * 4)];
        confetti.style.left = Math.random() * 90 + 5 + '%';
        confetti.style.top = '10%';
        confetti.style.borderRadius = '50%';
        confetti.style.zIndex = '10';
        confetti.style.opacity = Math.random();
        confetti.style.transform = `rotate(${Math.random() * 360}deg)`;
        
        quizTab.appendChild(confetti);
        
        const duration = Math.random() * 2000 + 1500;
        const animation = confetti.animate([
            { transform: 'translateY(0) rotate(0deg)', opacity: 1 },
            { transform: `translateY(350px) translateX(${Math.random() * 40 - 20}px) rotate(${Math.random() * 360}deg)`, opacity: 0 }
        ], {
            duration: duration,
            easing: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)'
        });
        
        animation.onfinish = () => confetti.remove();
    }
}

/* ==========================================================================
   🚨 APPLICATION INITIALIZER
   ========================================================================== */
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

// Run setup routines once the content is loaded
document.addEventListener('DOMContentLoaded', () => {
    switchTab('chat');
    loadSuggestions();
});
