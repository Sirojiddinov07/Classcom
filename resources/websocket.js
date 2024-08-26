document.addEventListener("DOMContentLoaded", function () {
    const notificationsList = document.getElementById("notifications");
    const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI0NjY5MzUwLCJpYXQiOjE3MjQ2NjU3NTAsImp0aSI6IjJjMzFkMTljNmFiMDRlYWRhYTllZTEzNzQ5MGFkYzc0IiwidXNlcl9pZCI6MX0.YLgKbEeCf9RRjQBqfzS8eomNU3qmdIU5Q8aaiwzH4u8"; // Replace with your actual token

    // Create a new WebSocket connection with custom headers
    const socket = new WebSocket("ws://localhost:8000/ws/notifications/");
    socket.onopen = function (event) {
        // Add the Bearer token to the headers
        socket.send(JSON.stringify({type: "auth", token: token}));
        console.log("WebSocket is open now.");
    };

    socket.onmessage = function (event) {
        const data = JSON.parse(event.data);
        if (data.type === "send_notification") {
            const notificationItem = document.createElement("li");
            notificationItem.textContent = data.message;
            notificationsList.appendChild(notificationItem);
        }
    };

    socket.onclose = function (event) {
        console.log("WebSocket is closed now.");
    };

    socket.onerror = function (error) {
        console.error("WebSocket error observed:", error);
    };
});