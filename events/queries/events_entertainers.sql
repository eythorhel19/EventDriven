SELECT
	NE.entertainer_id AS id, 
	NE.name, 
	NE.description, 
	NE.image_url, 
	NE.next_event_id,
	E.start_date AS next_event_date,
	L.name AS location_name
FROM (
	SELECT
		EE.entertainer_id, 
		ENT.name, 
		ENT.description, 
		ENT.image_url, 
		MIN(EE.event_id) AS next_event_id
	FROM 
		HOME_EVENTENTERTAINER AS EE
		-- Getting entertainer info
		JOIN ENTERTAINERS_ENTERTAINER AS ENT
		ON EE.entertainer_id = ENT.id

		-- Getting next event data
		JOIN (
			SELECT
				ENT2.id,
				MIN(EVE.start_date) AS next_event_date
			FROM 
				ENTERTAINERS_ENTERTAINER AS ENT2
				JOIN HOME_EVENTENTERTAINER AS HEE 
				ON ENT2.id = HEE.entertainer_id
				JOIN EVENTS_EVENT AS EVE 
				ON HEE.event_id = EVE.id
			WHERE 
				EVE.start_date >= CURRENT_DATE
			GROUP BY
				ENT2.id
		) AS X
		ON ENT.id = X.id

		-- Getting event_id
		JOIN EVENTS_EVENT AS E2
		ON (EE.event_id = E2.id AND E2.start_date = X.next_event_date)
	WHERE
		ENT.id IN (
			SELECT
				Y.entertainer_id
			FROM
				home_evententertainer AS Y
			WHERE
				Y.event_id = {event_id}
		)
	GROUP BY
		EE.entertainer_id, ENT.name, ENT.description, ENT.image_url
	) AS NE
	JOIN EVENTS_EVENT AS E
	ON NE.next_event_id = E.id
	JOIN HOME_LOCATION AS L
	ON E.location_id = L.id;