// import { fetchData } from "./fetch";
const container = document.getElementById('cards');

// var cards = fetchData('/api/brand/a');

const cards = [{
    title: "something/blog/test1",
    image: "https://www.supercars.net/blog/wp-content/uploads/2016/04/2004_Fuore_BlackJagConcept7.jpg",
}, {
    title: "something/blog/test2",
    image: "https://www.supercars.net/blog/wp-content/uploads/2016/04/2004_Fuore_BlackJagConcept7.jpg",
}, {
    title: "something/blog/test3",
    image: "https://www.supercars.net/blog/wp-content/uploads/2016/04/2004_Fuore_BlackJagConcept7.jpg",
}, {
    title: "something/blog/test4",
    image: "https://www.supercars.net/blog/wp-content/uploads/2016/04/2004_Fuore_BlackJagConcept7.jpg",
}, {
    title: "something/blog/test5",
    image: "https://www.supercars.net/blog/wp-content/uploads/2016/04/2004_Fuore_BlackJagConcept7.jpg",
}, {
    title: "something/blog/test6",
    image: "https://www.supercars.net/blog/wp-content/uploads/2016/04/2004_Fuore_BlackJagConcept7.jpg",
}, {
    title: "something/blog/test6",
    image: "https://www.supercars.net/blog/wp-content/uploads/2016/04/2004_Fuore_BlackJagConcept7.jpg",
}, {
    title: "something/blog/test6",
    image: "https://www.supercars.net/blog/wp-content/uploads/2016/04/2004_Fuore_BlackJagConcept7.jpg",
}];

cards.forEach((result) => {
    console.log(result)

    // const card = document.createElement("button");
    // card.classList = "vehicle-card";

    const content = `
        <button class="vehicle-card" data-modal-target="#modal">
            <img
                alt="image of a vehicle"
                src="${result.image}"
            />
            <p>dfhz</p>
        </button>
    `;

    container.innerHTML += content;
});