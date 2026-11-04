
const chatForm = document.getElementById("chat-form");
const messageInput = document.getElementById("message");
const chatBox = document.getElementById("chat-box");
const errorMessage = document.getElementById("error-message");
const newChatButton = document.getElementById("new-chat");

let conversationId = crypto.randomUUID();

// Display messages in chat
function addMessage(text, sender) {

    const welcome = document.querySelector(".welcome");

    if (welcome) {
        welcome.remove();
    }

    const messageDiv = document.createElement("div");

    messageDiv.classList.add("message", sender);

    messageDiv.textContent = text;

    chatBox.appendChild(messageDiv);

    chatBox.scrollTop = chatBox.scrollHeight;
}


// Send message to backend
chatForm.addEventListener("submit", async function(event) {

    event.preventDefault();

    const message = messageInput.value.trim();

    if (message === "") {
        return;
    }

    addMessage(message, "user");

    messageInput.value = "";

    errorMessage.textContent = "AI is thinking...";

    const sendButton = document.getElementById("send");
    sendButton.disabled = true;

    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message,
                conversation_id: conversationId
            })

        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Something went wrong");
        }

        conversationId = data.conversation_id;

        addMessage(data.reply, "bot");

        errorMessage.textContent = "";

    }

    catch (error) {

        errorMessage.textContent = error.message;

    }

    finally {

        sendButton.disabled = false;
        messageInput.focus();

    }

});


// Start a new conversation
newChatButton.addEventListener("click", async function() {

    try {
        await fetch("/reset", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                conversation_id: conversationId
            })
        });
    } catch (error) {
        console.log("Could not reset old conversation.");
    }

    conversationId = crypto.randomUUID();

    chatBox.innerHTML = `
        <div class="welcome">
            <h2>Welcome to SmartChat!</h2>
            <p>Ask me anything. I'm here to help you.</p>
        </div>
    `;

    errorMessage.textContent = "";

});
