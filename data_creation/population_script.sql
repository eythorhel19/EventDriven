INSERT INTO home_country (name, phone_country_code) VALUES ('Iceland', '354');

INSERT INTO home_state (country_id, name) VALUES (3, 'Hofudborgarsvaedid');

INSERT INTO home_city (state_id, name) VALUES (4, 'Reykjavik');
INSERT INTO home_city (state_id, name) VALUES (4, 'Kopavogur');

INSERT INTO home_location (city_id, name, capacity) VALUES (4, 'Laugardalsvollur', 10000);
INSERT INTO home_location (city_id, name, capacity) VALUES (4, 'Harpan', 2000);
INSERT INTO home_location (city_id, name, capacity) VALUES (4, 'Origo Hollin', 2000);
INSERT INTO home_location (city_id, name, capacity) VALUES (5, 'Korinn', 15000);

INSERT INTO home_postalcode (postal_code, city_id, country_id, description) VALUES ('104', 4, 3, 'Laugardalur');
INSERT INTO home_postalcode (postal_code, city_id, country_id, description) VALUES ('101', 4, 3, 'Miðborg');
INSERT INTO home_postalcode (postal_code, city_id, country_id, description) VALUES ('203', 5, 3, 'Hvorf og Korar');

INSERT INTO events_event (title, description, maximum_capacity, start_date, end_date, location_id) VALUES ('Coachella', 'The festival you cannot miss!', 25000, '2022-06-14', '2022-06-14', 4);

INSERT INTO events_eventimage(image_url, event_id, description, main) VALUES ('https://coinlive.me/wp-content/uploads/2022/02/Coachella-Music-Festival-opens-for-NFT-sale.jpg', 1, 'Coachella Stage', true);