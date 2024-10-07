
const container = document.getElementById('cards');





async function run() {


    let DATA;

    await fetch(`http://127.0.0.1:5000/api/brand/ABARTH`)
                .then(response => response.json())
                .then(data => {
                    DATA = data
                    Object.keys(data).forEach((k) => {
                        car = data[k]

                        // const card = document.createElement("button");
                        // card.classList = "vehicle-card";
                        const content = 
                            `<button class="vehicle-card" data-modal-target="#modal" data-text="${k}" data-image="${car.img}" \">
                                <img
                                    alt="image of a vehicle"
                                    src="${car.img}"
                                />
                                <p >${k}</p>
                            </button>`
                        ;
                        
                            container.innerHTML += content;
                        ;
                
                    });


                })
                .catch(error => console.error('Error fetching data:', error));
        




    // เลือก card ทุกใบ
    const cardItems = document.querySelectorAll('.vehicle-card');
    const overlay = document.getElementById('overlay');

    
    
    // ฟังก์ชันเพื่อสร้าง modal
    function createDynamicModal(content) {

        key_data = content.text
        
        details = DATA[key_data]
        

    
        const modal = document.createElement('div');
        modal.classList.add('modal', 'active');

        const keyValueString = Object.entries(details)
        .map(([key, value]) => `<li>${key}: ${value}</li>`).join('');

        // const keyValueString = contentArray.map(item => `<li>${item.text} : ${item.text}</li>`).join('');

        // content.text = "1948→1950 Cisitalia-Abarth 204 A"
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


        // เพิ่ม event listener เพื่อปิด modal
        const closeButton = modal.querySelector('[data-close-button]');
        closeButton.addEventListener('click', () => {
            closeModal(modal);
        });

        overlay.classList.add('active'); // เปิด overlay
    }

    // ฟังก์ชันเพื่อเปิด modal
    function openModal(content) {
        createDynamicModal(content); // สร้าง modal โดยใช้ข้อมูลที่ส่งเข้ามา
    }

    // ฟังก์ชันเพื่อปิด modal
    function closeModal(modal) {
        if (modal == null) return;
        modal.classList.remove('active');
        overlay.classList.remove('active');
        modal.remove(); // ลบ modal ออกจาก DOM
    }

    // เพิ่ม event listener เมื่อคลิกที่ card
    cardItems.forEach(card => {
        card.addEventListener('click', () => {



            const content = {
            image: card.dataset.image, // ดึง URL ของภาพจาก data-image
            text: card.dataset.text // ดึงข้อความจาก data-text
            };


            openModal(content); // เปิด modal พร้อมข้อมูล
        });
    });

    // ปิด modal เมื่อคลิกที่ overlay
    overlay.addEventListener('click', () => {
        const modals = document.querySelectorAll('.modal.active');
        modals.forEach(modal => {
            closeModal(modal);
        });
    });


    
}

run();

