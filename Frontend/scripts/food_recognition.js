document.getElementById("imageForm").addEventListener("submit", function (e) {
    e.preventDefault();
    const formData = new FormData();
    const imageFile = document.getElementById("image").files[0];

    if (imageFile) {
        formData.append("image", imageFile);
        // Send the form data to the backend using fetch
        fetch("http://127.0.0.1:8888/recognize", {
            method: "POST",
            headers:{
                "Authorization": 'Bearer WOEqx6cGzWY1kX8Mz8aFiBjGFP4z3MbQ'
            },
            body: formData,
            credentials: "include"
        })
            .then(response => {
                if(response.status === 401){
                    alert("Invalid session! Please login again.");
                    window.location.href = "../pages/login.html";
                }
                if (!response.ok){
                    throw new Error("Falied to process the image.")
                }
                return response.blob(); // Datatype for sending image or large files.
            })
            .then(blob => {
                if (!blob){
                    alert("Failed to process the image.");
                }
        
                const imageUrl = URL.createObjectURL(blob);
        
                const resultDiv = document.getElementById("result");
                resultDiv.innerHTML = `<img src="${imageUrl}" alt="Detected Food" style="max-width: 300px; max-height: 400; border-radius: 8px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.18);">`;
        
                document.getElementById("status").innerText = "";
            })
            .catch(error => {
                console.error("Error:", error);
                document.getElementById("status").innerText = "Error processing image.";
            });
    } else {
        alert("Please select an image to upload.");
    }
});

