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
                carList.innerHTML = '';
                data[letter].forEach(car => {
                    const itemCar = document.createElement('li');
                    const carLink = document.createElement('a');
                    carLink.textContent = car;
                    carLink.href = `${encodeURIComponent(car)}`;
                    itemCar.appendChild(carLink);
                    carList.appendChild(itemCar);
                });
            })
            .catch(error => console.error('Error fetching data:', error));
    }
});
