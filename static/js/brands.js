function changePage(brand) {
    console.log(brand);
    window.location.href = `/models?brand=${brand}`;
}

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
                    carLink.href = "#";
                    carLink.onclick = function() {
                        let carEncode = car.replace(/ /g, "%20").replace(/&/g, "%26");
                        changePage(carEncode);
                    };
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

function getInputValue() {
    const inputElement = document.getElementById('inpsearch').value.toUpperCase();
    console.log(inputElement);
    window.location.href = `/models?brand=${inputElement}`;
}

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