document.addEventListener("DOMContentLoaded", function () {
    let theme = document.getElementById("theme");
    theme.addEventListener("click", function () {
        var themeLink = document.getElementById("theme_css");
        var themeIcon = document.getElementById("theme_icon");
        if (themeLink.getAttribute("href") === "/static/css/light_theme.css") {
            themeLink.setAttribute("href", "/static/css/dark_theme.css");
            themeIcon.setAttribute("src", "/static/images/moon.svg");
            themeIcon.setAttribute("alt", "Dark Mode");
        } else {
            themeLink.setAttribute("href", "/static/css/light_theme.css");
            themeIcon.setAttribute("src", "/static/images/sun.svg");
            themeIcon.setAttribute("alt", "Light Mode");
        }
    });

    const input = document.getElementById("userInput");
    const messageContainer = document.getElementById("messageContainer");

    input.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            const text = input.value.trim();
            if (text !== "") {
                if (input.classList.contains("centered")) {
                    input.classList.remove("centered");
                    input.classList.add("fixed");
                    messageContainer.classList.add("active");
                }
                showUserMessage(text);
                getAnswer(text).then(response => showSystemMessage(response));
                input.value = "";
            
                messageContainer.scrollTop = messageContainer.scrollHeight;
            }
        }
    });
    const showUserMessage = (message) => {
        const messageElement = document.createElement("div");
        messageElement.className = "user_message";
        messageElement.textContent = message;
        messageContainer.appendChild(messageElement);
    }

    const showSystemMessage = (message) => {
        const messageElement = document.createElement("div");
        messageElement.className = "system_message";
        messageElement.textContent = message;
        messageContainer.appendChild(messageElement);
    } 

    async function getAnswer(question) {
        const response = await fetch('/get_answer', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: question })
        });
        const data = await response.json();
        return data.answer;
    }
});
