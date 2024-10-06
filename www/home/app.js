const container = document.getElementById('character');

for (let i = 65; i <= 90; i++) {
    let ch = String.fromCharCode(i);
    const char = document.createElement("div");
    char.classList = "char-body";
    
    const content = `
        <div class="card">
            <button id="character">
                <h3>${ch}</h3>
            </div>
        </div>
    `;

    container.innerHTML += content;
};