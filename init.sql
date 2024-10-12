CREATE DATABASE IF NOT EXISTS nail_db;
CREATE USER 'nail'@'localhost' IDENTIFIED BY 'nail';
GRANT ALL PRIVILEGES ON nail_db . * TO 'nail'@'localhost';

