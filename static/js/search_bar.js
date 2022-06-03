let button_bool = false;

function button_bool_true() {
    button_bool = true;
}

function search(ele) {
    if (event.key === "Enter") {
        button_bool_true();
        sendSearchAsParam(ele);
    }
}

function sendSearchAsParam(form) {
    if (button_bool === true) {
        const getUrl = window.location;
        const baseUrl = getUrl.protocol + "//" + getUrl.host + "/" + "search";
        const url = new URL(baseUrl);

        // Category
        url.searchParams.append(
            "categories",
            form.elements.categories.value
        );

        // Dates
        if (form.elements.chosen_date_range_type.value === "") {
            url.searchParams.append("date_to", "All");
            url.searchParams.append("date_from", "All");
        } else if (
            form.elements.chosen_date_range_type.value === "today"
        ) {
            let yourDate = new Date();
            const offset = yourDate.getTimezoneOffset();
            yourDate = new Date(
                yourDate.getTime() - offset * 60 * 1000
            );
            const theDate = yourDate.toISOString().split("T")[0];

            url.searchParams.append("date_to", theDate);
            url.searchParams.append("date_from", theDate);
        } else if (
            form.elements.chosen_date_range_type.value === "this week"
        ) {
            let yourDate = new Date();
            const offset = yourDate.getTimezoneOffset();
            yourDate = new Date(
                yourDate.getTime() - offset * 60 * 1000
            );

            const yourDateISO = yourDate.toISOString().split("T")[0];
            url.searchParams.append("date_from", yourDateISO);

            const firstDay = new Date(yourDateISO);
            const theDate = new Date(
                firstDay.getTime() + 7 * 24 * 60 * 60 * 1000
            );
            const theDateIso = theDate.toISOString().split("T")[0];
            url.searchParams.append("date_to", theDateIso);
        } else if (
            form.elements.chosen_date_range_type.value === "specific date"
        ) {
            if (form.elements.date_from.value !== "" && form.elements.date_to.value !== "") {
                url.searchParams.append(
                    "date_to",
                    form.elements.date_to.value
                );

                url.searchParams.append(
                    "date_from",
                    form.elements.date_from.value
                );
            } else if (form.elements.date_from.value !== "") {
                url.searchParams.append(
                    "date_from",
                    form.elements.date_from.value
                )
            } else if (form.elements.date_to.value !== "") {
                url.searchParams.append(
                    "date_to",
                    form.elements.date_to.value
                );
            }
        }

        // Search Input
        if (form.elements.search_input_field.value !== "") {
            url.searchParams.append(
                "search_input_field",
                form.elements.search_input_field.value
            );
        } else {
            url.searchParams.append("search_input_field", "All");
        }

        window.location.replace(url.href);
    }
}

function isItSpecificDate(form) {
    if (form.value === "specific date") {
        const theInputField = document.getElementById("date_to_div");
        const theInputField2 = document.getElementById("date_from_div");
        const theSelectField = document.getElementById("chosen_date_range_type");
        theInputField.style.display = "flex";
        theInputField2.style.display = "flex";
        theSelectField.style.display = "none";
    } else {
        return false;
    }
}

function populateSearchBar() {
    const url = window.location.search;
    const urlParams = new URLSearchParams(url);

    const categories = urlParams.get('categories');

    if (categories !== null) {
        document.getElementById('categories').value = categories;
    }

    const dateTo = urlParams.get('date_to');
    const dateFrom = urlParams.get('date_from');

    const todayDate = new Date();
    const today = todayDate.toISOString().split("T")[0];
    const afterWeekDay = new Date(
        todayDate.getTime() + 7 * 24 * 60 * 60 * 1000
    ).toISOString().split("T")[0];

    if (dateTo === 'All' && dateFrom === 'All') {
        // pass
    } else if (dateTo === null && dateFrom === null) {
        // pass
    } else if (dateFrom === today && dateTo === today) {
        document.getElementById('chosen_date_range_type').value = 'today';
    } else if (dateFrom === today && dateTo === afterWeekDay) {
        document.getElementById('chosen_date_range_type').value = 'this week';
    } else {
        document.getElementById('chosen_date_range_type').value = 'specific date';
        isItSpecificDate({'value': 'specific date'});

        if (dateFrom !== null) {
            document.getElementById('date_from').value = dateFrom;
        }

        if (dateTo !== null) {
            document.getElementById('date_to').value = dateTo;
        }
    }

    const searchInputField = urlParams.get('search_input_field');

    if (searchInputField !== 'All') {
        document.getElementById('search_input_field').value = searchInputField;
    }
}