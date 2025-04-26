document.getElementById("contactForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    const formData = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        message: document.getElementById("msg").value
    };

    try {
        const response = await fetch("http://127.0.0.1:8888/send_email", {
            method: "POST",
            headers: { "Content-Type": "application/json",
                "Authorization": 'Bearer hyoa wexw ebne myxd'
             },
            body: JSON.stringify(formData)
        });

        if (response.ok) {
            alert("Your message has been sent! We will get back to you soon.");
            document.getElementById("contactForm").reset();
        } else {
            alert("Failed to send message. Please try again later.");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Something went wrong!");
    }
});