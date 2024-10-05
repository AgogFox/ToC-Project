const container = document.getElementById('cards');

//sample
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

    const card = document.createElement("div");
    card.classList = "card-body";

    const content = `
        <div class="card">
            <div class="card-header" id="cards">
                <img src="${result.image}" class="cardImage">
            </div>
            <div class="card-body">
                <h5>${result.title}</h5>
            </div>
        </div>
    `;

    container.innerHTML += content;
});