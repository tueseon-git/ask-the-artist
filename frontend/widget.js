const API_BASE = "https://YOUR_RENDER_BACKEND_URL"; // replace with your deployed backend URL


const chatWindow = document.getElementById('chat-window');
const form = document.getElementById('chat-form');
const input = document.getElementById('msg');


function appendMessage(text, cls='bot'){
const el = document.createElement('div');
el.className = 'msg ' + cls;
el.textContent = text;
chatWindow.appendChild(el);
chatWindow.scrollTop = chatWindow.scrollHeight;
}


form.addEventListener('submit', async (e) => {
e.preventDefault();
const text = input.value.trim();
if(!text) return;
appendMessage(text, 'user');
input.value = '';
appendMessage('…', 'bot');
try {
const resp = await fetch(`${API_BASE}/chat`, {
method: 'POST',
headers: { 'Content-Type': 'application/json' },
body: JSON.stringify({ message: text })
});
const data = await resp.json();
// remove last loading message
const bots = chatWindow.querySelectorAll('.bot');
const lastBot = bots[bots.length - 1];
if(lastBot && lastBot.textContent === '…') lastBot.remove();
appendMessage(data.reply, 'bot');
} catch (err) {
console.error(err);
appendMessage("Sorry — I couldn't reach the artist. Please contact via the Contact page.", 'bot');
}
});