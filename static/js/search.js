// const container = document.getElementById('cards');

// searchModel();
// let carFromsearch;
// function searchModel(){
//     fetch(`/api/search?q=${encodeURIComponent(query)}`)
//         .then(response => response.json)
//         .then(data =>{
//             carFromsearch = [];
//             Object.keys(data).forEach((k) =>{
//                 carFromsearch.push(k);
//             })
//             localStorage.setItem('carFromSearch', JSON.stringify(carFromSearch));
//         })
//         .catch(error => console.error('Error fetching search data:', error));
// }


const container = document.getElementById('cards');
let srh;
let dataJs;
const storedCars = localStorage.getItem('carFromSearch');
let carFromSearch = storedCars ? JSON.parse(storedCars) : [];

document.addEventListener("DOMContentLoaded", async function () {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    srh = urlParams.get('q');
    await run();
});

async function run() {
    if (srh) {
        document.getElementById('srh-title').textContent = srh;
        try {
            const response = await fetch(`/api/search?q=${srh}`);
            console.log("juu4")
            console.log(response)
            const data = await response.json();
            populateVehicleCards(data);
            dataJs = data;
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }
}
async function search(){
    searchedVehicleCards(carFromSearch);
}
function searchedVehicleCards(data){
    Object.keys(data).forEach((k) => {
        const car = data[k];
        console.log(k)
        if (car == null) {
            `
            <button class="vehicle-card" data-modal-target="#modal" data-text="${k}" data-image="https://st4.depositphotos.com/14953852/24787/v/450/depositphotos_247872612-stock-illustration-no-image-available-icon-vector.jpg">
                <img alt="image of a vehicle" src="https://st4.depositphotos.com/14953852/24787/v/450/depositphotos_247872612-stock-illustration-no-image-available-icon-vector.jpg" />
                <p>${k}</p>
            </button>`
        }
        else{

        const content = `
            <button class="vehicle-card" data-modal-target="#modal" data-text="${k}" data-image="${car.img}">
                <img alt="image of a vehicle" src="${car.img}" />
                <p>${k}</p>
            </button>`;
        container.innerHTML += content;
        }
    });
}
function populateVehicleCards(data) {
    Object.keys(data).forEach((k) => {
        const car = data[k];
        if (car == null) {
            `
            <button class="vehicle-card" data-modal-target="#modal" data-text="${k}" data-image="https://st4.depositphotos.com/14953852/24787/v/450/depositphotos_247872612-stock-illustration-no-image-available-icon-vector.jpg">
                <img alt="image of a vehicle" src="https://st4.depositphotos.com/14953852/24787/v/450/depositphotos_247872612-stock-illustration-no-image-available-icon-vector.jpg" />
                <p>${k}</p>
            </button>`
        }
        else{

        const content = `
            <button class="vehicle-card" data-modal-target="#modal" data-text="${k}" data-image="${car.img}">
                <img alt="image of a vehicle" src="${car.img}" />
                <p>${k}</p>
            </button>`;
        container.innerHTML += content;
        }
    });

    // Call the function to add event listeners to the cards
    addCardEventListeners(data);
}

function addCardEventListeners(DATA) {
    const cardItems = document.querySelectorAll('.vehicle-card');
    const overlay = document.getElementById('overlay');

    cardItems.forEach(card => {
        card.addEventListener('click', () => {
            const content = {
                image: card.dataset.image, // Extract image URL from data-image
                text: card.dataset.text // Extract text from data-text
            };
            openModal(content, DATA); // Open modal with the provided content
        });
    });

    // Close modal when clicking on overlay
    overlay.addEventListener('click', () => {
        const modals = document.querySelectorAll('.modal.active');
        modals.forEach(modal => {
            closeModal(modal);
        });
    });
}

function openModal(content, DATA) {
    createDynamicModal(content, DATA); // Pass the content and DATA to createDynamicModal
}

function createDynamicModal(content, DATA) {
    const key_data = content.text;
    const details = DATA[key_data];

    if (!details) {

        const modal = document.createElement('div');
        modal.classList.add('modal', 'active');
        modal.innerHTML = `
        <div class="modal-header">
            <div class="title">${content.text}</div>        
            <button data-close-button class="close-button">&times;</button>
        </div>
        <div class="modal-body">
            <img class="image-car" src="${content.image}" alt="Image">
            <div class="modal-object">
                <ul>No infomation </ul>
            </div>
        </div>
        `;
        document.body.appendChild(modal);

        // Add event listener to close modal
        const closeButton = modal.querySelector('[data-close-button]');
        closeButton.addEventListener('click', () => {
            closeModal(modal);
        });

        overlay.classList.add('active'); // Show overlay
        
        
    }
    else {

    const modal = document.createElement('div');
    modal.classList.add('modal', 'active');

    const keyValueString = Object.entries(details)
        .map(([key, value]) => `<li>${key}: ${value}</li>`).join('');

    modal.innerHTML = `
        <div class="modal-header">
            <div class="title">${content.text}</div>        
            <button data-close-button class="close-button">&times;</button>
        </div>
        <div class="modal-body">
            <img class="image-car" src="${content.image}" alt="Image">
            <div class="modal-object">
                <ul>${keyValueString}</ul>
            </div>
        </div>
    `;
    document.body.appendChild(modal);

    // Add event listener to close modal
    const closeButton = modal.querySelector('[data-close-button]');
    closeButton.addEventListener('click', () => {
        closeModal(modal);
    });

    overlay.classList.add('active'); // Show overlay
    }
}