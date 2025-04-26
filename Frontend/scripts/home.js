document.getElementById("logoutButton").addEventListener("click", async (event) =>{
    const response = await fetch("http://127.0.0.1:8888/logout", {
        method: "get",
    })

    data = await response.json()
    console.log(data)
    if (response.ok){
        window.location.href = "../pages/index.html";
    }
});
