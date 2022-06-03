SELECT 
    E.id, 
    E.title, 
    E.description, 
    E.start_date, 
    E.end_date, 
    CONCAT(L.name,', ',C.name) AS location_name, 
    E.main_image_url,
	X.tickets_sold
FROM 
    EVENTS_EVENT AS E
    JOIN HOME_LOCATION AS L
    ON E.location_id = L.id
    JOIN HOME_CITY AS C
    ON L.city_id = C.id
	LEFT JOIN (
		SELECT
			T.event_id,
			COUNT(*) AS tickets_sold
		FROM home_ticket AS T
		WHERE T.status = 'S'
		GROUP BY T.event_id
	) AS X
	ON X.event_id = E.id
WHERE 
    E.id = {event_id};