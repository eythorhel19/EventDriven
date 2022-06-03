function showHelp() {
    const helpTags = document.getElementsByClassName('helptext');

    for (let i = 0; i<helpTags.length; i++) {
        if (helpTags[i].style.display == 'block') {
            helpTags[i].style.display = 'none';
        } else {
            helpTags[i].style.display = 'block';
        }
    }
}