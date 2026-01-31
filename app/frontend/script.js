let ws = null;
let currentBotMessage = null;
let currentBotMessageText = "";
let isTyping = false;

// WebSocket connection
function connect() {
    ws = new WebSocket("ws://localhost:8000/ws/chat");
    
    ws.onopen = function() {
        updateStatus(true);
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
        updateStatus(false);
    };

    ws.onclose = function() {
        console.log("Disconnected from WebSocket");
        updateStatus(false);
        // Try to reconnect after 3 seconds
        setTimeout(connect, 3000);
    };
}

// Update connection status
function updateStatus(connected) {
    const statusDot = document.getElementById("statusDot");
    const statusText = document.getElementById("statusText");
    
    if (connected) {
        statusDot.classList.add("connected");
        statusText.textContent = "Connected";
    } else {
        statusDot.classList.remove("connected");
        statusText.textContent = "Disconnected";
    }
}

// Send message
function sendMessage() {
    const input = document.getElementById("messageInput");
    const message = input.value.trim();
    
    if (!message) return;
    
    if (!ws || ws.readyState !== WebSocket.OPEN) {
        alert("Not connected to server. Please wait...");
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

// Connect on page load
window.addEventListener("load", function() {
    connect();
});
