import { fetchData } from "./fetch";
const container = document.getElementById('cards');

var cards = fetchData('/api/brand/');

cards.forEach(() => {

    // const card = document.createElement("button");
    // card.classList = "vehicle-card";

    const content = `
        <button class="vehicle-card" data-modal-target="#modal">
            <img
                alt="image of a vehicle"
                src="https://storage.googleapis.com/a1aa/image/5RuT8CZtQd7UGJyUbVHeHHnIdwvTvYwOAd5eY1BOcpZayajTA.jpg"
            />
            <p>2024 4Runner</p>
        </button>
    `;

    container.innerHTML += content;
});