-- Campus Access Management System Database Setup
-- This script creates the database and grants necessary permissions

-- Create database
CREATE DATABASE IF NOT EXISTS campus_access_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- Create user (change username and password as needed)
CREATE USER IF NOT EXISTS 'campus_user'@'localhost' IDENTIFIED BY 'campus_password';

-- Grant permissions
GRANT ALL PRIVILEGES ON campus_access_db.* TO 'campus_user'@'localhost';

-- Grant permissions for any host (for development)
GRANT ALL PRIVILEGES ON campus_access_db.* TO 'campus_user'@'%';

-- Flush privileges
FLUSH PRIVILEGES;

-- Use the database
USE campus_access_db;

-- Show created database
SHOW DATABASES LIKE 'campus_access_db';

-- Show user permissions
SHOW GRANTS FOR 'campus_user'@'localhost'; 