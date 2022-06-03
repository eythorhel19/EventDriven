const sourceParts2 = window.location.href.split("/");
const BASE_URL2 = sourceParts2[0] + "//" + sourceParts2[2];

$(document).ready(function () {
    $(".js-example-basic-multiple").select2();
});

async function funcForNewEventsCategories(event) {
    event.preventDefault();

    const token = $('input[name="csrfmiddlewaretoken"]').val();

    const url = BASE_URL2 + "/api/event_categories";

    const res = await fetch(url, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": token,
        },
        body: JSON.stringify({
            event_id: sourceParts[5],
            event_categories: $("#event_categories").select2(
                "data"
            ),
        }),
    });

    return res.status === 200;
}
async function funcForNewEventsEntertainers(event) {
    event.preventDefault();

    const token = $('input[name="csrfmiddlewaretoken"]').val();

    const url = BASE_URL2 + "/api/event_entertainers";

    const res = await fetch(url, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": token,
        },
        body: JSON.stringify({
            event_id: sourceParts[5],
            event_entertainers: $("#event_entertainers").select2(
                "data"
            ),
        }),
    });

    return res.status === 200;
}