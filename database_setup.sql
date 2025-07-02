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
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    INDEX idx_email (email),
    INDEX idx_is_active (is_active)
);

-- Access Cards table
CREATE TABLE IF NOT EXISTS access_cards (
    id VARCHAR(36) PRIMARY KEY,
    card_number VARCHAR(50) UNIQUE NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    issue_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    expiry_date DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_card_number (card_number),
    INDEX idx_user_id (user_id),
    INDEX idx_is_active (is_active),
    INDEX idx_expiry_date (expiry_date)
);

-- Rooms table
CREATE TABLE IF NOT EXISTS rooms (
    id VARCHAR(36) PRIMARY KEY,
    room_number VARCHAR(50) UNIQUE NOT NULL,
    building_name VARCHAR(255) NOT NULL,
    capacity INT,
    room_type VARCHAR(100) NOT NULL,
    is_accessible BOOLEAN DEFAULT TRUE,
    INDEX idx_room_number (room_number),
    INDEX idx_building_name (building_name),
    INDEX idx_room_type (room_type),
    INDEX idx_is_accessible (is_accessible)
);

-- Access Logs table
CREATE TABLE IF NOT EXISTS access_logs (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    access_card_id VARCHAR(36) NOT NULL,
    room_id VARCHAR(36) NOT NULL,
    access_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    access_type ENUM('entry', 'exit') NOT NULL,
    status ENUM('granted', 'denied') NOT NULL,
    reason VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (access_card_id) REFERENCES access_cards(id) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_room_id (room_id),
    INDEX idx_access_time (access_time),
    INDEX idx_status (status),
    INDEX idx_access_type (access_type)
);

-- Reservations table
CREATE TABLE IF NOT EXISTS reservations (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    room_id VARCHAR(36) NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    purpose VARCHAR(255),
    status ENUM('pending', 'confirmed', 'cancelled', 'completed') DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_room_id (room_id),
    INDEX idx_start_time (start_time),
    INDEX idx_end_time (end_time),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
);

-- Students table
CREATE TABLE IF NOT EXISTS students (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    student_id VARCHAR(50) UNIQUE NOT NULL,
    major VARCHAR(255),
    graduation_year INT,
    enrollment_status ENUM('active', 'inactive', 'graduated', 'suspended') DEFAULT 'active',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_student_id (student_id),
    INDEX idx_major (major),
    INDEX idx_enrollment_status (enrollment_status)
);

-- Professors table
CREATE TABLE IF NOT EXISTS professors (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    employee_id VARCHAR(50) UNIQUE NOT NULL,
    department VARCHAR(255),
    title VARCHAR(255),
    office_location VARCHAR(255),
    employment_status ENUM('active', 'inactive', 'retired') DEFAULT 'active',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_employee_id (employee_id),
    INDEX idx_department (department),
    INDEX idx_employment_status (employment_status)
);

-- Insert sample data

-- Insert users (password is 'password' hashed with bcrypt)
INSERT INTO users (id, email, hashed_password, full_name, is_admin) VALUES
('550e8400-e29b-41d4-a716-446655440001', 'admin@campus.edu', '$2b$12$PixI/wVbjrDadtV7FuIg5uSjijRRbVZdlybvhtkx7bS7VROLqvh1y', 'Admin User', TRUE),
('550e8400-e29b-41d4-a716-446655440002', 'john.doe@campus.edu', '$2b$12$PixI/wVbjrDadtV7FuIg5uSjijRRbVZdlybvhtkx7bS7VROLqvh1y', 'John Doe', FALSE),
('550e8400-e29b-41d4-a716-446655440003', 'jane.smith@campus.edu', '$2b$12$PixI/wVbjrDadtV7FuIg5uSjijRRbVZdlybvhtkx7bS7VROLqvh1y', 'Jane Smith', FALSE),
('550e8400-e29b-41d4-a716-446655440004', 'prof.wilson@campus.edu', '$2b$12$PixI/wVbjrDadtV7FuIg5uSjijRRbVZdlybvhtkx7bS7VROLqvh1y', 'Professor Wilson', FALSE),
('550e8400-e29b-41d4-a716-446655440005', 'alice.johnson@campus.edu', '$2b$12$PixI/wVbjrDadtV7FuIg5uSjijRRbVZdlybvhtkx7bS7VROLqvh1y', 'Alice Johnson', FALSE);

-- Insert access cards
INSERT INTO access_cards (id, card_number, user_id, expiry_date) VALUES
('550e8400-e29b-41d4-a716-446655440101', 'CARD001', '550e8400-e29b-41d4-a716-446655440001', '2025-12-31 23:59:59'),
('550e8400-e29b-41d4-a716-446655440102', 'CARD002', '550e8400-e29b-41d4-a716-446655440002', '2025-12-31 23:59:59'),
('550e8400-e29b-41d4-a716-446655440103', 'CARD003', '550e8400-e29b-41d4-a716-446655440003', '2025-12-31 23:59:59'),
('550e8400-e29b-41d4-a716-446655440104', 'CARD004', '550e8400-e29b-41d4-a716-446655440004', '2025-12-31 23:59:59'),
('550e8400-e29b-41d4-a716-446655440105', 'CARD005', '550e8400-e29b-41d4-a716-446655440005', '2025-12-31 23:59:59');

-- Insert rooms
INSERT INTO rooms (id, room_number, building_name, capacity, room_type) VALUES
('550e8400-e29b-41d4-a716-446655440201', '101', 'Main Building', 30, 'classroom'),
('550e8400-e29b-41d4-a716-446655440202', '102', 'Main Building', 25, 'classroom'),
('550e8400-e29b-41d4-a716-446655440203', '201', 'Main Building', 40, 'lecture_hall'),
('550e8400-e29b-41d4-a716-446655440204', '301', 'Science Building', 20, 'laboratory'),
('550e8400-e29b-41d4-a716-446655440205', '401', 'Library', 50, 'study_room'),
('550e8400-e29b-41d4-a716-446655440206', '501', 'Admin Building', 10, 'meeting_room'),
('550e8400-e29b-41d4-a716-446655440207', '601', 'Gymnasium', 100, 'sports_facility'),
('550e8400-e29b-41d4-a716-446655440208', '701', 'Computer Center', 35, 'computer_lab');

-- Insert students
INSERT INTO students (id, user_id, student_id, major, graduation_year, enrollment_status) VALUES
('550e8400-e29b-41d4-a716-446655440301', '550e8400-e29b-41d4-a716-446655440002', 'STU2024001', 'Computer Science', 2026, 'active'),
('550e8400-e29b-41d4-a716-446655440302', '550e8400-e29b-41d4-a716-446655440003', 'STU2024002', 'Mathematics', 2025, 'active'),
('550e8400-e29b-41d4-a716-446655440303', '550e8400-e29b-41d4-a716-446655440005', 'STU2024003', 'Physics', 2027, 'active');

-- Insert professors
INSERT INTO professors (id, user_id, employee_id, department, title, office_location, employment_status) VALUES
('550e8400-e29b-41d4-a716-446655440401', '550e8400-e29b-41d4-a716-446655440004', 'EMP2024001', 'Computer Science', 'Associate Professor', 'Main Building, Room 205', 'active');

-- Insert access logs
INSERT INTO access_logs (id, user_id, access_card_id, room_id, access_time, access_type, status, reason) VALUES
('550e8400-e29b-41d4-a716-446655440501', '550e8400-e29b-41d4-a716-446655440002', '550e8400-e29b-41d4-a716-446655440102', '550e8400-e29b-41d4-a716-446655440201', '2024-01-15 09:00:00', 'entry', 'granted', 'Regular class access'),
('550e8400-e29b-41d4-a716-446655440502', '550e8400-e29b-41d4-a716-446655440002', '550e8400-e29b-41d4-a716-446655440102', '550e8400-e29b-41d4-a716-446655440201', '2024-01-15 10:30:00', 'exit', 'granted', 'Class ended'),
('550e8400-e29b-41d4-a716-446655440503', '550e8400-e29b-41d4-a716-446655440004', '550e8400-e29b-41d4-a716-446655440104', '550e8400-e29b-41d4-a716-446655440201', '2024-01-15 09:00:00', 'entry', 'granted', 'Teaching class'),
('550e8400-e29b-41d4-a716-446655440504', '550e8400-e29b-41d4-a716-446655440003', '550e8400-e29b-41d4-a716-446655440103', '550e8400-e29b-41d4-a716-446655440205', '2024-01-15 14:00:00', 'entry', 'granted', 'Study session'),
('550e8400-e29b-41d4-a716-446655440505', '550e8400-e29b-41d4-a716-446655440005', '550e8400-e29b-41d4-a716-446655440105', '550e8400-e29b-41d4-a716-446655440204', '2024-01-15 15:00:00', 'entry', 'denied', 'No lab access permission');

-- Insert reservations
INSERT INTO reservations (id, user_id, room_id, start_time, end_time, purpose, status) VALUES
('550e8400-e29b-41d4-a716-446655440601', '550e8400-e29b-41d4-a716-446655440004', '550e8400-e29b-41d4-a716-446655440206', '2024-01-16 10:00:00', '2024-01-16 11:00:00', 'Department meeting', 'confirmed'),
('550e8400-e29b-41d4-a716-446655440602', '550e8400-e29b-41d4-a716-446655440002', '550e8400-e29b-41d4-a716-446655440205', '2024-01-16 14:00:00', '2024-01-16 16:00:00', 'Study group session', 'pending'),
('550e8400-e29b-41d4-a716-446655440603', '550e8400-e29b-41d4-a716-446655440003', '550e8400-e29b-41d4-a716-446655440208', '2024-01-17 09:00:00', '2024-01-17 11:00:00', 'Programming lab', 'confirmed'),
('550e8400-e29b-41d4-a716-446655440604', '550e8400-e29b-41d4-a716-446655440005', '550e8400-e29b-41d4-a716-446655440204', '2024-01-17 13:00:00', '2024-01-17 15:00:00', 'Physics experiment', 'confirmed'); 