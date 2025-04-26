
document.getElementById("registerForm").addEventListener("submit", async (event) => {
    event.preventDefault();

    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const response = await fetch("http://127.0.0.1:8888/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": 'Bearer qFHgqreAnBtjLyJL06UMtxmfrFi8QWPj'
        },
        body: JSON.stringify({ name, email, password }),
    });

    if (response.ok) {
        alert("Registration successful, please relogin");
        console.log("Registration successful, please relogin");
        window.location.href = "../pages/login.html";
    }
    else{
        alert("Email already exists. Please try with a different email.")
        console.log(await response.text())
    }

});
