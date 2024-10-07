document.addEventListener("DOMContentLoaded", function () {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const letter = urlParams.get('letter');

    if (letter) {
        document.getElementById('selected-letter').textContent = letter;
        fetch(`/api/alpha/${letter}`)
            .then(response => response.json())
            .then(data => {
                const carList = document.getElementById('car-list');
                const csvData = [];
                carList.innerHTML = '';
                data[letter].forEach(car => {
                    const itemCar = document.createElement('li');
                    const carLink = document.createElement('a');
                    carLink.textContent = car;
                    carLink.href = `${encodeURIComponent(car)}`;
                    itemCar.appendChild(carLink);
                    carList.appendChild(itemCar);
                    csvData.push(car);
                });

                // Create CSV download button
                createCSVDownloadButton(csvData);
            })
            .catch(error => console.error('Error fetching data:', error));
    }
});

function createCSVDownloadButton(data) {
    const csvContent = "data:text/csv;charset=utf-8," + data.map(e => e).join("\n");

    const downloadLink = document.createElement("a");
    downloadLink.href = encodeURI(csvContent);
    downloadLink.download = `cars_${document.getElementById('selected-letter').textContent}.csv`;

    // Ensure the button is selected properly
    const downloadButton = document.querySelector(".rounded-button");

    if (downloadButton) {
        downloadButton.onclick = function () {
            downloadLink.click(); // Trigger the download
        };
    }
}