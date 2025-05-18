-- 用户行为时间轴表
CREATE TABLE `user_activities` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `patient_id` BIGINT NOT NULL COMMENT '用户ID',
  `activity_type` VARCHAR(50) NOT NULL COMMENT '活动类型(login, appointment, feedback, view_record等)',
  `description` TEXT NOT NULL COMMENT '活动描述',
  `metadata` JSON DEFAULT NULL COMMENT '活动元数据，如关联ID等',
  `ip_address` VARCHAR(50) DEFAULT NULL COMMENT 'IP地址',
  `user_agent` VARCHAR(255) DEFAULT NULL COMMENT '用户代理信息',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户活动记录表';

-- 就诊体验反馈表
CREATE TABLE `treatment_feedbacks` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `patient_id` BIGINT NOT NULL COMMENT '患者ID',
  `appointment_id` BIGINT DEFAULT NULL COMMENT '关联预约ID',
  `treatment_rating` INT(1) NOT NULL COMMENT '就诊体验总评分',
  `doctor_rating` INT(1) NOT NULL COMMENT '医生评分',
  `hospital_rating` INT(1) NOT NULL COMMENT '医院环境评分',
  `waiting_rating` INT(1) NOT NULL COMMENT '等待时间评分',
  `content` TEXT NOT NULL COMMENT '详细反馈内容',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '提交时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='就诊体验反馈表';

-- 康复情况反馈表
CREATE TABLE `recovery_feedbacks` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `patient_id` BIGINT NOT NULL COMMENT '患者ID',
  `medical_record_id` BIGINT DEFAULT NULL COMMENT '关联病历ID',
  `recovery_status` ENUM('worse', 'same', 'better', 'cured') NOT NULL COMMENT '康复状态',
  `symptom_description` TEXT NOT NULL COMMENT '当前症状描述',
  `medication_adherence` ENUM('good', 'moderate', 'poor') NOT NULL COMMENT '服药依从性',
  `side_effects` TEXT DEFAULT NULL COMMENT '药物副作用',
  `content` TEXT DEFAULT NULL COMMENT '其他反馈内容',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '提交时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='康复情况反馈表';

-- 系统消息表
CREATE TABLE `notifications` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `patient_id` BIGINT NOT NULL COMMENT '患者ID',
  `title` VARCHAR(100) NOT NULL COMMENT '消息标题',
  `content` TEXT NOT NULL COMMENT '消息内容',
  `type` ENUM('appointment', 'medication', 'followup', 'health_tip', 'system') NOT NULL COMMENT '消息类型',
  `reference_id` BIGINT DEFAULT NULL COMMENT '相关联ID，如预约ID等',
  `delivery_method` VARCHAR(50) NOT NULL DEFAULT 'app' COMMENT '发送方式(app,sms,email)',
  `status` ENUM('pending', 'sent', 'read') NOT NULL DEFAULT 'pending' COMMENT '消息状态',
  `scheduled_time` DATETIME NOT NULL COMMENT '计划发送时间',
  `sent_time` DATETIME DEFAULT NULL COMMENT '实际发送时间',
  `read_time` DATETIME DEFAULT NULL COMMENT '阅读时间',
  FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统消息表';

-- 新手引导进度表
CREATE TABLE `guide_progress` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `patient_id` BIGINT NOT NULL COMMENT '患者ID',
  `guide_key` VARCHAR(50) NOT NULL COMMENT '引导类型',
  `current_step` INT NOT NULL DEFAULT 0 COMMENT '当前步骤',
  `is_completed` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否完成',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  UNIQUE KEY `uk_patient_guide` (`patient_id`, `guide_key`),
  FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='新手引导进度表';

-- 健康贴士表
CREATE TABLE `health_tips` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `title` VARCHAR(100) NOT NULL COMMENT '标题',
  `content` TEXT NOT NULL COMMENT '内容',
  `source` VARCHAR(100) DEFAULT NULL COMMENT '来源',
  `publish_date` DATE NOT NULL COMMENT '发布日期',
  `is_active` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否激活',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='健康贴士表';

-- 通知设置表
CREATE TABLE `notification_settings` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `patient_id` BIGINT NOT NULL COMMENT '患者ID',
  `app_enabled` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否启用应用内通知',
  `sms_enabled` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否启用短信通知',
  `email_enabled` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否启用邮件通知',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  UNIQUE KEY `uk_patient_id` (`patient_id`),
  FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='通知设置表';

-- 索引添加
ALTER TABLE user_activities ADD INDEX idx_patient_activity_type (patient_id, activity_type);
ALTER TABLE user_activities ADD INDEX idx_activity_created_at (created_at);
ALTER TABLE notifications ADD INDEX idx_patient_status (patient_id, status);
ALTER TABLE notifications ADD INDEX idx_scheduled_time (scheduled_time); 