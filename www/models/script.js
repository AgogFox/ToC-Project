// const openModalButtons = document.querySelectorAll('[data-modal-target]')
// const closeModalButtons = document.querySelectorAll('[data-close-button]')
// const overlay = document.getElementById('overlay')

// openModalButtons.forEach(button => {
//   button.addEventListener('click', () => {
//     const modal = document.querySelector(button.dataset.modalTarget)
//     openModal(modal)
//   })
// })

// overlay.addEventListener('click', () => {
//   const modals = document.querySelectorAll('.modal.active')
//   modals.forEach(modal => {
//     closeModal(modal)
//   })
// })

// closeModalButtons.forEach(button => {
//   button.addEventListener('click', () => {
//     const modal = button.closest('.modal')
//     closeModal(modal)
//   })
// })

// function openModal(modal) {
//   if (modal == null) return
//   modal.classList.add('active')
//   overlay.classList.add('active')
// }

// function closeModal(modal) {
//   if (modal == null) return
//   modal.classList.remove('active')
//   overlay.classList.remove('active')
// }

// เลือก card ทุกใบ
const cardItems = document.querySelectorAll('.vehicle-card');
const overlay = document.getElementById('overlay');

// ฟังก์ชันเพื่อสร้าง modal
function createDynamicModal(content) {
    const modal = document.createElement('div');
    modal.classList.add('modal', 'active');

    modal.innerHTML = `
        <div class="modal-header">
            <div class="title">Dynamic Modal</div>
            <button data-close-button class="close-button">&times;</button>
        </div>
        <div class="modal-body">
            <img class="image-car" src="${content.image}" alt="Image">
            <div class="modal-object"> ${content.text}
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
