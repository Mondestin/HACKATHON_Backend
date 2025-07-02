-- Campus Access Management System Database Setup
-- This script creates the database and all necessary tables with sample data

-- Create database if not exists
CREATE DATABASE IF NOT EXISTS campus_access_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- Use the database
USE campus_access_db;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'student', 'professor') NOT NULL,
    INDEX idx_email (email)
);

-- Roles table
CREATE TABLE IF NOT EXISTS roles (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- User roles table (many-to-many relationship)
CREATE TABLE IF NOT EXISTS user_roles (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    role_id VARCHAR(36) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
);

-- Access Cards table
CREATE TABLE IF NOT EXISTS access_cards (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    card_number VARCHAR(50) UNIQUE NOT NULL,
    status ENUM('active', 'lost', 'disabled') DEFAULT 'active',
    issued_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_card_number (card_number),
    INDEX idx_user_id (user_id)
);

-- Rooms table
CREATE TABLE IF NOT EXISTS rooms (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL,
    capacity INT NOT NULL,
    CHECK (capacity > 0),
    INDEX idx_name (name),
    INDEX idx_location (location)
);

-- Room Reservations table
CREATE TABLE IF NOT EXISTS room_reservations (
    id VARCHAR(36) PRIMARY KEY,
    room_id VARCHAR(36) NOT NULL,
    reserved_by VARCHAR(36) NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    expected_occupants INT NOT NULL,
    CHECK (expected_occupants > 0),
    FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE CASCADE,
    FOREIGN KEY (reserved_by) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_room_id (room_id),
    INDEX idx_reserved_by (reserved_by),
    INDEX idx_start_time (start_time),
    INDEX idx_end_time (end_time)
);

-- Access Logs table
CREATE TABLE IF NOT EXISTS access_logs (
    id VARCHAR(36) PRIMARY KEY,
    card_id VARCHAR(36),
    accessed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    location VARCHAR(100) NOT NULL,
    access_type ENUM('entry', 'exit', 'denied') NOT NULL,
    granted BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (card_id) REFERENCES access_cards(id) ON DELETE SET NULL,
    INDEX idx_card_id (card_id),
    INDEX idx_accessed_at (accessed_at),
    INDEX idx_location (location)
);

-- Students table
CREATE TABLE IF NOT EXISTS students (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    student_card_id VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    class_name VARCHAR(50) NOT NULL,
    phone_number VARCHAR(20),
    registered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_student_card_id (student_card_id),
    INDEX idx_email (email)
);

-- Professors table
CREATE TABLE IF NOT EXISTS professors (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    department VARCHAR(100),
    phone_number VARCHAR(20),
    office VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_email (email),
    INDEX idx_department (department)
);

-- Insert sample data

-- Insert roles
INSERT INTO roles (id, name) VALUES
('550e8400-e29b-41d4-a716-446655440000', 'admin'),
('550e8400-e29b-41d4-a716-446655440001', 'student'),
('550e8400-e29b-41d4-a716-446655440002', 'professor');

-- Insert users (password is 'password' hashed with bcrypt)
INSERT INTO users (id, email, password_hash, role) VALUES
('550e8400-e29b-41d4-a716-446655440003', 'admin@campus.edu', '$2b$12$PixI/wVbjrDadtV7FuIg5uSjijRRbVZdlybvhtkx7bS7VROLqvh1y', 'admin'),
('550e8400-e29b-41d4-a716-446655440004', 'john.doe@campus.edu', '$2b$12$PixI/wVbjrDadtV7FuIg5uSjijRRbVZdlybvhtkx7bS7VROLqvh1y', 'student'),
('550e8400-e29b-41d4-a716-446655440005', 'jane.smith@campus.edu', '$2b$12$PixI/wVbjrDadtV7FuIg5uSjijRRbVZdlybvhtkx7bS7VROLqvh1y', 'student'),
('550e8400-e29b-41d4-a716-446655440006', 'prof.wilson@campus.edu', '$2b$12$PixI/wVbjrDadtV7FuIg5uSjijRRbVZdlybvhtkx7bS7VROLqvh1y', 'professor'),
('550e8400-e29b-41d4-a716-446655440007', 'alice.johnson@campus.edu', '$2b$12$PixI/wVbjrDadtV7FuIg5uSjijRRbVZdlybvhtkx7bS7VROLqvh1y', 'student');

-- Insert user roles
INSERT INTO user_roles (id, user_id, role_id) VALUES
('550e8400-e29b-41d4-a716-446655440008', '550e8400-e29b-41d4-a716-446655440003', '550e8400-e29b-41d4-a716-446655440000'),
('550e8400-e29b-41d4-a716-446655440009', '550e8400-e29b-41d4-a716-446655440004', '550e8400-e29b-41d4-a716-446655440001'),
('550e8400-e29b-41d4-a716-446655440010', '550e8400-e29b-41d4-a716-446655440005', '550e8400-e29b-41d4-a716-446655440001'),
('550e8400-e29b-41d4-a716-446655440011', '550e8400-e29b-41d4-a716-446655440006', '550e8400-e29b-41d4-a716-446655440002'),
('550e8400-e29b-41d4-a716-446655440012', '550e8400-e29b-41d4-a716-446655440007', '550e8400-e29b-41d4-a716-446655440001');

-- Insert access cards
INSERT INTO access_cards (id, user_id, card_number, status, issued_at) VALUES
('550e8400-e29b-41d4-a716-446655440101', '550e8400-e29b-41d4-a716-446655440003', 'CARD001', 'active', '2024-01-01 00:00:00'),
('550e8400-e29b-41d4-a716-446655440102', '550e8400-e29b-41d4-a716-446655440004', 'CARD002', 'active', '2024-01-01 00:00:00'),
('550e8400-e29b-41d4-a716-446655440103', '550e8400-e29b-41d4-a716-446655440005', 'CARD003', 'active', '2024-01-01 00:00:00'),
('550e8400-e29b-41d4-a716-446655440104', '550e8400-e29b-41d4-a716-446655440006', 'CARD004', 'active', '2024-01-01 00:00:00'),
('550e8400-e29b-41d4-a716-446655440105', '550e8400-e29b-41d4-a716-446655440007', 'CARD005', 'active', '2024-01-01 00:00:00');

-- Insert rooms
INSERT INTO rooms (id, name, location, capacity) VALUES
('550e8400-e29b-41d4-a716-446655440201', 'Room 101', 'Main Building', 30),
('550e8400-e29b-41d4-a716-446655440202', 'Room 102', 'Main Building', 25),
('550e8400-e29b-41d4-a716-446655440203', 'Lecture Hall 201', 'Main Building', 40),
('550e8400-e29b-41d4-a716-446655440204', 'Lab 301', 'Science Building', 20),
('550e8400-e29b-41d4-a716-446655440205', 'Study Room 401', 'Library', 50),
('550e8400-e29b-41d4-a716-446655440206', 'Meeting Room 501', 'Admin Building', 10),
('550e8400-e29b-41d4-a716-446655440207', 'Gymnasium', 'Sports Center', 100),
('550e8400-e29b-41d4-a716-446655440208', 'Computer Lab 601', 'Computer Center', 35);

-- Insert students
INSERT INTO students (id, user_id, full_name, student_card_id, email, class_name, phone_number, registered_at) VALUES
('550e8400-e29b-41d4-a716-446655440301', '550e8400-e29b-41d4-a716-446655440004', 'John Doe', 'STU2024001', 'john.doe@campus.edu', 'Computer Science', '+1234567890', '2024-01-01 00:00:00'),
('550e8400-e29b-41d4-a716-446655440302', '550e8400-e29b-41d4-a716-446655440005', 'Jane Smith', 'STU2024002', 'jane.smith@campus.edu', 'Mathematics', '+1234567891', '2024-01-01 00:00:00'),
('550e8400-e29b-41d4-a716-446655440303', '550e8400-e29b-41d4-a716-446655440007', 'Alice Johnson', 'STU2024003', 'alice.johnson@campus.edu', 'Physics', '+1234567892', '2024-01-01 00:00:00');

-- Insert professors
INSERT INTO professors (id, user_id, full_name, email, department, phone_number, office) VALUES
('550e8400-e29b-41d4-a716-446655440401', '550e8400-e29b-41d4-a716-446655440006', 'Professor Wilson', 'prof.wilson@campus.edu', 'Computer Science', '+1234567893', 'Main Building, Room 205');

-- Insert access logs
INSERT INTO access_logs (id, card_id, accessed_at, location, access_type, granted) VALUES
('550e8400-e29b-41d4-a716-446655440501', '550e8400-e29b-41d4-a716-446655440102', '2024-01-15 09:00:00', 'Main Building', 'entry', TRUE),
('550e8400-e29b-41d4-a716-446655440502', '550e8400-e29b-41d4-a716-446655440102', '2024-01-15 10:30:00', 'Main Building', 'exit', TRUE),
('550e8400-e29b-41d4-a716-446655440503', '550e8400-e29b-41d4-a716-446655440104', '2024-01-15 09:00:00', 'Main Building', 'entry', TRUE),
('550e8400-e29b-41d4-a716-446655440504', '550e8400-e29b-41d4-a716-446655440103', '2024-01-15 14:00:00', 'Library', 'entry', TRUE),
('550e8400-e29b-41d4-a716-446655440505', '550e8400-e29b-41d4-a716-446655440105', '2024-01-15 15:00:00', 'Science Building', 'denied', FALSE);

-- Insert room reservations
INSERT INTO room_reservations (id, room_id, reserved_by, start_time, end_time, expected_occupants) VALUES
('550e8400-e29b-41d4-a716-446655440601', '550e8400-e29b-41d4-a716-446655440206', '550e8400-e29b-41d4-a716-446655440006', '2024-01-16 10:00:00', '2024-01-16 11:00:00', 8),
('550e8400-e29b-41d4-a716-446655440602', '550e8400-e29b-41d4-a716-446655440205', '550e8400-e29b-41d4-a716-446655440004', '2024-01-16 14:00:00', '2024-01-16 16:00:00', 5),
('550e8400-e29b-41d4-a716-446655440603', '550e8400-e29b-41d4-a716-446655440208', '550e8400-e29b-41d4-a716-446655440005', '2024-01-17 09:00:00', '2024-01-17 11:00:00', 30),
('550e8400-e29b-41d4-a716-446655440604', '550e8400-e29b-41d4-a716-446655440204', '550e8400-e29b-41d4-a716-446655440007', '2024-01-17 13:00:00', '2024-01-17 15:00:00', 15); 