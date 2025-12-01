function goBack() {
    history.back();
}

function addMessage(role, text) {
    const area = document.getElementById("chat-area");
    const div = document.createElement("div");

    div.className = "chat-msg system-msg";

    div.innerHTML = text;
    area.appendChild(div);

    area.scrollTop = area.scrollHeight;
}

function sendQuestion() {
    const q = document.getElementById("question").value.trim();
    const truth = document.getElementById("truth").value;

    if (!q) return;

    addMessage("user", "<b>You:</b> " + q);
    document.getElementById("question").value = "";

    fetch("/ask", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ question: q, truth })
    })
    .then(r => r.json())
    .then(d => {
        addMessage("ai", "<b>Answer:</b> " + d.answer);
    });
}
