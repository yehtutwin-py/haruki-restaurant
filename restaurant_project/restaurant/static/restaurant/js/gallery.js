const rawPhotos     = JSON.parse(document.getElementById('gallery-data').textContent);
const galleryPhotos = rawPhotos.map(photo => ({
    src:   '/media/' + photo.image,
    title: photo.title || ''
}));

let currentIndex = 0;

function openLightbox(index) {
    currentIndex = index;
    updateLightbox();
    document.getElementById('lightbox').classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeLightbox() {
    document.getElementById('lightbox').classList.remove('active');
    document.body.style.overflow = '';
}

function closeLightboxOnBg(event) {
    if (event.target === document.getElementById('lightbox')) {
        closeLightbox();
    }
}

function updateLightbox() {
    const photo = galleryPhotos[currentIndex];
    document.getElementById('lightbox-img').src             = photo.src;
    document.getElementById('lightbox-caption').textContent = photo.title;
}

function nextPhoto(event) {
    event.stopPropagation();
    currentIndex = (currentIndex + 1) % galleryPhotos.length;
    updateLightbox();
}

function prevPhoto(event) {
    event.stopPropagation();
    currentIndex = (currentIndex - 1 + galleryPhotos.length) % galleryPhotos.length;
    updateLightbox();
}

document.addEventListener('keydown', function(e) {
    const lightbox = document.getElementById('lightbox');
    if (!lightbox.classList.contains('active')) return;
    if (e.key === 'ArrowRight') nextPhoto(e);
    if (e.key === 'ArrowLeft')  prevPhoto(e);
    if (e.key === 'Escape')     closeLightbox();
});

document.querySelectorAll('.gallery-item').forEach(function(item) {
    item.addEventListener('click', function() {
        openLightbox(parseInt(this.dataset.index));
    });
});