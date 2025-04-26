document.getElementById("imageForm").addEventListener("submit", function (e) {
    e.preventDefault();
    const formData = new FormData();
    const imageFile = document.getElementById("image").files[0];

    if (imageFile) {
        formData.append("image", imageFile);
        // Send the form data to the backend using fetch
        fetch("http://127.0.0.1:8888/predict", {
            method: "POST",
            headers: {
                "Authorization": 'Bearer 574dj9rOox5xpVuqcnkX2bjHvgadjThx'
            },
            body: formData,
            credentials: "include"
        })
            .then(response => {
                if(response.status === 401){
                    alert("Invalid session! Please login again.");
                    window.location.href = "../pages/login.html";
                }
                return response.json();
            })
            .then(data => {
                console.log("Response from backend:", data);
                const tbody = document.getElementById("resultBody");
                tbody.innerHTML = '';
                data.forEach(item => {
                    let row = `<tr>
                            <td>${item.Food_Item}</td>
                            <td>${item["Calories (kcal)"]}</td>
                            <td>${item["Protein (g)"]}</td>
                            <td>${item["Carbohydrates (g)"]}</td>
                            <td>${item["Fat (g)"]}</td>
                            <td>${item["Fiber (g)"]}</td>
                            <td>${item["Sugar (g)"]}</td>
                            <td>${[item["Calories (kcal)"]+item["Protein (g)"]+item["Carbohydrates (g)"]+item["Fat (g)"]+item["Fiber (g)"]+item["Sugar (g)"]]} 
                        </tr>`;// SI unit to be checked!
                    tbody.innerHTML += row;
                })
            })
            .catch(error => {
                console.error("Error uploading image:", error);
            });
    } else {
        alert("Please select an image to upload.");
    }
});

