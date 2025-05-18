import requests
import json
# from flask import current_app
from config import Config
from openai import OpenAI

class DeepSeekService:
    @staticmethod
    def generate_response(prompt, model="deepseek-chat", max_tokens=2048):
        """
        调用DeepSeek API生成响应
        :param prompt: 用户输入的提示词
        :param model: 使用的模型名称
        :param max_tokens: 最大token数
        :return: API响应内容
        """
        # headers = {
        #     "Authorization": f"Bearer {Config.DEEPSEEK_API_KEY}",
        #     "Content-Type": "application/json"
        # }
        
        # payload = {
        #     "model": model,
        #     "messages": [{"role": "user", "content": prompt}],
        #     "max_tokens": max_tokens
        # }
        
        # try:
        #     response = requests.post(
        #         Config.DEEPSEEK_API_URL,
        #         headers=headers,
        #         data=json.dumps(payload)
        #     )
        #     response.raise_for_status()
        #     return response.json()
        # except requests.exceptions.RequestException as e:
        #     current_app.logger.error(f"DeepSeek API请求失败: {str(e)}")
        #     return {"error": str(e)}
        
        # deepseek api 
        # messages = prompt
        # client = OpenAI(api_key=Config.DEEPSEEK_API_KEY, base_url=Config.DEEPSEEK_API_URL)

        # response = client.chat.completions.create(
        #     model="deepseek-chat",
        #     messages=[
        #         {"role": "system", "content": "你是一位专业的医疗顾问，用中文回答。"},
        #         {"role": "user", "content": messages},
        #     ],
        #     # stream=True,
        # )

        # return response.choices[0].message.content
        

        # for chunk in response:
        #     message = chunk.choices[0].delta.content
        #     yield f"data: {message}\n\n"

        # keys = 'sk-1eac2c03ec0e4cbba82ed465aea18962'

        client = OpenAI(
            # 若没有配置环境变量，用百炼API Key将下行替换为：api_key="sk-xxx",
            api_key = Config.API_KEY,
            base_url = Config.API_URL
        )

        completion = client.chat.completions.create(
            model="deepseek-r1",  # 可按需更换模型名称。
            messages=[
                {'role': 'user', 'content': prompt}
            ]
        )

        # 通过reasoning_content字段打印思考过程
        # print("思考过程：")
        # print(completion.choices[0].message.reasoning_content)

        # 通过content字段打印最终答案
        # print("最终答案：")
        # print(completion.choices[0].message.content)

        return completion.choices[0].message.content