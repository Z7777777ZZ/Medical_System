# Medical System Backend

## Project Structure

```
backend/
├── api/                    # API routes
│   ├── __init__.py
│   ├── auth.py            # Authentication routes
│   ├── queue.py           # Queue management routes
│   └── prescription.py    # Prescription management routes
├── models/                # Database models
│   ├── __init__.py
│   ├── base.py           # Base model with common fields
│   ├── queue.py          # Queue model
│   └── prescription.py   # Prescription model
├── call_number/          # 叫号系统模块
│   ├── api/              # API routes for queue management
│   │   ├── __init__.py
│   │   └── queue.py      # Queue API
│   ├── models/           # Queue models
│   │   └── queue.py      # Queue model
│   └── services/         # Queue services
│       └── queue_service.py  # Queue service implementation
├── diagnosis/            # 诊断与处方模块
│   ├── api/              # API routes for diagnosis
│   │   ├── __init__.py
│   │   └── prescription.py # Prescription API
│   ├── models/           # Diagnosis models
│   │   └── prescription.py # Prescription model
│   └── services/         # Diagnosis services
│       └── prescription_service.py # Prescription service implementation
├── config.py             # Configuration settings
├── app.py               # Application factory
├── requirements.txt     # Python dependencies
├── schema.sql          # Database schema
└── API_DOCUMENTATION.md # API documentation
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the backend directory with:
```
SECRET_KEY=your-secret-key
DATABASE_URL=mysql+pymysql://username:password@localhost/medical_system
JWT_SECRET_KEY=your-jwt-secret-key
```

4. Initialize the database:
```bash
mysql -u username -p < schema.sql
```

5. Run the application:
```bash
python app.py
```

## API Documentation

API documentation is available through Swagger UI at `/docs` endpoint when the application is running.

## API Overview

### 叫号系统 API

- `POST /api/call-number/queue/register` - 注册患者进入队列
- `GET /api/call-number/queue/status/<patient_id>` - 获取患者队列状态
- `GET /api/call-number/queue/clinic/<clinic_id>` - 获取诊所信息
- `GET /api/call-number/queue/current` - 获取当前叫号患者
- `GET /api/call-number/queue/list` - 获取当前队列列表
- `POST /api/call-number/queue/refresh/<patient_id>` - 刷新患者队列状态

### 处方系统 API

- `GET /api/diagnosis/prescription/medicines` - 获取所有药品列表
- `GET /api/diagnosis/prescription/medicines/<medicine_id>` - 获取药品详情
- `POST /api/diagnosis/prescription` - 创建新处方
- `GET /api/diagnosis/prescription?patientId=<patient_id>` - 获取患者的所有处方
- `GET /api/diagnosis/prescription/<prescription_id>` - 获取处方详情
- `PUT /api/diagnosis/prescription/<prescription_id>` - 更新处方信息

## Development Guidelines

1. **Code Style**
   - Follow PEP 8 guidelines
   - Use type hints where appropriate
   - Document all public functions and classes

2. **Database Changes**
   - All database changes should be documented in schema.sql
   - Use migrations for database schema changes
   - Test migrations before deploying

3. **API Development**
   - Follow RESTful principles
   - Use appropriate HTTP methods
   - Include proper error handling
   - Document all endpoints

4. **Testing**
   - Write unit tests for all new features
   - Test API endpoints with Postman or similar tools
   - Test database operations

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Write tests
4. Update documentation
5. Submit a pull request

## License

This project is licensed under the MIT License.