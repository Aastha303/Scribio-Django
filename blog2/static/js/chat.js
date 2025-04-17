function getCSRFToken() {
    return document.cookie.split('; ').find(row => row.startsWith('csrftoken'))?.split('=')[1];
}

function sendQuery() {
    const userText = document.getElementById("chatInput").value;
    const outputBox = document.getElementById("chatOutput");

    if (!userText.trim()) {
        outputBox.innerText = "Please enter something first.";
        return;
    }

    outputBox.innerText = "Thinking...";

    // Update fetch URL to match the correct path
    fetch("/profile/chatbot", {  // Correct URL
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({ message: userText }),
    })
    .then(response => response.json())
    .then(data => {
        outputBox.innerText = data.response || "Sorry, I couldn't understand.";
        document.getElementById("chatInput").value = "";  // Clear the input
    })
    .catch(error => {
        outputBox.innerText = "Oops! Something went wrong.";
        console.error("Error:", error);
    });
}