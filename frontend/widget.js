const API_URL = "https://ask-the-artist-1.onrender.com/chat";

const chatWidget = document.getElementById("chat-widget");
const chatBubble = document.getElementById("chat-bubble");
const chatBody = document.getElementById("chat-body");
const chatInput = document.getElementById("chat-input");
const sendBtn = document.getElementById("send-btn");

// Toggle widget visibility
chatBubble.addEventListener("click", () => {
    chatWidget.classList.toggle("hidden");
});

// Send message
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

    // Add user message
    addMessage(text, "user");
    chatInput.value = "";

    // Typing indicator
    const typing = document.createElement("div");
    typing.className = "bot-msg typing";
    typing.innerText = "Artist is thinking…";
    chatBody.appendChild(typing);
    chatBody.scrollTop = chatBody.scrollHeight;

    try {
        const res = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: text })   // ✅ FIXED
        });

        const data = await res.json();

        typing.remove();

        addMessage(
            data.answer || "No response from server.",   // ✅ FIXED
            "bot"
        );

    } catch (err) {
        typing.remove();
        addMessage("⚠ Error: Could not connect to server.", "bot");
    }
}
