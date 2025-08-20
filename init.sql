-- Создаем схему если не существует
CREATE SCHEMA IF NOT EXISTS weather;

-- Даем права пользователю
GRANT ALL PRIVILEGES ON SCHEMA weather TO postgres;

-- Создаем таблицу для погоды
CREATE TABLE IF NOT EXISTS weather.weather_data (
    city VARCHAR(100) NOT NULL,
    temp DECIMAL(5,2) NOT NULL,
    humidity INTEGER,
    pressure INTEGER,
    wind_speed DECIMAL(5,2),
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Даем права на таблицу
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA weather TO postgres;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA weather TO postgres;