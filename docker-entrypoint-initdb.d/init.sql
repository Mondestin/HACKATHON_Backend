CREATE DATABASE IF NOT EXISTS estiamAccess;
CREATE USER IF NOT EXISTS 'campus_user'@'%' IDENTIFIED BY 'campus_pass';
GRANT ALL PRIVILEGES ON estiamAccess.* TO 'campus_user'@'%';
FLUSH PRIVILEGES;
