

document.addEventListener("DOMContentLoaded", () => {
    const chatHistory = document.getElementById("chat-history");
    const messageInput = document.getElementById("message-input");
    const sendButton = document.getElementById("send-button");

    const API_BASE_URL = "http://127.0.0.1:8000";

    const fetchChatHistory = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/history`);
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            const data = await response.json();
            chatHistory.innerHTML = ""; // Clear existing history
            data.history.forEach((message) => {
                appendMessage(message.role, message.content);
            });
        } catch (error) {
            console.error("Error fetching chat history:", error);
        }
    };

    const appendMessage = (role, content) => {
        const messageElement = document.createElement("div");
        messageElement.classList.add("message", role);

        // Ensure proper rendering of HTML (bold, bullet points, etc.)
        messageElement.innerHTML = `<b>${role === "user" ? "You" : "Pregnicare AI"}:</b><br>${content}`;

        chatHistory.appendChild(messageElement);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    };

    const sendMessage = async () => {
        const message = messageInput.value.trim();
        if (message) {
            appendMessage("user", message);
            messageInput.value = "";

            try {
                const response = await fetch(`${API_BASE_URL}/chat`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ message }),
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }

                const data = await response.json();
                appendMessage("bot", data.response);
            } catch (error) {
                console.error("Error sending message:", error);
                appendMessage("bot", "<b>⚠️ Error:</b> Unable to connect to the server. Please try again!");
            }
        }
    };

    sendButton.addEventListener("click", sendMessage);
    messageInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            sendMessage();
        }
    });

    fetchChatHistory();
});

// document.addEventListener("DOMContentLoaded", () => {
//     const chatHistory = document.getElementById("chat-history");
//     const messageInput = document.getElementById("message-input");
//     const sendButton = document.getElementById("send-button");

//     const API_BASE_URL = "http://127.0.0.1:8000";

//     const appendMessage = (role, content) => {
//         const messageContainer = document.createElement("div");
//         messageContainer.classList.add("message-container", role);

//         // Bot Profile GIF (Only for bot messages)
//         if (role === "bot") {
//             const botProfile = document.createElement("img");
//             botProfile.src = "static/bot-profile.gif"; // GIF instead of PNG
//             botProfile.alt = "Bot";
//             botProfile.classList.add("bot-profile");
//             messageContainer.appendChild(botProfile);
//         }

//         const messageElement = document.createElement("div");
//         messageElement.classList.add("message", role);
//         messageElement.innerHTML = `<b>${role === "user" ? "You" : "Pregnicare AI"}:</b><br>${content}`;

//         messageContainer.appendChild(messageElement);
//         chatHistory.appendChild(messageContainer);
//         chatHistory.scrollTop = chatHistory.scrollHeight;
//     };

//     const sendMessage = async () => {
//         const message = messageInput.value.trim();
//         if (message) {
//             appendMessage("user", message);
//             messageInput.value = "";

//             try {
//                 const response = await fetch(`${API_BASE_URL}/chat`, {
//                     method: "POST",
//                     headers: { "Content-Type": "application/json" },
//                     body: JSON.stringify({ message }),
//                 });

//                 if (!response.ok) {
//                     throw new Error(`HTTP error! Status: ${response.status}`);
//                 }

//                 const data = await response.json();
//                 appendMessage("bot", data.response);
//             } catch (error) {
//                 console.error("Error sending message:", error);
//                 appendMessage("bot", "<b>⚠️ Error:</b> Unable to connect to the server. Please try again!");
//             }
//         }
//     };

//     sendButton.addEventListener("click", sendMessage);
//     messageInput.addEventListener("keypress", (e) => {
//         if (e.key === "Enter") {
//             sendMessage();
//         }
//     });
// });

