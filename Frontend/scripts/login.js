
document.getElementById("loginForm").addEventListener("submit", async (event) => {
    // console.log("Login Called")
    event.preventDefault();
    
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    
    const response = await fetch("http://127.0.0.1:8888/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": 'Bearer CBvERn0lxjJMAQdDaLnAKRysM02YNOs1'
        },
        body: JSON.stringify({ email: email, password: password })
    });

    console.log(response)

    
    if (response.ok) {
        alert("Login Successfull!")
        window.location.href = "../pages/home.html";
    }
    else{
        alert("Invalid email or password!");
        console.log(await response.text());
    }
    
});
