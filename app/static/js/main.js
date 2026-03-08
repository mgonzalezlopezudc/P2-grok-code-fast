// app/static/js/main.js

const socket = io();

socket.on('price_change', (data) => {
    // Update prices
    data.forEach(item => {
        const priceElements = document.querySelectorAll(`.js-price[data-product="${item.id}"]`);
        priceElements.forEach(el => el.textContent = `$${item.price}`);
    });
    showToast('Price updated', 'success');
});

socket.on('low_stock_001', (data) => {
    showToast('Low stock in Store 001', 'warning');
});

socket.on('low_stock_002', (data) => {
    showToast('Low stock in Store 002', 'warning');
});

socket.on('low_stock_003', (data) => {
    showToast('Low stock in Store 003', 'warning');
});

socket.on('low_stock_004', (data) => {
    showToast('Low stock in Store 004', 'warning');
});

function showToast(message, type) {
    const colors = {
        success: '#28a745',
        warning: '#ffc107',
        error: '#dc3545',
        info: '#17a2b8'
    };
    Toastify({
        text: message,
        duration: 3000,
        gravity: "top",
        position: "right",
        backgroundColor: colors[type] || colors.info,
    }).showToast();
}