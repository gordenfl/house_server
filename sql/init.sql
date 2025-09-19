-- 创建数据库
CREATE DATABASE IF NOT EXISTS house_db;
USE house_db;

-- 用户表
CREATE TABLE users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone VARCHAR(20),
    role ENUM('USER', 'ADMIN') DEFAULT 'USER',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 房屋类型枚举表
CREATE TABLE house_types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT
);

INSERT INTO house_types (name, description) VALUES 
('APARTMENT', 'Apartment'),
('CONDO', 'Condominium'),
('HOUSE', 'Single Family House');

-- 房屋状态枚举表
CREATE TABLE house_statuses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT
);

INSERT INTO house_statuses (name, description) VALUES 
('FOR_SALE', 'For Sale'),
('SOLD', 'Sold'),
('FORECLOSED', 'Foreclosed');

-- 维修规模枚举表
CREATE TABLE maintenance_scales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(20) NOT NULL UNIQUE,
    description TEXT
);

INSERT INTO maintenance_scales (name, description) VALUES 
('SMALL', 'Small maintenance'),
('MEDIUM', 'Medium maintenance'),
('LARGE', 'Large maintenance');

-- 灾害类型枚举表
CREATE TABLE disaster_types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT
);

INSERT INTO disaster_types (name, description) VALUES 
('FIRE', 'Fire'),
('MURDER', 'Murder'),
('COLLAPSE', 'Collapse'),
('EARTHQUAKE', 'Earthquake'),
('FLOOD', 'Flood'),
('OTHER', 'Other');

-- 房屋主表
CREATE TABLE houses (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(50) NOT NULL,
    zip_code VARCHAR(20) NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    house_type_id INT NOT NULL,
    area_sqft INT NOT NULL,
    lot_area_sqft INT,
    house_status_id INT NOT NULL,
    build_year INT,
    bathrooms INT DEFAULT 0,
    bedrooms INT DEFAULT 0,
    description TEXT,
    zillow_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (house_type_id) REFERENCES house_types(id),
    FOREIGN KEY (house_status_id) REFERENCES house_statuses(id),
    INDEX idx_location (latitude, longitude),
    INDEX idx_city_state (city, state),
    INDEX idx_status (house_status_id)
);

-- 房屋销售记录表
CREATE TABLE house_sales (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    house_id BIGINT NOT NULL,
    sale_date DATE NOT NULL,
    sale_price DECIMAL(15, 2) NOT NULL,
    buyer_name VARCHAR(100),
    seller_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (house_id) REFERENCES houses(id) ON DELETE CASCADE,
    INDEX idx_house_sale_date (house_id, sale_date)
);

-- 房屋维修记录表
CREATE TABLE house_maintenance (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    house_id BIGINT NOT NULL,
    maintenance_date DATE NOT NULL,
    maintenance_scale_id INT NOT NULL,
    cost DECIMAL(10, 2) NOT NULL,
    description TEXT,
    contractor_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (house_id) REFERENCES houses(id) ON DELETE CASCADE,
    FOREIGN KEY (maintenance_scale_id) REFERENCES maintenance_scales(id),
    INDEX idx_house_maintenance_date (house_id, maintenance_date)
);

-- 房屋灾害记录表
CREATE TABLE house_disasters (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    house_id BIGINT NOT NULL,
    disaster_type_id INT NOT NULL,
    disaster_date DATE NOT NULL,
    description TEXT,
    severity ENUM('LOW', 'MEDIUM', 'HIGH', 'CRITICAL') DEFAULT 'MEDIUM',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (house_id) REFERENCES houses(id) ON DELETE CASCADE,
    FOREIGN KEY (disaster_type_id) REFERENCES disaster_types(id),
    INDEX idx_house_disaster_date (house_id, disaster_date)
);

-- 创建管理员用户
INSERT INTO users (username, email, password_hash, first_name, last_name, role) VALUES 
('admin', 'admin@house.com', '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iKTVEFDi', 'Admin', 'User', 'ADMIN');

-- 创建测试用户
INSERT INTO users (username, email, password_hash, first_name, last_name) VALUES 
('testuser', 'user@house.com', '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iKTVEFDi', 'Test', 'User');
