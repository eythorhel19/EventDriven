const params = new URLSearchParams(window.location.search);
if (params.get('success') == 'true') {
    document.body.scrollTop = 1000; // For Safari
    document.documentElement.scrollTop = 1000; // For Chrome, Firefox, IE and Opera
}

document.getElementById('id_postal_country').addEventListener('change', function() {
    document.getElementById("detailed_info_form").submit(); 
});