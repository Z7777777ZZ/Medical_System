CREATE DATABASE medical_system;

use medical_system;

-- 创建医院表
CREATE TABLE hospitals (
    hospital_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL
);

-- 创建科室表
CREATE TABLE departments (
    department_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    hospital_id BIGINT NOT NULL,
    FOREIGN KEY (hospital_id) REFERENCES hospitals(hospital_id)
);

-- 创建医生表
CREATE TABLE doctors (
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

-- 插入医院数据
INSERT INTO hospitals (name, address) VALUES 
('北京协和医院', '北京市东城区帅府园1号'),
('上海瑞金医院', '上海市黄浦区瑞金二路197号'),
('广州南方医院', '广州市白云区广花路1838号');

-- 插入科室数据
INSERT INTO departments (name, hospital_id) VALUES 
('内科', 1),
('外科', 1),
('妇产科', 1),
('儿科', 1),
('骨科', 2),
('心脏内科', 2),
('神经内科', 2),
('急诊科', 3),
('肿瘤科', 3),
('眼科', 3);

-- 插入医生数据
INSERT INTO doctors (phone, name, hospital_id, department_id, specialty, bio, password_hash, created_at) VALUES 
('13800001111', '张伟', 1, 1, '呼吸系统疾病', '毕业于北京医科大学，从事呼吸系统疾病研究20年', SHA2('password123', 256), '2023-01-15 09:00:00'),
('13800002222', '王芳', 1, 3, '妇科肿瘤', '妇科肿瘤专家，擅长妇科恶性肿瘤的诊断与治疗', SHA2('password123', 256), '2023-01-16 10:30:00'),
('13800003333', '李明', 1, 2, '胃肠外科', '擅长微创手术和胃肠道肿瘤手术', SHA2('password123', 256), '2023-02-01 08:45:00'),
('13800004444', '赵华', 2, 5, '骨折创伤', '专注于复杂骨折和创伤修复', SHA2('password123', 256), '2023-02-10 14:00:00'),
('13800005555', '刘洋', 2, 6, '冠心病', '心脏介入治疗专家', SHA2('password123', 256), '2023-03-05 11:20:00'),
('13800006666', '陈晓', 3, 9, '肺癌治疗', '肺癌靶向治疗和免疫治疗专家', SHA2('password123', 256), '2023-03-15 16:40:00'),
('13800007777', '杨红', 3, 10, '白内障手术', '高级眼科医师，擅长各类眼科疾病诊疗', SHA2('password123', 256), '2023-04-01 09:15:00');

-- 创建用户表
CREATE TABLE patients (
    patient_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL,
    name VARCHAR(50) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 插入患者数据
INSERT INTO patients (phone, email, name, password_hash, created_at) VALUES 
('13900001111', 'patient1@example.com', '张三', SHA2('patientpwd1', 256), '2023-05-01 10:00:00'),
('13900002222', 'patient2@example.com', '李四', SHA2('patientpwd2', 256), '2023-05-02 11:30:00'),
('13900003333', 'patient3@example.com', '王五', SHA2('patientpwd3', 256), '2023-05-03 14:20:00'),
('13900004444', 'patient4@example.com', '赵六', SHA2('patientpwd4', 256), '2023-05-04 16:45:00'),
('13900005555', 'patient5@example.com', '孙七', SHA2('patientpwd5', 256), '2023-05-05 09:15:00'),
('13900006666', 'patient6@example.com', '周八', SHA2('patientpwd6', 256), '2023-05-06 13:40:00'),
('13900007777', 'patient7@example.com', '吴九', SHA2('patientpwd7', 256), '2023-05-07 15:10:00'),
('13900008888', 'patient8@example.com', '郑十', SHA2('patientpwd8', 256), '2023-05-08 10:50:00');

-- 创建医生评分评价表
CREATE TABLE doctor_reviews (
    review_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    patient_id BIGINT NOT NULL,
    doctor_id BIGINT NOT NULL,
    rating TINYINT NOT NULL CHECK (rating BETWEEN 1 AND 5),  -- 1-5星评分
    comment TEXT,
    review_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
);

-- 插入医生评价测试数据
INSERT INTO doctor_reviews (patient_id, doctor_id, rating, comment, review_date) VALUES
-- 张伟医生(1)的评价
(1, 1, 5, '张医生非常专业，耐心解答我的问题，治疗效果很好', '2023-06-10 14:30:00'),
(2, 1, 4, '问诊过程很细致，但候诊时间稍长', '2023-06-15 10:20:00'),
(3, 1, 5, '医术高明，吃了张医生开的药很快就好了', '2023-06-20 16:45:00'),

-- 王芳医生(2)的评价
(4, 2, 5, '王医生非常温柔，妇科检查一点也不紧张', '2023-06-12 09:15:00'),
(5, 2, 3, '医术不错，但等待时间太长', '2023-06-18 11:30:00'),
(6, 2, 4, '专业且耐心，解释得很清楚', '2023-06-25 14:20:00'),

-- 李明医生(3)的评价
(7, 3, 5, '李医生的微创手术技术一流，恢复很快', '2023-06-05 10:00:00'),
(8, 3, 4, '诊断准确，治疗效果明显', '2023-06-15 15:30:00'),
(1, 3, 5, '胃肠问题困扰多年，李医生一次就解决了', '2023-06-22 09:45:00'),

-- 赵华医生(4)的评价
(2, 4, 5, '骨折恢复得很好，赵医生手法专业', '2023-06-08 14:15:00'),
(3, 4, 4, '态度和蔼，解释详细', '2023-06-16 11:20:00'),
(4, 4, 5, '手术很成功，术后指导也很到位', '2023-06-24 16:30:00'),

-- 刘洋医生(5)的评价
(5, 5, 5, '心脏问题得到很好控制，刘医生非常专业', '2023-06-11 10:45:00'),
(6, 5, 4, '问诊过程很详细，药物调整后效果明显', '2023-06-19 15:10:00'),
(7, 5, 5, '冠心病治疗专家，名不虚传', '2023-06-28 09:30:00'),

-- 陈晓医生(6)的评价
(8, 6, 4, '肺癌治疗方案很科学，目前效果不错', '2023-06-14 14:40:00'),
(1, 6, 5, '陈医生给了我们很大希望，治疗很专业', '2023-06-21 11:15:00'),
(2, 6, 4, '免疫治疗效果正在观察中，医生很负责', '2023-06-29 16:20:00'),

-- 杨红医生(7)的评价
(3, 7, 5, '白内障手术非常成功，视力恢复得很好', '2023-06-09 09:50:00'),
(4, 7, 5, '杨医生手法轻柔，眼科检查一点也不疼', '2023-06-17 15:25:00'),
(5, 7, 4, '专业且耐心，解释得很清楚', '2023-06-26 10:40:00');

ALTER TABLE doctors ADD COLUMN average_rating FLOAT DEFAULT 0;
ALTER TABLE doctors ADD COLUMN review_count INT DEFAULT 0;