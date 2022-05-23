DROP TABLE IF EXISTS UserFavoriteCatagory;
DROP TABLE IF EXISTS EventTicketTypePrice;
DROP TABLE IF EXISTS EventEntertainer;
DROP TABLE IF EXISTS EventCategory;
DROP TABLE IF EXISTS Ticket;
DROP TABLE IF EXISTS TicketType;
DROP TABLE IF EXISTS UserDetails;
DROP TABLE IF EXISTS auth_user;
DROP TABLE IF EXISTS Entertainer;
DROP TABLE IF EXISTS Category;
DROP TABLE IF EXISTS EventImage;
DROP TABLE IF EXISTS Event;
DROP TABLE IF EXISTS PostalCode;
DROP TABLE IF EXISTS Location;
DROP TABLE IF EXISTS City;
DROP TABLE IF EXISTS State;
DROP TABLE IF EXISTS Country;

DROP TYPE IF EXISTS TICKET_STATUS;
CREATE TYPE TICKET_STATUS AS ENUM
('unreleased','released','sold');

DROP TYPE IF EXISTS TICKET_DELIVERY_METHODS;
CREATE TYPE TICKET_DELIVERY_METHODS AS ENUM
('postal', 'electronic');

-- Base Tables

-- Location

CREATE TABLE Country
(
    country_id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    phone_country_code VARCHAR NOT NULL
);

CREATE TABLE State
(
    state_id SERIAL PRIMARY KEY,
    country_id INT REFERENCES Country (country_id),
    name VARCHAR NOT NULL
);

CREATE TABLE City
(
    city_id SERIAL PRIMARY KEY,
    state_id INT REFERENCES State (state_id),
    name VARCHAR NOT NULL
);

CREATE TABLE Location
(
    location_id SERIAL PRIMARY KEY,
    city_id INT REFERENCES City (city_id),
    name VARCHAR NOT NULL
);

-- Address

CREATE TABLE PostalCode
(
    postal_code_id SERIAL PRIMARY KEY,
    postal_code VARCHAR,
    city_id INT REFERENCES City (city_id),
    country_id INT REFERENCES Country (country_id),
    description VARCHAR,
    UNIQUE(postal_code, country_id)
);

--    Event

CREATE TABLE Event
(
    event_id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    description VARCHAR NOT NULL,
    maximum_capacity VARCHAR,
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    location_id INT REFERENCES Location (location_id)
);

CREATE TABLE EventImage
(
    event_image_id SERIAL PRIMARY KEY,
    event_id INT REFERENCES Event (event_id),
    image_url VARCHAR NOT NULL,
    description VARCHAR,
    main_image BOOLEAN NOT NULL DEFAULT FALSE
);

--    Category

CREATE TABLE Category
(
    category_id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    UNIQUE(name)
);

--    Entertainer

CREATE TABLE Entertainer
(
    entertainer_id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    description VARCHAR NOT NULL
);

-- User

CREATE TABLE auth_user
(
    id SERIAL PRIMARY KEY,
    password VARCHAR,
    last_login TIMESTAMP,
    is_superuser BOOLEAN,
    username VARCHAR,
    first_name VARCHAR,
    last_name VARCHAR,
    email VARCHAR,
    is_staff BOOLEAN,
    is_active BOOLEAN,
    date_joined TIMESTAMP
);

CREATE TABLE UserDetails
(
    user_id INT REFERENCES auth_user (id),
    profile_image_url VARCHAR,
    PRIMARY KEY (user_id)
);

--   Tickets

CREATE TABLE TicketType
(
    ticket_type_id SERIAL PRIMARY KEY,
    description VARCHAR NOT NULL
);

CREATE TABLE Ticket
(
    ticket_id SERIAL PRIMARY KEY,
    ticket_type_id INT REFERENCES TicketType (ticket_type_id),
    event_id INT REFERENCES Event (event_id) NOT NULL,
    user_id INT REFERENCES auth_user (id),
    delivery_method TICKET_DELIVERY_METHODS NOT NULL,
    email VARCHAR NOT NULL,
    status TICKET_STATUS NOT NULL DEFAULT 'unreleased',
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    street_name VARCHAR NOT NULL,
    house_number INT NOT NULL,
    postal_code_id INT REFERENCES PostalCode (postal_code_id)
);

-- Relation Tables

--    Event

CREATE TABLE EventCategory
(
    event_entertainer_id SERIAL PRIMARY KEY,
    event_id INT REFERENCES Event (event_id) NOT NULL,
    category_id INT REFERENCES Category (category_id) NOT NULL,
    UNIQUE(event_id, category_id)
);

CREATE TABLE EventEntertainer
(
    event_entertainer_id SERIAL PRIMARY KEY,
    event_id INT REFERENCES Event (event_id) NOT NULL,
    entertainer_id INT REFERENCES Entertainer (entertainer_id) NOT NULL,
    UNIQUE(event_id, entertainer_id)
);

--    Ticket

CREATE TABLE EventTicketTypePrice
(
    event_ticket_type_price_id SERIAL PRIMARY KEY,
    event_id INT REFERENCES Event (event_id),
    ticket_type_id INT REFERENCES TicketType (ticket_type_id),
    price FLOAT
);

--    User

CREATE TABLE UserFavoriteCatagory
(
    user_favorite_category_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES auth_user (id),
    category_id INT,
    UNIQUE(user_id, category_id)
);