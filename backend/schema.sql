-- Existing tables from development manual
-- 创建用户表
CREATE TABLE IF NOT EXISTS patients (
    patient_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL,
    name VARCHAR(50) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 创建医院表
CREATE TABLE IF NOT EXISTS hospitals (
    hospital_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL
);

-- 创建科室表
CREATE TABLE IF NOT EXISTS departments (
    department_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    hospital_id BIGINT NOT NULL,
    FOREIGN KEY (hospital_id) REFERENCES hospitals(hospital_id)
);

-- 创建医生表
CREATE TABLE IF NOT EXISTS doctors (
    doctor_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    phone VARCHAR(20) NOT NULL,
    name VARCHAR(50) NOT NULL,
    hospital_id BIGINT NOT NULL,
    department_id BIGINT NOT NULL,
    specialty VARCHAR(100) NOT NULL,
    bio TEXT,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (hospital_id) REFERENCES hospitals(hospital_id),
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

-- 创建患者信息表
CREATE TABLE IF NOT EXISTS patient_details (
    patient_id BIGINT PRIMARY KEY,
    gender ENUM('male', 'female', 'other'),
    date_of_birth DATE,
    blood_type ENUM('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'),
    height DECIMAL(5,2),
    weight DECIMAL(5,2),
    emergency_contact VARCHAR(100),
    emergency_phone VARCHAR(20),
    medical_insurance_id VARCHAR(50),
    allergies TEXT,
    chronic_conditions TEXT,
    medications TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);

-- 创建药品表
CREATE TABLE IF NOT EXISTS medicines (
    medicine_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    description TEXT
);

-- 创建处方表
CREATE TABLE IF NOT EXISTS prescriptions (
    prescription_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    patient_id BIGINT NOT NULL,
    doctor_id BIGINT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
);

-- 创建处方明细表
CREATE TABLE IF NOT EXISTS prescription_details (
    detail_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    prescription_id BIGINT NOT NULL,
    medicine_id BIGINT NOT NULL,
    instructions TEXT NOT NULL,
    FOREIGN KEY (prescription_id) REFERENCES prescriptions(prescription_id),
    FOREIGN KEY (medicine_id) REFERENCES medicines(medicine_id)
);

-- 创建电子病历表
CREATE TABLE IF NOT EXISTS medical_records (
    record_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    patient_id BIGINT NOT NULL,
    doctor_id BIGINT NOT NULL,
    visit_date DATE NOT NULL,
    discription TEXT,
    photo TEXT,
    diagnosis TEXT NOT NULL,
    prescription_id BIGINT,
    treatment TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id),
    FOREIGN KEY (prescription_id) REFERENCES prescriptions(prescription_id)
);

-- 创建预约表
CREATE TABLE IF NOT EXISTS appointments (
    appointment_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    patient_id BIGINT NOT NULL,
    doctor_id BIGINT NOT NULL,
    appointment_time DATETIME NOT NULL,
    status ENUM('pending', 'confirmed', 'cancelled') NOT NULL DEFAULT 'pending',
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
);

-- 创建支付表
CREATE TABLE IF NOT EXISTS payments (
    payment_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    patient_id BIGINT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    type VARCHAR(50) NOT NULL,
    status ENUM('pending', 'paid') NOT NULL DEFAULT 'pending',
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);

-- New tables for queue management
-- 创建排队表 (Updated version with priority field)
CREATE TABLE IF NOT EXISTS queues (
    queue_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    patient_id BIGINT NOT NULL,
    doctor_id BIGINT NOT NULL,
    queue_number INT NOT NULL,
    status ENUM('waiting', 'called') NOT NULL DEFAULT 'waiting',
    priority BOOLEAN DEFAULT FALSE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
); 