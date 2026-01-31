const API_URL = "http://localhost:8000";
const WS_URL = "ws://localhost:8000";

let ws = null;
let currentSessionId = null;
let currentBotMessage = null;
let currentBotMessageText = "";
let isTyping = false;

// Load sessions on page load
window.addEventListener("load", function() {
    loadSessions();
});

// Create new chat session
async function createNewChat() {
    try {
        const response = await fetch(`${API_URL}/sessions`, {
            method: 'POST'
        });
        const data = await response.json();
        currentSessionId = data.session_id;
        
        // Clear chat and connect
        clearChat();
        connectWebSocket(currentSessionId);
        loadSessions();
        
        // Enable input
        enableInput();
    } catch (error) {
        console.error("Error creating session:", error);
        alert("Failed to create new chat session");
    }
}

// Load all sessions
async function loadSessions() {
    try {
        const response = await fetch(`${API_URL}/sessions`);
        const data = await response.json();
        displaySessions(data.sessions);
    } catch (error) {
        console.error("Error loading sessions:", error);
    }
}

// Display sessions in sidebar
function displaySessions(sessions) {
    const sessionsList = document.getElementById("sessionsList");
    
    if (sessions.length === 0) {
        sessionsList.innerHTML = '<div class="no-sessions">No chat sessions yet</div>';
        return;
    }
    
    sessionsList.innerHTML = '';
    sessions.forEach(session => {
        const sessionDiv = document.createElement("div");
        sessionDiv.className = "session-item" + (session.session_id === currentSessionId ? " active" : "");
        sessionDiv.innerHTML = `
            <div class="session-info" onclick="switchSession('${session.session_id}')">
                <div class="session-title">${session.title}</div>
                <div class="session-meta">${session.message_count} messages</div>
            </div>
            <button class="session-delete" onclick="deleteSession('${session.session_id}', event)">
                🗑️
            </button>
        `;
        sessionsList.appendChild(sessionDiv);
    });
}

// Switch to a different session
async function switchSession(sessionId) {
    if (ws) {
        ws.close();
    }
    currentSessionId = sessionId;
    clearChat();
    connectWebSocket(sessionId);
    loadSessions();
    enableInput();
}

// Delete a single session
async function deleteSession(sessionId, event) {
    event.stopPropagation();
    
    if (!confirm("Delete this chat session?")) return;
    
    try {
        await fetch(`${API_URL}/sessions/${sessionId}`, {
            method: 'DELETE'
        });
        
        if (sessionId === currentSessionId) {
            currentSessionId = null;
            clearChat();
            disableInput();
            if (ws) ws.close();
        }
        
        loadSessions();
    } catch (error) {
        console.error("Error deleting session:", error);
        alert("Failed to delete session");
    }
}

// Delete all sessions
async function deleteAllChats() {
    if (!confirm("Delete ALL chat sessions? This cannot be undone!")) return;
    
    try {
        await fetch(`${API_URL}/sessions`, {
            method: 'DELETE'
        });
        
        currentSessionId = null;
        clearChat();
        disableInput();
        if (ws) ws.close();
        loadSessions();
    } catch (error) {
        console.error("Error deleting all sessions:", error);
        alert("Failed to delete all sessions");
    }
}

// WebSocket connection
function connectWebSocket(sessionId) {
    if (ws) {
        ws.close();
    }
    
    ws = new WebSocket(`${WS_URL}/ws/chat/${sessionId}`);
    
    ws.onopen = function() {
        updateStatus(true, "Connected");
        console.log("Connected to WebSocket");
    };

    ws.onmessage = function(event) {
        const data = event.data;
        
        if (data === "[DONE]") {
            // Message complete - reset for next message
            isTyping = false;
            removeTypingIndicator();
            currentBotMessage = null;
            currentBotMessageText = "";
            loadSessions(); // Refresh to update message count
        } else if (data.startsWith("[ERROR]")) {
            removeTypingIndicator();
            alert(data);
        } else {
            // Receiving message character by character
            if (!currentBotMessage) {
                removeTypingIndicator();
                currentBotMessage = addMessage("", "bot");
                currentBotMessageText = "";
            }
            currentBotMessageText += data;
            currentBotMessage.textContent = currentBotMessageText;
            scrollToBottom();
        }
    };

    ws.onerror = function(error) {
        console.error("WebSocket Error:", error);
        updateStatus(false, "Error");
    };

    ws.onclose = function() {
        console.log("Disconnected from WebSocket");
        updateStatus(false, "Disconnected");
    };
}

// Update connection status
function updateStatus(connected, text) {
    const statusDot = document.getElementById("statusDot");
    const statusText = document.getElementById("statusText");
    
    if (connected) {
        statusDot.classList.add("connected");
        statusText.textContent = text || "Connected";
    } else {
        statusDot.classList.remove("connected");
        statusText.textContent = text || "Disconnected";
    }
}

// Send message
function sendMessage() {
    const input = document.getElementById("messageInput");
    const message = input.value.trim();
    
    if (!message) return;
    
    if (!ws || ws.readyState !== WebSocket.OPEN) {
        alert("Not connected to server. Please create a new chat.");
        return;
    }
    
    // Reset bot message state for new response
    currentBotMessage = null;
    currentBotMessageText = "";
    
    // Add user message to chat
    addMessage(message, "user");
    
    // Show typing indicator
    showTypingIndicator();
    
    // Send to WebSocket
    ws.send(message);
    
    // Clear input
    input.value = "";
    input.style.height = "auto";
    
    // Scroll to bottom
    scrollToBottom();
}

// Add message to chat
function addMessage(text, sender) {
    const messagesContainer = document.getElementById("chatMessages");
    
    // Remove welcome message if it exists
    const welcomeMsg = messagesContainer.querySelector(".welcome-message");
    if (welcomeMsg) {
        welcomeMsg.remove();
    }
    
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${sender}`;
    
    const avatar = document.createElement("div");
    avatar.className = "message-avatar";
    avatar.textContent = sender === "user" ? "👤" : "🤖";
    
    const content = document.createElement("div");
    content.className = "message-content";
    content.textContent = text;
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);
    messagesContainer.appendChild(messageDiv);
    
    scrollToBottom();
    
    return content; // Return the content element for streaming updates
}

// Show typing indicator
function showTypingIndicator() {
    if (isTyping) return;
    
    isTyping = true;
    const messagesContainer = document.getElementById("chatMessages");
    
    const typingDiv = document.createElement("div");
    typingDiv.className = "message bot";
    typingDiv.id = "typingIndicator";
    
    const avatar = document.createElement("div");
    avatar.className = "message-avatar";
    avatar.textContent = "🤖";
    
    const content = document.createElement("div");
    content.className = "message-content";
    
    const indicator = document.createElement("div");
    indicator.className = "typing-indicator";
    indicator.innerHTML = "<span></span><span></span><span></span>";
    
    content.appendChild(indicator);
    typingDiv.appendChild(avatar);
    typingDiv.appendChild(content);
    messagesContainer.appendChild(typingDiv);
    
    scrollToBottom();
}

// Remove typing indicator
function removeTypingIndicator() {
    const indicator = document.getElementById("typingIndicator");
    if (indicator) {
        indicator.remove();
    }
}

// Clear chat messages
function clearChat() {
    const messagesContainer = document.getElementById("chatMessages");
    messagesContainer.innerHTML = '<div class="welcome-message"><p>👋 Ready to chat!</p><p>Type your message below.</p></div>';
}

// Enable input
function enableInput() {
    document.getElementById("messageInput").disabled = false;
    document.getElementById("sendButton").disabled = false;
}

// Disable input
function disableInput() {
    document.getElementById("messageInput").disabled = true;
    document.getElementById("sendButton").disabled = true;
    updateStatus(false, "No session");
}

// Toggle sidebar
function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    sidebar.classList.toggle("hidden");
}

// Scroll to bottom of chat
function scrollToBottom() {
    const messagesContainer = document.getElementById("chatMessages");
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Auto-resize textarea
const messageInput = document.getElementById("messageInput");
messageInput.addEventListener("input", function() {
    this.style.height = "auto";
    this.style.height = (this.scrollHeight) + "px";
});

// Send on Enter key (Shift+Enter for new line)
messageInput.addEventListener("keydown", function(event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
});
