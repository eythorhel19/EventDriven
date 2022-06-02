let imageIndex = 0;
let images = [];
let imagesHaveBeenFetched = false;

function getImages() {
    const imageTags = document.getElementsByClassName('event_image_url');

    for (let img of imageTags) {
        images.push(img.innerText);
    }

    imagesHaveBeenFetched = true;
}

function loadNextImage() {
    if (!imagesHaveBeenFetched) {
        getImages();
    }

    if (images.length > 0) {
        imageIndex++;
        if (imageIndex === images.length) {
            imageIndex = 0;
        }
        
        document.getElementById('event_current_image').src = images[imageIndex];
    }
}

function loadPrevImage() {
    if (!imagesHaveBeenFetched) {
        getImages();
    }

    if (images.length > 0) {
        if (imageIndex == 0) {
            imageIndex = images.length - 1;
        } else {
            imageIndex--;
        }
    
        document.getElementById('event_current_image').src = images[imageIndex];
    }
}