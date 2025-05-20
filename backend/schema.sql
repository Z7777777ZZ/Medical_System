USE medical_system;
-- 首先删除依赖medicines表的表（处理外键约束）
DROP TABLE IF EXISTS prescription_details;
DROP TABLE IF EXISTS prescriptions;
DROP TABLE IF EXISTS medicines;
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
    specification VARCHAR(1024) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    description TEXT
);

-- 创建处方表
CREATE TABLE IF NOT EXISTS prescriptions (
    prescription_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    patient_id BIGINT NOT NULL,
    doctor_id BIGINT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    instructions TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
);

-- 创建处方明细表
CREATE TABLE IF NOT EXISTS prescription_details (
    detail_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    prescription_id BIGINT NOT NULL,
    medicine_id BIGINT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    instructions TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    FOREIGN KEY (prescription_id) REFERENCES prescriptions(prescription_id) ON DELETE CASCADE,
    FOREIGN KEY (medicine_id) REFERENCES medicines(medicine_id)
);

-- 创建电子病历表
CREATE TABLE IF NOT EXISTS medical_records (
    record_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    patient_id BIGINT NOT NULL,
    doctor_id BIGINT NOT NULL,
    visit_date DATE NOT NULL,
    discription TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    photo TEXT,
    diagnosis TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    prescription_id BIGINT,
    treatment TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
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

-- 创建排队表
CREATE TABLE IF NOT EXISTS queues (
    queue_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    patient_id BIGINT NOT NULL,
    doctor_id BIGINT NOT NULL,
    queue_number INT NOT NULL,
    status ENUM('waiting', 'called') NOT NULL DEFAULT 'waiting',
    priority BOOLEAN DEFAULT FALSE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
);

-- 插入医院数据
INSERT INTO hospitals (hospital_id, name, address) VALUES
(1, '市中心医院', '市中心大街123号'),
(2, '人民医院', '人民路456号'),
(3, '妇幼保健院', '妇幼路789号');

-- 插入科室数据
INSERT INTO departments (department_id, name, hospital_id) VALUES
(1, '内科', 1),
(2, '外科', 1),
(3, '儿科', 1),
(4, '妇产科', 2),
(5, '骨科', 2),
(6, '皮肤科', 3),
(7, '眼科', 3);

-- 插入患者数据
INSERT INTO patients (patient_id, phone, email, name, password_hash, created_at) VALUES
(1, '13800138001', 'zhang@example.com', '张三', '$2a$10$1qAz2wSx3eDc4rFv5tGb5edO/Y/cZy/T/20OEyq1DRaBmH7G.PmLq', '2023-09-01 08:00:00'),
(2, '13800138002', 'li@example.com', '李四', '$2a$10$1qAz2wSx3eDc4rFv5tGb5edO/Y/cZy/T/20OEyq1DRaBmH7G.PmLq', '2023-09-02 09:30:00'),
(3, '13800138003', 'wang@example.com', '王五', '$2a$10$1qAz2wSx3eDc4rFv5tGb5edO/Y/cZy/T/20OEyq1DRaBmH7G.PmLq', '2023-09-03 10:45:00'),
(4, '13800138004', 'zhao@example.com', '赵六', '$2a$10$1qAz2wSx3eDc4rFv5tGb5edO/Y/cZy/T/20OEyq1DRaBmH7G.PmLq', '2023-09-04 14:20:00');

-- 插入医生数据
INSERT INTO doctors (doctor_id, phone, name, hospital_id, department_id, specialty, bio, password_hash, created_at) VALUES
(1, '13900139001', '刘医生', 1, 1, '心血管内科', '从业20年，专攻心血管疾病', '$2a$10$1qAz2wSx3eDc4rFv5tGb5edO/Y/cZy/T/20OEyq1DRaBmH7G.PmLq', '2023-08-01 08:00:00'),
(2, '13900139002', '杨医生', 1, 2, '普外科', '外科手术专家', '$2a$10$1qAz2wSx3eDc4rFv5tGb5edO/Y/cZy/T/20OEyq1DRaBmH7G.PmLq', '2023-08-02 09:00:00'),
(3, '13900139003', '周医生', 2, 4, '产科', '高风险妊娠专家', '$2a$10$1qAz2wSx3eDc4rFv5tGb5edO/Y/cZy/T/20OEyq1DRaBmH7G.PmLq', '2023-08-03 10:00:00'),
(4, '13900139004', '吴医生', 2, 5, '创伤骨科', '骨折治疗专家', '$2a$10$1qAz2wSx3eDc4rFv5tGb5edO/Y/cZy/T/20OEyq1DRaBmH7G.PmLq', '2023-08-04 11:00:00'),
(5, '13900139005', '郑医生', 3, 6, '皮肤病理', '皮肤过敏治疗专家', '$2a$10$1qAz2wSx3eDc4rFv5tGb5edO/Y/cZy/T/20OEyq1DRaBmH7G.PmLq', '2023-08-05 12:00:00');

-- 插入患者详细信息
INSERT INTO patient_details (patient_id, gender, date_of_birth, blood_type, height, weight, emergency_contact, emergency_phone, medical_insurance_id, allergies, chronic_conditions, medications) VALUES
(1, 'male', '1980-05-15', 'A+', 175.5, 70.2, '张太太', '13800138011', 'INS12345', '青霉素', '高血压', '硝苯地平'),
(2, 'female', '1985-08-20', 'B+', 165.0, 55.5, '李先生', '13800138022', 'INS23456', '无', '糖尿病', '二甲双胍'),
(3, 'male', '1975-12-10', 'O+', 180.0, 85.0, '王太太', '13800138033', 'INS34567', '花粉', '无', '无'),
(4, 'female', '1990-03-25', 'AB-', 160.5, 50.0, '赵先生', '13800138044', 'INS45678', '海鲜', '贫血', '铁剂补充');

-- 插入药品数据
INSERT INTO medicines (medicine_id, name, specification, price, stock, description) VALUES
(1, '阿莫西林胶囊', '0.25g*24粒', 24.5, 100, '用于敏感菌所致的各种感染'),
(2, '布洛芬缓释胶囊', '0.3g*10粒', 16.8, 150, '用于缓解轻至中度疼痛'),
(3, '头孢克肟胶囊', '100mg*6片', 38.5, 80, '用于敏感菌所致的呼吸道感染等'),
(4, '感冒灵颗粒', '10g*9袋', 12.5, 200, '用于感冒引起的头痛、发热等'),
(5, '维生素C片', '100mg*60片', 8.5, 300, '用于维生素C缺乏的预防和治疗'),
(6, '盐酸氨溴索片', '30mg*20片', 15.6, 120, '用于急慢性呼吸道疾病痰液粘稠'),
(7, '复方甘草片', '0.5g*24片', 9.8, 180, '用于镇咳祛痰'),
(8, '降压钙片', '300mg*60片', 28.5, 90, '用于高血压患者的辅助治疗');

-- 插入处方数据
INSERT INTO prescriptions (prescription_id, patient_id, doctor_id, created_at, instructions, status) VALUES
(1, 1, 1, '2023-10-01 10:00:00', '请按时服用药物，注意休息', 'pending'),
(2, 2, 2, '2023-10-02 11:00:00', '注意休息，多喝水', 'pending'),
(3, 3, 3, '2023-10-03 14:30:00', '三餐后服用，避免辛辣食物', 'pending'),
(4, 4, 4, '2023-10-04 16:45:00', '按时服药，两周后复诊', 'pending'),
(5, 1, 5, '2023-10-05 09:15:00', '外用药涂抹患处，每日两次', 'pending');

-- 插入处方明细数据
INSERT INTO prescription_details (prescription_id, medicine_id, quantity, instructions) VALUES
(1, 1, 2, '一日三次，饭后服用'),
(1, 4, 1, '一日三次，温水冲服'),
(2, 2, 1, '发热时服用，一次一粒，间隔6小时'),
(2, 5, 1, '一日一次，饭后服用'),
(3, 3, 1, '一日两次，早晚各一次'),
(3, 6, 1, '一日三次，饭后服用'),
(4, 7, 2, '一日三次，饭后服用'),
(4, 8, 1, '一日一次，晚饭后服用'),
(5, 2, 1, '疼痛时服用，一次一粒'),
(5, 6, 1, '一日两次，早晚各一次');

-- 插入电子病历数据
INSERT INTO medical_records (patient_id, doctor_id, visit_date, discription, diagnosis, prescription_id, treatment, created_at) VALUES
(1, 1, '2023-10-01', '患者出现胸闷、气短症状三天', '冠心病', 1, '药物治疗为主，建议心脏彩超检查', '2023-10-01 10:30:00'),
(2, 2, '2023-10-02', '患者右侧腹部疼痛，伴有恶心', '阑尾炎', 2, '建议手术治疗', '2023-10-02 11:30:00'),
(3, 3, '2023-10-03', '孕妇例行产检', '妊娠28周，一切正常', 3, '继续定期产检', '2023-10-03 15:00:00'),
(4, 4, '2023-10-04', '患者右腿摔伤，行走困难', '胫骨轻微骨裂', 4, '石膏固定，卧床休息两周', '2023-10-04 17:15:00'),
(1, 5, '2023-10-05', '患者出现皮疹，伴有瘙痒', '接触性皮炎', 5, '避免接触过敏原，使用外用药膏', '2023-10-05 09:45:00');

-- 插入预约数据
INSERT INTO appointments (patient_id, doctor_id, appointment_time, status) VALUES
(1, 1, '2023-10-15 09:00:00', 'confirmed'),
(2, 2, '2023-10-16 10:30:00', 'confirmed'),
(3, 3, '2023-10-17 14:00:00', 'pending'),
(4, 4, '2023-10-18 15:30:00', 'pending'),
(1, 5, '2023-10-19 11:00:00', 'confirmed');

-- 插入支付数据
INSERT INTO payments (patient_id, amount, type, status) VALUES
(1, 120.50, '门诊费用', 'paid'),
(2, 350.80, '手术费用', 'paid'),
(3, 80.00, '产检费用', 'paid'),
(4, 200.30, '骨科治疗', 'pending'),
(1, 65.20, '药品费用', 'pending');

-- 插入排队数据
INSERT INTO queues (patient_id, doctor_id, queue_number, status, priority, created_at) VALUES
(1, 1, 1, 'called', FALSE, '2023-10-01 08:30:00'),
(2, 2, 2, 'called', FALSE, '2023-10-02 09:45:00'),
(3, 3, 1, 'waiting', FALSE, '2023-10-03 13:50:00'),
(4, 4, 1, 'waiting', TRUE, '2023-10-04 14:30:00'),
(1, 5, 3, 'waiting', FALSE, '2023-10-05 08:45:00'),
-- 添加更多可被取消的挂号测试数据
(1, 2, 4, 'waiting', FALSE, '2023-10-06 09:00:00'),
(2, 3, 3, 'waiting', FALSE, '2023-10-06 09:15:00'),
(3, 1, 2, 'waiting', FALSE, '2023-10-06 09:30:00'),
(4, 5, 2, 'waiting', FALSE, '2023-10-06 10:00:00'),
(1, 3, 5, 'waiting', TRUE, '2023-10-06 10:15:00'),
(2, 4, 4, 'waiting', FALSE, '2023-10-06 10:30:00'),
(3, 5, 4, 'waiting', TRUE, '2023-10-06 11:00:00'),
(4, 1, 3, 'waiting', FALSE, '2023-10-06 11:15:00'),
(1, 4, 6, 'waiting', FALSE, '2023-10-06 13:00:00'),
(2, 5, 5, 'waiting', FALSE, '2023-10-06 13:30:00');