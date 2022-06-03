SELECT 
    E.id, 
    E.title, 
    E.description, 
    E.start_date, 
    E.end_date, 
    CONCAT(L.name,', ',C.name) AS location_name, 
    E.main_image_url
FROM 
    EVENTS_EVENT AS E
    JOIN HOME_LOCATION AS L
    ON E.location_id = L.id
    JOIN HOME_CITY AS C
    ON L.city_id = C.id
WHERE 
    E.id = {event_id};