document.addEventListener('DOMContentLoaded', async () => {
    const tableBody = document.getElementById('tableBody');
    const showHistoryButton = document.getElementById('showHistory');
    
    async function fetchFoodHistory(startDate, endDate) {
        startDate = document.getElementById('startDate').value;
        endDate = document.getElementById('endDate').value;
        // console.log(startDate,endDate,"my new")
        try {
            const response = await fetch('http://127.0.0.1:8888/food_history', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer i655AfW4OIpOWHB7IxZ0pz3FLx5IHwJ7'
                },
                body: JSON.stringify({"start_date": startDate, "end_date": endDate })
            });
            console.log(response)
    
            if (!response.ok) {
                console.error('Failed to fetch food history', response.status, response.statusText);
                return [];
            }
            // const data = await response.json();
            // console.log('Fetched Data:', data); // Log the fetched data
            // return data;
            return await response.json();
        } catch (error) {
            console.error('Error:', error);
            return [];
        }
    }

    function filterDataByDate(data, startDate, endDate) {
        return data.filter(food => {
            const foodDate = new Date(food.Date);
            return (!startDate || foodDate >= startDate) && (!endDate || foodDate <= endDate);
        });
    }

    function formatDate(date) {
        return date.toISOString().split('T')[0]; // Converts to YYYY-MM-DD format
    }

    function displayData(data) {
        tableBody.innerHTML = '';
        data.forEach(food => {
            const row = `
                <tr>
                    <td>${food.Date}</td>
                    <td>${food.Time}</td>
                    <td>${food.Food_Item}</td>
                    <td>${food["Calories (kcal)"]}</td>
                    <td>${food["Protein (g)"]}</td>
                    <td>${food["Fat (g)"]}</td>
                    <td>${food["Carbohydrates (g)"]}</td>
                    <td>${food["Fiber (g)"]}</td>
                    <td>${food["Sugar (g)"]}</td>
                </tr>`;
            tableBody.innerHTML += row;
        });
    }

    showHistoryButton.addEventListener('click', async () => {
        const startDate = new Date(document.getElementById('startDate').value);
        const endDate = new Date(document.getElementById('endDate').value);
        const formattedStartDate = formatDate(startDate);
        const formattedEndDate = formatDate(endDate);
        const payload ={
            "startDate": formattedStartDate,
            "endDate": formattedEndDate
        }
        console.log(payload)
        const allData = await fetchFoodHistory(formattedStartDate, formattedEndDate);
        const filteredData = filterDataByDate(allData, startDate, endDate);
        displayData(filteredData);
    });
    console.log("displayed")
    // Load all data on initial page load
    const allData = await fetchFoodHistory();
    displayData(allData);
});