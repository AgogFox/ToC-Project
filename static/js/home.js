function changePage(letter) {
    fetch(`/api/alpha/${letter}`)
        .then(response => response.json())
        .then(data => {
            window.location.href = `/brands?letter=${letter}`;
        });
}


function getInputValue() {
    const inputElement = document.getElementById('inpsearch').value.toUpperCase();
    console.log(inputElement);
    window.location.href = `/models?brand=${inputElement}`;
}


const container = document.getElementById('character');


for (let i = 65; i <= 90; i++) {
    let ch = String.fromCharCode(i);
    const char = document.createElement("div");
    char.classList = "char-body";
    
    const content = `
        <div class="card">
            <button  onclick="changePage('${ch}')" class="char-button" id="${ch}" >
                <h3>${ch}</h3>
            </div>
        </div>
    `;
    container.innerHTML += content;
};