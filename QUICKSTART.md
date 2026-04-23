# Quick Start Guide

## Prerequisites
- Python 3.9+
- PostgreSQL database (or update DATABASE_URL in .env)
- Virtual environment (venv/virtualenv)

## Installation Steps

### 1. Setup Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\Activate.ps1
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Setup
```bash
# Run migration to create tables
python migrate.py

# Create demo admin user (optional)
python create_demo_user.py
```

### 4. Environment Configuration
Create a `.env` file in the project root (already exists):
```
DATABASE_URL=postgresql://user:password@localhost/ecommerce
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### 5. Run the Application
```bash
# Start development server
uvicorn src.main:app --reload --port 8000

# Or using the provided task
# Press Ctrl+Shift+B in VS Code and select "Run FastAPI Server"
```

The application will be available at: `http://localhost:8000`

## Features Available

### Public Pages
- **Homepage**: `http://localhost:8000/`
- **Products List**: `http://localhost:8000/products`
- **Product Details**: `http://localhost:8000/products/{id}`

### Authentication
- **Login**: `http://localhost:8000/auth/login`
- **Signup**: `http://localhost:8000/auth/signup`
- **Logout**: `http://localhost:8000/auth/logout`

### Admin Panel (Login Required)
- **Add Product**: `http://localhost:8000/admin/add-product`
- **Manage Products**: `http://localhost:8000/admin/products`

## Demo Account

For testing admin features:
- **Username**: admin
- **Password**: admin
- **Email**: admin@example.com

## Testing Authentication Flow

1. Visit `http://localhost:8000/auth/login`
2. Login with demo account (admin/admin)
3. You'll be redirected to products page
4. Visit `http://localhost:8000/admin/add-product` to add products
5. Click "Logout" to end session

## Creating New Users

1. Visit `http://localhost:8000/auth/signup`
2. Fill in username, email, and password
3. Submit the form
4. You'll be redirected to login page
5. Login with your new credentials

## Project Structure

```
ecommerce-backend-design/
├── src/
│   ├── main.py              # FastAPI app entry point
│   ├── models/              # Database models
│   ├── routers/             # API endpoints
│   ├── database/            # Database queries
│   ├── utils/               # Utilities (auth, etc.)
│   ├── views/               # HTML templates
│   ├── public/              # Static files (CSS, JS)
│   └── assets/              # Images and assets
├── migrate.py               # Database migration
├── create_demo_user.py      # Demo user creation
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
└── README.md               # Project documentation
```

## Troubleshooting

### Port Already in Use
```bash
# Use a different port
uvicorn src.main:app --reload --port 8001
```

### Database Connection Error
- Check DATABASE_URL in .env
- Ensure PostgreSQL is running
- Verify database credentials

### Import Errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Module Not Found Errors
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

## API Documentation

Once the server is running, access:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Database Commands

### View Users
```bash
python -c "
from src.database.user_queries import get_user_by_username
user = get_user_by_username('admin')
print(user)
"
```

### Create Additional Admin Users
```bash
python -c "
from src.database.user_queries import create_user
result = create_user('admin2', 'admin2@example.com', 'password', is_admin=True)
print(result)
"
```

## Performance Tips

1. Database Connection Pooling
   - Connection pool is configured in `db_config.py`
   - Pool size: 10, Max overflow: 20

2. Caching
   - Consider adding Redis for session caching
   - Use pagination to limit query results

3. Query Optimization
   - Indexed fields: username, email, category, product_id
   - Use LIMIT for large result sets

## Deployment

For production deployment, refer to:
- [FastAPI Deployment Documentation](https://fastapi.tiangolo.com/deployment/)
- [Render Deployment Guide](https://render.com/docs/deploy-fastapi)
- [Heroku Deployment Guide](https://devcenter.heroku.com/articles/getting-started-with-python)

## Support

For issues or questions:
1. Check the `WEEK3_IMPLEMENTATION.md` for detailed feature documentation
2. Review FastAPI documentation: https://fastapi.tiangolo.com
3. Check PostgreSQL documentation: https://www.postgresql.org/docs/

---

**Last Updated**: April 23, 2026
