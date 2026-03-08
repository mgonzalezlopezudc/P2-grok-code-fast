// app/static/js/main.js

const socket = io();

socket.on('price_change', (data) => {
    // Update prices
    data.forEach(item => {
        const priceElements = document.querySelectorAll(`.js-price[data-product="${item.id}"]`);
        priceElements.forEach(el => el.textContent = `$${item.price}`);
    });
    showToast('Price updated', 'info');
});

socket.on('low_stock_001', (data) => {
    showToast('Low stock in Store 001', 'warning');
    // Append to store panel if on store page
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
    // Simple toast
    alert(message); // Placeholder, replace with proper toast
}