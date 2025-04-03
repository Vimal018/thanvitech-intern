const imageZoomContainer = document.querySelector('.image-zoom-container');
const imageZoom = document.querySelector('.image-zoom');
const zoomOverlay = document.querySelector('.zoom-overlay');

imageZoomContainer.addEventListener('mousemove', (event) => {
    const containerRect = imageZoomContainer.getBoundingClientRect();
    const x = ((event.clientX - containerRect.left) / containerRect.width) * 100;
    const y = ((event.clientY - containerRect.top) / containerRect.height) * 100;

    imageZoom.style.transformOrigin = `${x}% ${y}%`;
});

imageZoomContainer.addEventListener('mouseenter', () => {
    zoomOverlay.style.opacity = '1';
});

imageZoomContainer.addEventListener('mouseleave', () => {
    zoomOverlay.style.opacity = '0';
});