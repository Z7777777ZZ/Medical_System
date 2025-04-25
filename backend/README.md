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

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for detailed API documentation.

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