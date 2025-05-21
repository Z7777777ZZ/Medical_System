from flask import Flask
from flask import request, jsonify
from flask_cors import CORS  # 跨域支持
# from aidg.api.doctor_find import doctor_find_bp
from aidg.services.ai_service import DeepSeekService
from config import Config
from flask_sqlalchemy import SQLAlchemy
import re

app = Flask(__name__)

app.config.from_object(Config)

CORS(app)  # 允许跨域请求

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:123456@localhost:3306/medical_system"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# def create_app():
#     app = Flask(__name__)
    
#     # 配置跨域（如果需要）
#     CORS(app)
    
#     # 配置数据库等其他设置
#     app.config.from_pyfile('config.py')
    
#     # 注册蓝图
#     app.register_blueprint(doctor_find_bp, url_prefix='/api/doctors')
    
#     return app

# app = create_app()

@app.route('/')
def home():
    """首页"""
    return "Hello, Flask!"

# 医生模型 SQLAlchemy 默认使用 ​​类名的小写蛇形命名（snake_case）​​ 作为表名
class Doctor(db.Model):
    __tablename__ = 'doctors' # 显式指定该模型对应的数据库表名为 doctors
    doctor_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    phone = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    hospital_id = db.Column(db.BigInteger, db.ForeignKey('hospitals.hospital_id'), nullable=False)
    department_id = db.Column(db.BigInteger, db.ForeignKey('departments.department_id'), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    # 定义关系
    hospital = db.relationship('Hospital', backref='doctors')
    department = db.relationship('Department', backref='doctors')

    def to_dict(self):
        return {
            # 'doctor_id': self.doctor_id,
            'phone': self.phone,
            'name': self.name,
            # 'hospital_id': self.hospital_id,
            'hospital': self.hospital.name if self.hospital else None,
            # 'department_id': self.department_id,
            'department': self.department.name if self.department else None,
            'specialty': self.specialty,
            'bio': self.bio,
            # 'password_hash': self.password_hash,
            # 'created_at': self.created_at
        }
    
# 医院模型
class Hospital(db.Model):
    __tablename__ = 'hospitals'
    hospital_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)

# 科室模型
class Department(db.Model):
    __tablename__ = 'departments'
    department_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    hospital_id = db.Column(db.BigInteger, db.ForeignKey('hospitals.hospital_id'), nullable=False)

@app.route('/api/doctors/search', methods=['GET'])
def search_doctors():
    search_term = request.args.get('query', '').strip().lower()

    if not search_term:
        doctors = Doctor.query.all()
        return jsonify([doctor.to_dict() for doctor in doctors])
        # return jsonify({"error": "查询参数不能为空"}), 400
    
    query = Doctor.query.join(Hospital).join(Department)

    query = query.filter(
        db.or_(
            Doctor.name.ilike(f'%{search_term}%'),
            Hospital.name.ilike(f'%{search_term}%'),
            Department.name.ilike(f'%{search_term}%'),
            Doctor.specialty.ilike(f'%{search_term}%')
        )
    )

    doctors = query.all()
    return jsonify([doctor.to_dict() for doctor in doctors])

@app.route('/api/aidiagnosis', methods=['POST'])
def ai_diagnosis():
    """处理聊天请求的API端点"""
    data = request.get_json()
    prompt = data.get('prompt', '')
    
    if not prompt:
        return jsonify({"error": "Prompt不能为空"}), 400
    
    # 获取科室信息
    # departments = ['内科', '外科', '妇产科', '儿科', '骨科', '心脏内科', '神经内科', '急诊科', '肿瘤科', '眼科']
    # Department_str = '、'.join(departments)

    # 获取所有医生信息用于AI参考
    doctors = Doctor.query.join(Hospital).join(Department).all()
    doctor_info = "\n".join([
        f"医生ID: {d.doctor_id}, 医生: {d.name}, 医院: {d.hospital.name}, 科室: {d.department.name}, 专长: {d.specialty}"
        for d in doctors
    ])
    
    try:
        # 调用DeepSeek服务 - 现在直接返回字符串响应
        # prompt += "回答要求如下：首先给出可能疾病（以“可能疾病”开头，疾病之间用“、”分隔），然后给出建议（建议分点列出），最后直接给出紧急程度（以“紧急程度”开头，紧急程度分为低、中、高）及其备注，三项内容之间用---分割。"
        # prompt += "回答要求如下：首先给出可能疾病（以“可能疾病”开头，疾病之间用“、”分隔），然后给出建议（建议分点列出），接着直接给出紧急程度（以“紧急程度”开头，紧急程度分为低、中、高）及其备注，最后根据诊断结果给出推荐科室"
        # prompt += "（以“推荐科室”开头，科室之间用“、”分隔，科室请从[" + Department_str + "]中选择）"
        # prompt += "，四项内容之间用---分割。"

        prompt += "回答要求如下：首先给出可能疾病（以“可能疾病”开头，疾病之间用“、”分隔），然后给出建议（建议分点列出），接着直接给出紧急程度（以“紧急程度”开头，紧急程度分为低、中、高）及其备注，最后根据诊断结果推荐不超过3位最适合的医生"
        prompt += "（以“推荐医生”开头，给出医生信息（ID和名字必须给出），参考输出格式为“1-张伟（北京协和医院-内科，呼吸系统疾病相关症状评估）”，每行给出一个医生，可选的医生信息如下："
        prompt += doctor_info + "）"
        prompt += "，四项内容之间用---分割。"
        
        # 构建更详细的提示词，包含医生信息
        # prompt += """
        # 回答要求如下：
        # 1. 首先给出可能疾病（以"可能疾病:"开头，疾病之间用"、"分隔）
        # 2. 然后给出建议（建议分点列出）
        # 3. 直接给出紧急程度（以"紧急程度:"开头，紧急程度分为低、中、高）及其备注
        # 4. 最后根据诊断结果推荐3位最适合的医生（以"推荐医生:"开头）
        
        # 可选的医生信息如下：
        # """ + doctor_info + """
        
        # 请按照以下格式返回：
        # 可能疾病: 疾病1、疾病2、疾病3
        # ---
        # 建议:
        # 1. 建议1
        # 2. 建议2
        # 3. 建议3
        # ---
        # 紧急程度: 中
        # 备注: 这是备注信息
        # ---
        # 推荐医生: 
        # 1. 医生A (医院X, 科室Y, 专长Z)
        # 2. 医生B (医院X, 科室Y, 专长Z)
        # 3. 医生C (医院X, 科室Y, 专长Z)
        # """

        raw_response = DeepSeekService.generate_response(prompt)
        print(raw_response)

        # 初始化结构化结果
        structured_response = {
            "possibleDiseases": [],
            "suggestions": [],
            "urgencyLevel": "",
            "urgencyNote": "", 
            "recommendedDoctors": []  # 新增推荐医生列表
        }

        # 按章节分割响应内容
        sections = [section.strip() for section in raw_response.split('---')]

        # 1. 解析"可能疾病"部分（格式：心绞痛、胃食管反流病、肋软骨炎...）
        if len(sections) > 0:
            disease_section = sections[0]
            # 提取冒号后的内容，并按逗号分隔
            if '可能疾病：' in disease_section:
                diseases_part = disease_section.split('可能疾病：')[-1].strip()
                structured_response["possibleDiseases"] = [
                    disease.strip() 
                    for disease in diseases_part.split('、')
                    if disease.strip()
                ]
        
        # 2. 解析"建议"部分（带数字序号列表）
        if len(sections) > 1:
            suggestion_section = sections[1]
            for line in suggestion_section.split('\n'):
                line = line.strip()
                # 提取带数字序号的建议（如"1. **尽早就医**：..."）
                if line and line[0].isdigit():
                    # 移除序号和Markdown标记
                    suggestion = line.split('.', 1)[-1].strip()
                    suggestion = suggestion.replace('**', '').strip()
                    if suggestion:
                        structured_response["suggestions"].append(suggestion)
        
        # 3. 解析紧急程度和备注
        if len(sections) > 2:
            urgency_section = sections[2]
            # 提取紧急程度（格式：**紧急程度：中**）
            if '紧急程度：' in urgency_section:
                urgency_level = urgency_section.split('紧急程度：')[-1].strip()
                if '备注：' in urgency_level:
                    urgency_level = urgency_level.split('备注：')[0].strip()
                # structured_response["urgencyLevel"] = urgency_part.split('**')[0].strip()
                structured_response["urgencyLevel"] = urgency_level.replace('**', '').replace('(', '').strip()
            
            # 提取备注（格式：备注：...）
            if '备注：' in urgency_section:
                urgency_note = urgency_section.split('备注：')[-1].strip()
                structured_response["urgencyNote"] = urgency_note.replace('**', '').replace('(', '').replace(')', '').strip()

        # 解析推荐科室，给出推荐医生
        # if len(sections) > 3:
        #     department_section = sections[3]
        #     # 提取推荐科室（格式：推荐科室：内科、外科、妇产科...）
        #     if '推荐科室：' in department_section:
        #         department_part = department_section.split('推荐科室：')[-1].strip()
        #         # structured_response["departments"] = [
        #         #     department.strip() 
        #         #     for department in department_part.split('、')
        #         #     if department.strip()
        #         # ]
        #         rec_departments = [d.strip() for d in department_part.split('、') if d.strip()]

        #         # 查询每个推荐科室的医生（最多3个）
        #         recommended_doctors = []
        #         for dept_name in rec_departments[:3]:  # 最多处理前3个推荐科室
        #             # 查询科室
        #             department = Department.query.filter_by(name=dept_name).first()
        #             if department:
        #                 # 查询该科室的医生（随机取最多3个）
        #                 doctors = Doctor.query.filter_by(department_id=department.department_id)\
        #                                       .order_by(db.func.random())\
        #                                       .limit(3)\
        #                                       .all()
        #                 for doctor in doctors:
        #                     recommended_doctors.append(doctor.to_dict())
                
        #         # 去重并限制总数不超过3个
        #         unique_doctors = []
        #         seen_doctors = set()
        #         for doctor in recommended_doctors:
        #             doctor_key = (doctor['name'], doctor['hospital'], doctor['department'])
        #             if doctor_key not in seen_doctors:
        #                 seen_doctors.add(doctor_key)
        #                 unique_doctors.append(doctor)
        #                 if len(unique_doctors) >= 3:
        #                     break
                
        #         structured_response["recommendedDoctors"] = unique_doctors

        # 解析推荐医生
        if len(sections) > 3:
            doctor_section = sections[3]
            if '推荐医生：' in doctor_section:
                # print(doctor_section)
                # 提取医生推荐部分
                doctor_lines = [line.strip() for line in doctor_section.split('\n') if line.strip()]
                doctor_lines = doctor_lines[1:]  # 跳过"推荐医生:"行

                # print(doctor_lines)
                
                # 解析每位医生信息
                for line in doctor_lines[:3]:  # 最多取3位医生
                    # print(line)
                    if line and line[0].isdigit():  # 检查是否是带序号的医生行
                        # 获取医生id，取最前面的数字
                        # extract_leading_number
                        match = re.match(r'^\d+', line)  # 匹配开头的数字
                        doctor_id = match.group() if match else None
                        
                        # 根据id提取医生信息
                        if doctor_id:
                            doctor = Doctor.query.filter_by(doctor_id=doctor_id).first()
                            if doctor:
                                structured_response["recommendedDoctors"].append(doctor.to_dict())

                        # # 提取医生信息
                        # doctor_info = line.split('.', 1)[-1].strip()
                        # # 解析医生姓名、医院、科室、专长
                        # parts = [p.strip() for p in doctor_info.split(',')]
                        # if len(parts) >= 3:
                        #     name = parts[0].split('(')[0].strip()
                        #     hospital = parts[1].split(':')[-1].strip()
                        #     department = parts[2].split(':')[-1].strip()
                        #     specialty = parts[3].split(':')[-1].strip() if len(parts) > 3 else ""
                            
                        #     structured_response["recommendedDoctors"].append({
                        #         "name": name,
                        #         "hospital": hospital,
                        #         "department": department,
                        #         "specialty": specialty
                        #     })

        print(structured_response)

        return jsonify(structured_response)
        
    except Exception as e:
        app.logger.error(f"处理聊天请求失败: {str(e)}")
        return jsonify({"error": "处理请求时发生错误"}), 500

if __name__ == '__main__':
    # 测试deepseek服务
    with app.app_context():  # 添加应用上下文
        prompt = "你好，医生，我最近感觉胸口疼痛，已经持续了一个星期了，应该怎么办？"
        prompt += "回答要求如下：首先给出可能疾病（疾病之间用“、”分隔），然后给出建议（建议分点列出），最后直接给出紧急程度（低、中、高）及其备注，三项内容之间用---分割。"
        """
        可能疾病：心绞痛、胃食管反流、肋软骨炎、胸膜炎、焦虑症  
        ---
        建议：
        1. **尽早就医检查**：立即到心内科或急诊科就诊，完善心电图、心肌酶、胸部CT等检查，排除心血管或肺部疾病。
        2. **观察症状特征**：记录疼痛性质（钝痛、刺痛、烧灼感）、持续时间、诱发因素（运动、进食、情绪等）及伴随症状（呼吸困难、恶心、出汗等）。
        3. **避免剧烈活动**：在明确病因前减少体力劳动，保持情绪稳定。
        4. **调整饮食**：避免辛辣、油腻食物，少量多餐，减少胃酸反流风险。
        5. **紧急情况处理**：若出现持续剧烈胸痛（＞20分钟）、呼吸急促、晕厥等症状，立即拨打急救电话。
        ---
        紧急程度：**中**
        备注：胸痛可能为严重疾病信号（如心绞痛、肺栓塞），尤其合并高血压、糖尿病、吸烟史者需高度警惕，建议24小时内就医。
        """
        
        """
        **可能疾病**：  
        1. **心绞痛/冠心病**（尤其疼痛与活动相关）
        2. **胃食管反流病/胃炎**（伴随烧心、反酸）
        3. **肋软骨炎/肌肉拉伤**（局部按压痛或特定动作诱发）
        4. **肺部疾病**（如肺炎、气胸，可能伴随咳嗽、呼吸困难）
        5. **焦虑症**（伴随心悸、紧张感）

        **建议**：
        1. **立即就医**：建议前往医院心内科或急诊，完善心电图、心肌酶、胸部CT等检查。
        2. **观察症状**：记录疼痛性质（钝痛/刺痛/压迫感）、持续时间、诱因（如运动、进食后）及伴随症状（出汗、恶心、肩背放射痛）。
        3. **避免风险行为**：暂停剧烈运动、吸烟、饮酒，保持情绪稳定。

        **紧急程度**：**中**（需24-48小时内就诊，若出现持续剧烈胸痛、呼吸困难、晕厥则升级为**高**紧急度）。
        """

        """
        可能疾病：心绞痛、胃食管反流、肋软骨炎、肌肉拉伤、肺部或胸膜疾病（如肺炎、气胸）等。  
        ---
        建议：1. 立即停止活动并休息；2. 若伴随呼吸困难、恶心、晕厥、左臂放射痛或冷汗，需立即急诊；3. 若无上述症状但持续不缓解，建议24小时内就诊心内科或胸外科；4. 避免自行服用药物（如阿司匹林）或剧烈运动。
        ---
        紧急程度：中（若伴随上述危险症状则为高）
        """

        # response = DeepSeekService.generate_response(prompt)
        # print(response)

        """
        # 调用DeepSeek服务 - 现在直接返回字符串响应
        raw_response = DeepSeekService.generate_response(prompt)
        print(raw_response)

        # 初始化结构化结果
        structured_response = {
            "possibleDiseases": [],
            "suggestions": [],
            "urgencyLevel": "",
            "urgencyNote": ""
        }

        # 按章节分割响应内容
        sections = [section.strip() for section in raw_response.split('---')]

        # 1. 解析"可能疾病"部分（格式：心绞痛、胃食管反流病、肋软骨炎...）
        if len(sections) > 0:
            disease_section = sections[0]
            # 提取冒号后的内容，并按逗号分隔
            if '可能疾病：' in disease_section:
                diseases_part = disease_section.split('可能疾病：')[-1].strip()
                structured_response["possibleDiseases"] = [
                    disease.strip() 
                    for disease in diseases_part.split('、')
                    if disease.strip()
                ]
        
        # 2. 解析"建议"部分（带数字序号列表）
        if len(sections) > 1:
            suggestion_section = sections[1]
            for line in suggestion_section.split('\n'):
                line = line.strip()
                # 提取带数字序号的建议（如"1. **尽早就医**：..."）
                if line and line[0].isdigit():
                    # 移除序号和Markdown标记
                    suggestion = line.split('.', 1)[-1].strip()
                    suggestion = suggestion.replace('**', '').strip()
                    if suggestion:
                        structured_response["suggestions"].append(suggestion)
        
        # 3. 解析紧急程度和备注
        if len(sections) > 2:
            urgency_section = sections[2]
            # 提取紧急程度（格式：**紧急程度：中**）
            if '紧急程度：' in urgency_section:
                urgency_level = urgency_section.split('紧急程度：')[-1].strip()
                if '备注：' in urgency_level:
                    urgency_level = urgency_level.split('备注：')[0].strip()
                # structured_response["urgencyLevel"] = urgency_part.split('**')[0].strip()
                structured_response["urgencyLevel"] = urgency_level.replace('**', '').strip()
            
            # 提取备注（格式：备注：...）
            if '备注：' in urgency_section:
                urgency_note = urgency_section.split('备注：')[-1].strip()
                structured_response["urgencyNote"] = urgency_note.replace('**', '').strip()

        print(structured_response)
        """

    app.run(debug=True)