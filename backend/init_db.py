import pymysql
import os
from datetime import datetime, date

def format_date(value):
    if isinstance(value, (datetime, date)):
        return value.strftime('%Y-%m-%d')
    return value

def execute_sql_file():
    # 读取 SQL 文件
    with open('data.txt', 'r', encoding='utf-8') as f:
        sql_commands = f.read()
    
    # 连接数据库
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='zsj031128',  # 修改为与 config.py 相同的密码
        charset='utf8mb4'
    )
    
    try:
        with connection.cursor() as cursor:
            # 执行 SQL 命令
            for command in sql_commands.split(';'):
                if command.strip():
                    try:
                        cursor.execute(command)
                        print(f"Successfully executed: {command[:50]}...")
                    except Exception as e:
                        print(f"Error executing command: {command[:50]}...")
                        print(f"Error: {str(e)}")
        connection.commit()
        print("SQL file executed successfully!")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        connection.close()

if __name__ == '__main__':
    execute_sql_file() 