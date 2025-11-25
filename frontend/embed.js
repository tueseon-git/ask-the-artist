// ========== CONFIG ==========
const API_URL = "https://ask-the-artist-1.onrender.com";  // CHANGE THIS
// ============================

// Inject CSS
const style = document.createElement("style");
style.innerHTML = `
#chat-bubble {
    position: fixed;
    bottom: 22px;
    right: 22px;
    background-color: #8e44ad;
    color: white;
    width: 58px;
    height: 58px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    font-size: 28px;
    cursor: pointer;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    z-index: 99999;
}
#chat-widget {
    position: fixed;
    bottom: 90px;
    right: 20px;
    width: 320px;
    max-height: 480px;
    background: white;
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    z-index: 99999;
}
.hidden { display: none !important; }
.chat-header {
    background: #8e44ad;
    color: white;
    padding: 14px;
    text-align: center;
    font-size: 18px;
}
#chat-body {
    padding: 12px;
    flex: 1;
    overflow-y: auto;
    background: #fafafa;
    font-size: 15px;
}
.chat-input-container {
    display: flex;
    border-top: 1px solid #ddd;
    padding: 8px;
}
#chat-input {
    flex: 1;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 8px;
    font-size: 14px;
}
#send-btn {
    background: #8e44ad;
    color: white;
    border: none;
    padding: 10px 14px;
    margin-left: 8px;
    border-radius: 8px;
    cursor: pointer;
}
.user-msg, .bot-msg {
    padding: 10px 12px;
    margin-bottom: 10px;
    border-radius: 12px;
    max-width: 80%;
}
.user-msg {
    background: #d1c4e9;
    align-self: flex-end;
}
.bot-msg {
    background: #eee;
    align-self: flex-start;
}
.typing {
    font-style: italic;
    opacity: 0.6;
}
`;
document.head.appendChild(style);

// Inject HTML structure
const widgetWrapper = document.createElement("div");
widgetWrapper.innerHTML = `
<div id="chat-bubble">💬</div>
<div id="chat-widget" class="hidden">
    <div class="chat-header">Ask The Artist 🎨</div>
    <div id="chat-body"></div>
    <div class="chat-input-container">
        <input id="chat-input" type="text" placeholder="Ask something..." />
        <button id="send-btn">➤</button>
    </div>
</div>
`;
document.body.appendChild(widgetWrapper);

// Chat functionality
(function () {
    const chatWidget = document.getElementById("chat-widget");
    const chatBubble = document.getElementById("chat-bubble");
    const chatBody = document.getElementById("chat-body");
    const chatInput = document.getElementById("chat-input");
    const sendBtn = document.getElementById("send-btn");

    chatBubble.addEventListener("click", () => {
        chatWidget.classList.toggle("hidden");
    });

    sendBtn.addEventListener("click", sendMessage);
    chatInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") sendMessage();
    });

    function addMessage(text, type) {
        const msg = document.createElement("div");
        msg.className = type === "user" ? "user-msg" : "bot-msg";
        msg.innerText = text;
        chatBody.appendChild(msg);
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    async function sendMessage() {
        const text = chatInput.value.trim();
        if (!text) return;

        addMessage(text, "user");
        chatInput.value = "";

        const typing = document.createElement("div");
        typing.className = "bot-msg typing";
        typing.innerText = "Artist is thinking…";
        chatBody.appendChild(typing);

        try {
            const res = await fetch(`${API_URL}/ask`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ question: text }),
            });
            const data = await res.json();
            typing.remove();
            addMessage(data.answer || "No response", "bot");
        } catch {
            typing.remove();
            addMessage("⚠ Error: Could not connect to server.", "bot");
        }
    }
})();
