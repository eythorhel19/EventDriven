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

INSERT INTO events_event (title, description, maximum_capacity, start_date, end_date, location_id, main_image_url) VALUES 
(
    'Coachella', 
    'The festival you cannot miss!', 
    25000, 
    '2022-06-14', 
    '2022-06-14', 
    4,
    'https://coinlive.me/wp-content/uploads/2022/02/Coachella-Music-Festival-opens-for-NFT-sale.jpg'
),
(
    'Skepta', 
    'Skepta is bringing the british grime to Iceland.', 
    5000, 
    '2022-07-1', 
    '2022-07-1', 
    4,
    'https://i.guim.co.uk/img/media/05d40829197a54e67e8bde4bcaffe35d5da1fe46/0_250_3414_2048/master/3414.jpg?width=465&quality=45&auto=format&fit=max&dpr=2&s=7d23a70263bfc696fa3dd09aba7c778c'
);

INSERT INTO events_eventimage(image_url, event_id, description, main) VALUES ('https://coinlive.me/wp-content/uploads/2022/02/Coachella-Music-Festival-opens-for-NFT-sale.jpg', 1, 'Coachella Stage', true);
INSERT INTO events_eventimage(image_url, event_id, description, main) VALUES ('https://cdn.tix.is/tix/EventImages/Event_13188.jpg?cache=637871210889600000', 2, 'Skepta', true);

INSERT INTO home_category (name) VALUES 
('Rap'), 
('Rock'), 
('Hip-Hop'), 
('Pop'), 
('Jazz'), 
('Classical'), 
('Country'), 
('Electronic'), 
('House'), 
('Rave'), 
('Indie Rock');

INSERT INTO entertainers_entertainer (name, description, image_url) VALUES 
(
    '21 Savage', 
    'Shéyaa Bin Abraham-Joseph, known professionally as 21 Savage, is a rapper based in Atlanta, Georgia, United States. Born in London, he moved to Atlanta with his mother at age seven.', 
    'https://i.guim.co.uk/img/media/812da1e53127011a8adb395045c69722305dbef6/0_0_1548_929/master/1548.jpg?width=1200&height=1200&quality=85&auto=format&fit=crop&s=cc4234292c2af1e002d63389c0f99b59'
),
(
    'Drake', 
    'Aubrey Drake Graham[5] (born October 24, 1986) is a Canadian rapper, singer-songwriter, and actor.[6] Gaining recognition by starring as Jimmy Brooks in the CTV teen drama series Degrassi: The Next Generation (2001–08), Drake pursued a career in music releasing his debut mixtape Room for Improvement in 2006.', 
    'https://i.guim.co.uk/img/media/812da1e53127011a8adb395045c69722305dbef6/0_0_1548_929/master/1548.jpg?width=1200&height=1200&quality=85&auto=format&fit=crop&s=cc4234292c2af1e002d63389c0f99b59'
),
(
    'Ariana Grande',
    'Ariana Grande-Butera is an American singer, songwriter, and actress. Her four-octave vocal range has received critical acclaim, and her personal life has been the subject of widespread media attention.',
    'https://assets.teenvogue.com/photos/613b5fd248eda7f19679403c/4:3/w_1999,h_1499,c_limit/1235152164'
),
(
    'Travis Scott',
    'Jacques Bermon Webster II, better known by his stage name Travis Scott, is an American rapper, singer, songwriter, and record producer. His stage name is the namesake of a favorite uncle combined with the first name of one of his inspirations, Kid Cudi.',
    'https://static.hiphopdx.com/2022/04/travis-scott-utopia-billboards-coachella-1200x675.jpg'
),
(
    'Rihanna',
    'Robyn Rihanna Fenty NH is a Barbadian singer, actress, fashion designer, and businesswoman. Born in Saint Michael and raised in Bridgetown, Barbados, Rihanna was discovered by American record producer Evan Rogers who invited her to the United States to record demo tapes.',
    'https://api.time.com/wp-content/uploads/2018/09/rihanna-barbados-ambassador.jpg'
);

INSERT INTO home_tickettype (description) VALUES 
('Standard'),
('VIP');

INSERT INTO home_eventtickettypeprice (event_id, ticket_type_id, price) VALUES
(1, 1, 100),
(1, 2, 160),
(2, 1, 40),
(2, 2, 60);

