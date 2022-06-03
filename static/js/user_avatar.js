function displayUserOptions() {
    const tag = document.getElementById('user_avatar_option_wrapper');

    if (tag.style.display === 'flex') {
        tag.style.display = 'none';
    } else {
        tag.style.display = 'flex';
    }
}