const sourceParts3 = window.location.href.split("/");
const BASE_URL3 = sourceParts3[0] + "//" + sourceParts3[2];

$(document).ready(function () {
    $(".js-example-basic-multiple").select2();
});

async function funcForUsersFavCatSelected(event) {
    event.preventDefault();

    const token = $('input[name="csrfmiddlewaretoken"]').val();

    const url = BASE_URL3 + "/api/user_categories";
    const res = await fetch(url, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": token,
        },
        body: JSON.stringify({
            users_fav_cat_selected: $("#users_fav_cat_selected").select2(
                "data"
            ),
        }),
    });

    return res.status === 200;
}
async function funcForUsersFavEntSelected(event) {
    event.preventDefault();

    const token = $('input[name="csrfmiddlewaretoken"]').val();

    const url = BASE_URL3 + "/api/user_entertainers";
    const res = await fetch(url, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": token,
        },
        body: JSON.stringify({
            select_entertainers: $("#select_entertainers").select2("data"),
        }),
    });

    return res.status === 200;
}