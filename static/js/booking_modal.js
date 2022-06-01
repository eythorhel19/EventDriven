let eventData;
let postData = {};
let countryData;
let cityData;

const sourceParts = window.location.href.split('/');
const BASE_URL = sourceParts[0] + '//' + sourceParts[2];

// Requests

async function getEventData(eventID) {
    const url = BASE_URL + "/api/event/" + eventID;
    const res = await fetch(url);

    if (res.status != 200) {
        return;
    }
    const data = await res.json();
    return data;
}

async function getCountryData() {
    const url = BASE_URL + "/api/country";
    const res = await fetch(url);

    if (res.status != 200) {
        return;
    }
    const data = await res.json();
    return data;
}

async function getCityData(countryID) {
    const url = BASE_URL + "/api/city?country_id=" + countryID;
    const res = await fetch(url);

    if (res.status != 200) {
        return;
    }
    const data = await res.json();
    return data;
}

function populateEventData(eventData) {
    document.getElementById("booking_modal_image").src = eventData.main_image_url;
    document.getElementById("booking_modal_title").textContent = eventData.title;
    document.getElementById("booking_modal_description").textContent = eventData.description;
    document.getElementById("booking_modal_location").textContent = eventData.location_name;
    document.getElementById("booking_modal_date").textContent = eventData.date_description;

    const select = document.getElementById("ticket_type_select");
    select.innerHTML = "";
    for (let i = 0; i<eventData.ticket_types.length; i++) {
        let option = document.createElement('option');
        option.value = eventData.ticket_types[i].ticket_type_id;
        option.textContent = eventData.ticket_types[i].option_description;
        select.appendChild(option);
    }
}

function startLoading(loadingTag, contentTag) {
    displayContentPage(-1);
    document.getElementById('booking_modal_loading').style.display = 'flex';
}

function stopLoading(loadingTag, contentTag) {
    document.getElementById('booking_modal_loading').style.display = 'none';
}

function showErrorMessage(message) {
    const errorWrapperTag = document.getElementById('booking_modal_error_wrapper');
    const errorMessageTag = document.getElementById('booking_modal_error_message');
    errorMessageTag.textContent = message;
    errorWrapperTag.style.display = "flex";
}

function closeErrorMessage() {
    const errorWrapperTag = document.getElementById('booking_modal_error_wrapper');
    const errorMessageTag = document.getElementById('booking_modal_error_message');
    errorMessageTag.textContent = "";
    errorWrapperTag.style.display = "none";
}

function setProgressPoint(index) {
    const numberOfPoints = document.getElementById('progress_points_wrapper').children.length;

    for (let i = 1; i<numberOfPoints + 1; i++) {
        const id = 'booking_modal_pp_' + String(i);
        
        // Setting default state
        document.getElementById(id).className = "progress_point";
        
        if (index > i) {
            document.getElementById(id).classList.add('finished');
        } else if (index == i) {
            document.getElementById(id).classList.add('active');
        }
    }
}


// Content Switchers

function displayContentPage(index) {
    const numberOfPoints = document.getElementById('progress_points_wrapper').children.length;

    setProgressPoint(index);

    if (index < 3 || index >= 5) {
        hideInfoBar();
    } else {
        displayInfoBar();
    }

    for (let i = 1; i<numberOfPoints + 3; i++) {
        const id = 'booking_modal_content_' + String(i);

        // Setting default state
        if (index === i) {
            document.getElementById(id).style.display = 'flex';
        } else {
            document.getElementById(id).style.display = 'none';            
        }
        
    }
}

function displayInfoBar() {
    document.getElementById('booking_modal_order_info').style.display = 'flex';

    document.getElementById('booking_modal_order_info_event').textContent = eventData.title;
    document.getElementById('booking_modal_order_info_date').textContent = eventData.date_description;
    document.getElementById('booking_modal_order_info_quantity').textContent = postData.ticket_quantity;
    document.getElementById('booking_modal_order_info_delivery').textContent = postData.delivery_method_description;

    let ticketType = '';
    let totalPrice = 0;

    for (let i = 0; i<eventData.ticket_types.length; i++) {
        if (eventData.ticket_types[i].ticket_type_id === postData.ticket_type_id) {
            ticketType = eventData.ticket_types[i].description;
            totalPrice = eventData.ticket_types[i].price * postData.ticket_quantity;
        }
    }

    document.getElementById('booking_modal_order_info_ticket_type').textContent = ticketType;
    document.getElementById('booking_modal_order_info_total_price').textContent = totalPrice;
}

function hideInfoBar() {
    document.getElementById('booking_modal_order_info').style.display = 'none';
}

async function populatePostalCity() {
    const countryID = document.getElementById("booking_modal_p_country").value;

    cityData = await getCityData(countryID);

    cityData.sort((a, b) => {
        return a.name > b.name;
    })

    const citySelect = document.getElementById("booking_modal_p_city");
    citySelect.disabled = false;
    citySelect.innerHTML = "";
    for (let i = 0; i<cityData.length; i++) {
        let option = document.createElement('option');
        option.value = cityData[i].id;
        option.textContent = cityData[i].name;
        citySelect.appendChild(option);
    }

    if (document.getElementById('booking_modal_p_phone_country_code').value == "") {
        document.getElementById('booking_modal_p_phone_country_code').value = countryID;
    }
}

function populationPostalInfo(countryData) {
    const countrySelect = document.getElementById("booking_modal_p_country");
    countrySelect.innerHTML = "<option disabled selected value> -- Select an option -- </option>";

    for (let i = 0; i<countryData.length; i++) {
        let option = document.createElement('option');
        option.value = countryData[i].id;
        option.textContent = countryData[i].name;
        countrySelect.appendChild(option);
    }

    const phoneCountrySelect = document.getElementById("booking_modal_p_phone_country_code");

    phoneCountrySelect.innerHTML = "<option disabled selected value> -- Select an option -- </option>";

    for (let i = 0; i<countryData.length; i++) {
        let option = document.createElement('option');
        option.value = countryData[i].id;
        option.textContent = countryData[i].name + " (+" + countryData[i].phone_country_code + ")";
        phoneCountrySelect.appendChild(option);
    }

}

async function displayPostalInfo() {
    displayContentPage(3);
    document.getElementById('booking_modal_content_3_p').style.display = 'flex';
    document.getElementById('booking_modal_content_3_e').style.display = 'none';

    countryData = await getCountryData();

    // Sorting the country data
    countryData = countryData.sort((a, b) => {
        return a.name > b.name;
    })

    populationPostalInfo(countryData);
}

function populateEmailInfo(countryData) {
    const select = document.getElementById("booking_modal_e_phone_country_code");
    select.innerHTML = "<option disabled selected value> -- Select an option -- </option>";
    for (let i = 0; i<countryData.length; i++) {
        let option = document.createElement('option');
        option.value = countryData[i].id;
        option.textContent = countryData[i].name + " (+" + countryData[i].phone_country_code + ")";
        select.appendChild(option);
    }
}

async function displayEmailInfo() {
    
    setProgressPoint(2);
    startLoading();

    countryData = await getCountryData();

    // Sorting the country data
    countryData = countryData.sort((a, b) => {
        return a.name > b.name;
    })

    populateEmailInfo(countryData);

    stopLoading();
    
    displayContentPage(3);
    document.getElementById('booking_modal_content_3_e').style.display = 'flex';
    document.getElementById('booking_modal_content_3_p').style.display = 'none';
}

function formatCardNumber(cardNumber) {
    let ret_str = "";

    for (let i = 0; i<cardNumber.length; i++) {
        ret_str += cardNumber[i];
        if ((i + 1) % 4 == 0 && i !== 15) {
            ret_str += '-';
        }
    }

    return ret_str;
}

function displayConfimationPage() {
    displayContentPage(5);

    // Event Info
    document.getElementById('booking_modal_confirm_event_title').textContent = eventData.title;
    document.getElementById('booking_modal_confirm_location').textContent = eventData.location_name;
    document.getElementById('booking_modal_confirm_date').textContent = eventData.date_description;
    
    document.getElementById('booking_modal_confirm_delivery_method').textContent = 'Via ' + postData.delivery_method_description;
    const deliveryDetails =  document.getElementById('booking_modal_confirm_delivery_details');
    deliveryDetails.innerHTML = "";

    
    // Delivery Info
    if (postData.delivery_method == 'P') {

        console.log(postData.postal_delivery_info);

        const nameTag = document.createElement('p');
        nameTag.textContent = postData.postal_delivery_info.first_name + ' ' + postData.postal_delivery_info.last_name;
        nameTag.classList.add('p_light');
        deliveryDetails.appendChild(nameTag);

        let countryCode = '';
        let countryName = '';
        for (let i = 0; i<countryData.length; i++) {
            if (countryData[i].id === postData.postal_delivery_info.phone_country) {
                countryCode = countryData[i].phone_country_code;
            }
            if (countryData[i].id === postData.postal_delivery_info.country_id) {
                countryName = countryData[i].name;
            }
        }

        const phoneTag = document.createElement('p');
        phoneTag.textContent = '+' + countryCode + ' ' + postData.postal_delivery_info.phone_number;
        phoneTag.classList.add('p_light');
        deliveryDetails.appendChild(phoneTag);

        const streetNameTag = document.createElement('p');
        streetNameTag.textContent = postData.postal_delivery_info.street_name + ' ' + postData.postal_delivery_info.house_number;
        streetNameTag.classList.add('p_light');
        deliveryDetails.appendChild(streetNameTag);

        let cityName = '';
        for (let i = 0; i<cityData.length; i++) {
            if (cityData[i].id === postData.postal_delivery_info.city_id) {
                cityName = cityData[i].name;
            }
        }

        const cityCountryTag = document.createElement('p');
        cityCountryTag.textContent = postData.postal_delivery_info.postal_code + " " + cityName + ', ' + countryName;
        cityCountryTag.classList.add('p_light');
        deliveryDetails.appendChild(cityCountryTag);

    } else if (postData.delivery_method == 'E') {
        const nameTag = document.createElement('p');
        nameTag.textContent = postData.email_delivery_info.first_name + ' ' + postData.email_delivery_info.last_name;
        nameTag.classList.add('p_light');
        deliveryDetails.appendChild(nameTag);

        const emailTag = document.createElement('p');
        emailTag.textContent = postData.email_delivery_info.email;
        emailTag.classList.add('p_light');
        deliveryDetails.appendChild(emailTag);

        let countryCode = '';
        for (let i = 0; i<countryData.length; i++) {
            if (countryData[i].id === postData.email_delivery_info.phone_country) {
                countryCode = countryData[i].phone_country_code;
            }
        }

        const phoneTag = document.createElement('p');
        phoneTag.textContent = '+' + countryCode + ' ' + postData.email_delivery_info.phone_number;
        phoneTag.classList.add('p_light');
        deliveryDetails.appendChild(phoneTag);
    }

    // Payment Info
    document.getElementById('booking_modal_confirm_card_name').textContent = postData.paymentInfo.name_on_card;
    document.getElementById('booking_modal_confirm_card_number').textContent = formatCardNumber(postData.paymentInfo.card_number);
    document.getElementById('booking_modal_confirm_expiration_date').textContent = postData.paymentInfo.expiration_date;
    document.getElementById('booking_modal_confirm_cvc').textContent = postData.paymentInfo.cvc;

    // Amount
    let ticketType = '';
    let ticketPrice;
    let totalPrice;

    for (let i = 0; i<eventData.ticket_types.length; i++) {
        if (eventData.ticket_types[i].ticket_type_id === postData.ticket_type_id) {
            ticketType = eventData.ticket_types[i].description;
            ticketPrice = eventData.ticket_types[i].price;
            totalPrice = eventData.ticket_types[i].price * postData.ticket_quantity;
        }
    }

    document.getElementById('booking_modal_confirm_ticket_type').textContent = ticketType;
    document.getElementById('booking_modal_confirm_quantity').textContent = postData.ticket_quantity;
    document.getElementById('booking_modal_confirm_ticket_price').textContent = ticketPrice;
    document.getElementById('booking_modal_confirm_total_price').textContent = totalPrice;
}

function displayErrorPage(message) {
    document.getElementById('booking_modal_fail_message').textContent = message;
    displayContentPage(7);
}

// Handler Functions

async function handleBookNow(eventID) {
    // Initilizing
    closeErrorMessage();
    eventData = undefined;
    postData = {};

    // Start loading
    startLoading();

    // Getting event data
    eventData = await getEventData(eventID);

    // Populating Booking Modal
    populateEventData(eventData);

    // Stop loading
    stopLoading();
    displayContentPage(1);
}

function handleDeliveryMethodPage() {
    const ticketAmount = document.getElementById('ticket_amount_entry_field').value;

    if (isNaN(ticketAmount) || ticketAmount == "") {
        showErrorMessage("Please enter a valid integer input as the quantity.");
        return;
    } else if (ticketAmount > 10) {
        showErrorMessage("You can only buy a maximum of 10 tickets.");
        return;
    }

    postData['ticket_quantity'] = Number(ticketAmount);
    postData['ticket_type_id'] = Number(document.getElementById('ticket_type_select').value);
    
    closeErrorMessage();

    displayContentPage(2);
}

function handleDeliveryMethod(chosenMethod) {
    if (chosenMethod == 'postal') {
        postData['delivery_method'] = 'P';
        postData['delivery_method_description'] = 'Postal';
        displayPostalInfo();
        
    } else if (chosenMethod == 'email') {
        postData['delivery_method'] = 'E';
        postData['delivery_method_description'] = 'Email';
        displayEmailInfo();
    }
}

function handleBack(contentPageIndex) {
    displayContentPage(contentPageIndex - 1);
}

function validateEmail(value) {
    if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(value)) {
        return true;
    }
    return false;
}

function autoFillNameOnCard(firstName, lastName) {
    const nameOnCard = document.getElementById('booking_modal_name_on_card');
    if (nameOnCard.value.length === 0) {
        nameOnCard.value = firstName + ' ' + lastName;
    }
}

function handleSavePostDeliveryInfo() {
    closeErrorMessage();

    const countryID = document.getElementById('booking_modal_p_country').value;
    if (isNaN(countryID)) {
        showErrorMessage('Please enter a valid country ID.');
        return;
    }

    const cityID = document.getElementById('booking_modal_p_city').value;
    if (isNaN(cityID)) {
        showErrorMessage('Please enter a valid city ID.');
        return;
    }

    const postalCode = document.getElementById('booking_modal_p_postal_code').value;
    if (postalCode.length > 16) {
        showErrorMessage('Please enter a valid postal code.');
        return;
    }

    const streetName = document.getElementById('booking_modal_p_street_name').value;
    if (streetName == '') {
        showErrorMessage('Please enter the street name.')
        return;
    }

    const houseNumber = document.getElementById('booking_modal_p_house_number').value;
    if (isNaN(houseNumber)) {
        showErrorMessage('Please enter a valid house number. House number should only include digits.');
        return;
    }

    const firstName = document.getElementById('booking_modal_p_first_name').value;
    if (firstName == '') {
        showErrorMessage('Please enter your first name.');
        return;
    }

    const lastName = document.getElementById('booking_modal_p_last_name').value;
    if (lastName == '') {
        showErrorMessage('Please enter your last name.');
        return;
    }

    const phoneCountry = document.getElementById('booking_modal_p_phone_country_code').value;
    if (isNaN(phoneCountry)) {
        showErrorMessage('Please enter a valid phone country code.');
        return;
    }

    const phoneNumber = document.getElementById('booking_modal_p_phone_number').value;
    if (phoneNumber == '') {
        showErrorMessage('Please enter your phone number.')
        return;
    } else if (isNaN(phoneNumber)) {
        showErrorMessage('Please enter a valid phone number. It should only include digits.')
        return;
    }

    const email = document.getElementById('booking_modal_p_email').value;
    if (!validateEmail(email)) {
        showErrorMessage('Please enter a valid email address.');
        return;
    }

    postData['postal_delivery_info'] = {
        'country_id': Number(countryID),
        'city_id': Number(cityID),
        'postal_code': postalCode,
        'street_name': streetName,
        'house_number': Number(houseNumber),
        'first_name': firstName,
        'last_name': lastName,
        'phone_country': Number(phoneCountry),
        'phone_number': Number(phoneNumber),
        'email': email
    }

    autoFillNameOnCard(firstName, lastName);

    displayContentPage(4);
}

function handleSaveEmailDeliveryInfo() {
    closeErrorMessage();

    const firstName = document.getElementById('booking_modal_e_first_name').value;
    if (firstName == '') {
        showErrorMessage('Please enter your first name.');
        return;
    }

    const lastName = document.getElementById('booking_modal_e_last_name').value;
    if (lastName == '') {
        showErrorMessage('Please enter your last name.');
        return;
    }

    const email = document.getElementById('booking_modal_e_email').value;
    if (!validateEmail(email)) {
        showErrorMessage('Please enter a valid email address.');
        return;
    }

    const phoneCountry = Number(document.getElementById('booking_modal_e_phone_country_code').value);
    if (phoneCountry == 0) {
        showErrorMessage('Please select the phone country code.');
        return;
    }
    else if (isNaN(phoneCountry)) {
        showErrorMessage('Please enter a valid phone country code.');
        return;
    }

    const phoneNumber = document.getElementById('booking_modal_e_phone_number').value;

    if (phoneNumber == '') {
        showErrorMessage('Please enter your phone number.')
        return;
    } else if (isNaN(phoneNumber)) {
        showErrorMessage('Please enter a valid phone number. It should only include digits.')
        return;
    }

    postData['email_delivery_info'] = {
        'first_name': firstName,
        'last_name': lastName,
        'email': email,
        'phone_country': phoneCountry,
        'phone_number': Number(phoneNumber)
    }

    autoFillNameOnCard(firstName, lastName);

    displayContentPage(4);
}

function validateExpirationDate(exDate) {
    dateSplit = exDate.split('/');
    if (dateSplit.length !== 2) {
        return false;
    } else if (dateSplit[0].length !== 2 || dateSplit[1].length !== 2) {
        return false;
    } else if (isNaN(dateSplit[0]) || isNaN(dateSplit[1])) {
        return false;
    } else if (1 > Number(dateSplit[0]) || Number(dateSplit[0]) > 12) {
        return false;
    } else if (0 > Number(dateSplit[1]) || Number(dateSplit[1]) > 99) {
        return false;
    }

    const today = new Date();
    const expirationDate = new Date('20' + dateSplit[1] + '-' + dateSplit[0] + '-1')

    if (expirationDate <= today) {
        return false;
    }

    return true;
}

function validateCVC(cvc) {
    if (cvc.length !== 3) {
        return false;
    } else if (isNaN(cvc)) {
        return false;
    }
    return true;
}

function validateCardNumber(cardNumber) {
    if (cardNumber.length !== 16) {
        return false;
    } else if (isNaN(cardNumber)) {
        return false;
    }
    return true;
}

function handleSavePaymentInfo() {
    closeErrorMessage();

    const nameOnCard = document.getElementById('booking_modal_name_on_card').value;

    if (nameOnCard.length < 4) {
        showErrorMessage('Please enter a valid name on the card.')
        return;
    }

    const cardNumber = document.getElementById('booking_modal_card_number').value.replaceAll('-', '');

    if (!validateCardNumber(cardNumber)) {
        showErrorMessage('Please enter a valid card number. The card number should only include digits.')
        return;
    }

    const expirationDate = document.getElementById('booking_modal_expiration_date').value;

    if (!validateExpirationDate(expirationDate)) {
        showErrorMessage('Please enter the valid expiration date in the following format MM/YY.')
        return;
    }

    const cvc = document.getElementById('booking_modal_cvc').value;

    if (!validateCVC(cvc)) {
        showErrorMessage('Please enter a valid CVC number, a CVC number should only include 3 digits.')
        return;
    }

    postData['paymentInfo'] = {
        'name_on_card': nameOnCard,
        'card_number': cardNumber,
        'expiration_date': expirationDate,
        'cvc': cvc
    }

    displayConfimationPage();
}

async function handlePostBooking(e) {
    e.preventDefault();
    
    startLoading();

    const token = $('input[name="csrfmiddlewaretoken"]').val();
    
    // Formating for post

    let patchBody;
    if (postData.delivery_method == 'E') {
        patchBody = {
            'ticket_type_id': postData.ticket_type_id,
            'event_id': eventData.id,
            'delivery_method': postData.delivery_method,
            'email': postData.email_delivery_info.email,
            'first_name': postData.email_delivery_info.first_name,
            'last_name': postData.email_delivery_info.last_name,
            'quantity': postData.ticket_quantity,
            'phone_country': postData.email_delivery_info.phone_country,
            'phone_number': postData.email_delivery_info.phone_number
        };
    } else if (postData.delivery_method == 'P') {
        patchBody = {
            'ticket_type_id': postData.ticket_type_id,
            'event_id': eventData.id,
            'delivery_method': postData.delivery_method,
            'email': postData.postal_delivery_info.email,
            'first_name': postData.postal_delivery_info.first_name,
            'last_name': postData.postal_delivery_info.last_name,
            'street_name': postData.postal_delivery_info.street_name,
            'house_number': postData.postal_delivery_info.house_number,
            'postal_code': postData.postal_delivery_info.postal_code,
            'quantity': postData.ticket_quantity,
            'phone_country': postData.postal_delivery_info.phone_country,
            'phone_number': postData.postal_delivery_info.phone_number
        };
    }

    // Booking tickets
    const url = BASE_URL + "/api/booktickets";
    const res = await fetch(url, {
        method: "PATCH",
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': token
        },
        body: JSON.stringify(patchBody)
    })

    stopLoading();

    if (res.status != 200) {
        const data = await res.json();
        displayErrorPage(data['message'])
    } else {
        displayContentPage(6);
    }

    return false;
}