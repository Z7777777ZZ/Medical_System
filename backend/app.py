from flask import Flask
from flask import request, jsonify, render_template
from flask_cors import CORS  # 如果需要跨域支持
# from aidg.api.doctor_find import doctor_find_bp
from aidg.services.ai_service import DeepSeekService
from config import Config

app = Flask(__name__)

app.config.from_object(Config)

CORS(app)  # 允许跨域请求

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

@app.route('/api/aidiagnosis', methods=['POST'])
def chat():
    """处理聊天请求的API端点"""
    data = request.get_json()
    prompt = data.get('prompt', '')
    
    if not prompt:
        return jsonify({"error": "Prompt不能为空"}), 400
    
    try:
        # 调用DeepSeek服务 - 现在直接返回字符串响应
        prompt += "回答要求如下：首先给出可能疾病（疾病之间用“、”分隔），然后给出建议（建议分点列出），最后直接给出紧急程度（低、中、高）及其备注，三项内容之间用---分割。"
        raw_response = DeepSeekService.generate_response(prompt)

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
                structured_response["urgencyLevel"] = urgency_level.replace('**', '').replace('(', '').strip()
            
            # 提取备注（格式：备注：...）
            if '备注：' in urgency_section:
                urgency_note = urgency_section.split('备注：')[-1].strip()
                structured_response["urgencyNote"] = urgency_note.replace('**', '').replace('(', '').replace(')', '').strip()
        
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

    app.run(debug=True)