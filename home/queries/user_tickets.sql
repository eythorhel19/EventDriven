SELECT 
    HT.*, 
    EEVE.title AS event_title, 
    EEVE.start_date AS event_start_date, 
	EEVE.main_image_url, 
	HLOC.name AS event_location_name
FROM 
	HOME_TICKET AS HT
	JOIN EVENTS_EVENT AS EEVE
	ON HT.event_id = EEVE.id
	JOIN HOME_LOCATION AS HLOC
	ON HLOC.id = EEVE.location_id
WHERE 
	HT.user_id = {user_id};