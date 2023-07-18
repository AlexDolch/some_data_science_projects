-- city	country	population	lat	long-- 

DROP DATABASE gans;
CREATE DATABASE gans;

USE gans;

CREATE TABLE IF NOT EXISTS city (
	city_id INT AUTO_INCREMENT,
    city VARCHAR(100),
    country VARCHAR(100),
    population INT,
    lat FLOAT,
    `long` FLOAT,
    PRIMARY KEY (city_id)
);

--  0   city_id     324 non-null    int64  
--  1   time        324 non-null    object 
--  2   temp        324 non-null    float64
--  3   wind_speed  324 non-null    float64

CREATE TABLE IF NOT EXISTS weather(
	weather_id INT AUTO_INCREMENT,
    city_id INT NOT NULL,
    `time` DATETIME,
    temp FLOAT,
    wind_speed FLOAT,
    PRIMARY KEY (weather_id),
    FOREIGN KEY (city_id) REFERENCES city(city_id)    
);

--  city_id       22 non-null     int64 
--  1   icao          22 non-null     object
--  2   airport_name  22 non-null     object

DROP TABLE airports;
CREATE TABLE IF NOT EXISTS airports(
	city_id INT NOT NULL,
    icao VARCHAR(10),
    PRIMARY KEY (icao),
    FOREIGN KEY (city_id) REFERENCES city(city_id)
);


-- 0   ICAO               20 non-null     object
--  1   departure_airport  20 non-null     object
--  2   local_time         20 non-null     object

CREATE TABLE IF NOT EXISTS flight(
	flight_id INT AUTO_INCREMENT,
    ICAO VARCHAR(10),
    departure_airport VARCHAR(10),
    local_time DATETIME,
    PRIMARY KEY (flight_id),
    FOREIGN KEY (ICAO) REFERENCES airports(icao)
);