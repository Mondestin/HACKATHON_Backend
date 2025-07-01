# Campus Access Management System API

A comprehensive FastAPI-based REST API for managing campus access control, room reservations, and user profiles.

## Features

### 🔐 User Management
- User authentication and authorization
- Role-based access control (Admin, Student, Professor)
- Password hashing with bcrypt
- User profile management

### 🎫 Access Control
- Access card management with status tracking (active, lost, disabled)
- Access log tracking for audit trails
- Access simulation and validation
- Location-based access control

### 🏢 Room Management
- Room creation and management
- Capacity tracking and validation
- Location-based room organization
- Room statistics and analytics

### 📅 Room Reservations
- Room booking system with time slots
- Conflict detection and prevention
- Capacity vs. occupancy validation
- Reservation management and tracking

### 👥 Student & Professor Profiles
- Extended user profiles for students and professors
- Academic information management
- Department and class organization
- Contact information tracking

## API Endpoints

### Users (`/api/v1/users`)
- `POST /` - Create a new user
- `GET /` - Get all users (paginated)
- `GET /{user_id}` - Get specific user
- `PUT /{user_id}` - Update user
- `DELETE /{user_id}` - Delete user

### Access Cards (`/api/v1/access-cards`)
- `POST /` - Create a new access card
- `GET /` - Get all access cards (paginated)
- `GET /{card_id}` - Get specific access card
- `GET /user/{user_id}` - Get user's access cards
- `PUT /{card_id}` - Update access card
- `PUT /{card_id}/status` - Update card status
- `DELETE /{card_id}` - Delete access card

### Access Logs (`/api/v1/access-logs`)
- `POST /` - Create access log entry
- `POST /simulate-access` - Simulate access attempt
- `GET /` - Get all access logs (paginated)
- `GET /{log_id}` - Get specific access log
- `GET /card/{card_id}` - Get card's access logs
- `GET /user/{user_id}` - Get user's access logs
- `GET /location/{location}` - Get location's access logs
- `GET /stats/summary` - Get access statistics

### Rooms (`/api/v1/rooms`)
- `POST /` - Create a new room
- `GET /` - Get all rooms (paginated)
- `GET /{room_id}` - Get specific room
- `GET /location/{location}` - Get rooms by location
- `GET /capacity/{min_capacity}` - Get rooms by minimum capacity
- `PUT /{room_id}` - Update room
- `DELETE /{room_id}` - Delete room
- `GET /stats/summary` - Get room statistics

### Reservations (`/api/v1/reservations`)
- `POST /` - Create a new reservation
- `GET /` - Get all reservations (paginated)
- `GET /{reservation_id}` - Get specific reservation
- `GET /room/{room_id}` - Get room's reservations
- `GET /user/{user_id}` - Get user's reservations
- `GET /room/{room_id}/availability` - Check room availability
- `PUT /{reservation_id}` - Update reservation
- `DELETE /{reservation_id}` - Delete reservation
- `GET /stats/summary` - Get reservation statistics

### Students (`/api/v1/students`)
- `POST /` - Create a new student profile
- `GET /` - Get all students (paginated)
- `GET /{student_id}` - Get specific student
- `GET /user/{user_id}` - Get student by user ID
- `GET /class/{class_name}` - Get students by class
- `PUT /{student_id}` - Update student
- `DELETE /{student_id}` - Delete student
- `GET /stats/summary` - Get student statistics

### Professors (`/api/v1/professors`)
- `POST /` - Create a new professor profile
- `GET /` - Get all professors (paginated)
- `GET /{professor_id}` - Get specific professor
- `GET /user/{user_id}` - Get professor by user ID
- `GET /department/{department}` - Get professors by department
- `PUT /{professor_id}` - Update professor
- `DELETE /{professor_id}` - Delete professor
- `GET /stats/summary` - Get professor statistics

## Database Schema

The system uses MySQL/MariaDB with the following main tables:

- **users** - Base user accounts with authentication
- **roles** - Role definitions
- **user_roles** - Many-to-many user-role relationships
- **access_cards** - Physical access cards
- **access_logs** - Access attempt audit trail
- **rooms** - Physical spaces
- **room_reservations** - Room booking system
- **students** - Extended student profiles
- **professors** - Extended professor profiles

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd campus-access-management
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your database configuration
   ```

5. **Initialize database**
   ```bash
   python -m app.database.init_db
   ```

6. **Run the application**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## Environment Variables

Create a `.env` file with the following variables:

```env
# Database Configuration
DATABASE_URL=mysql+pymysql://user:password@localhost/campus_access_db
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_NAME=campus_access_db
DATABASE_USER=user
DATABASE_PASSWORD=password

# Security
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=true
LOG_LEVEL=INFO
```

## Default Admin User

The system creates a default admin user during initialization:
- **Email**: admin@campus.com
- **Password**: admin123

**Important**: Change these credentials in production!

## API Documentation

Once the server is running, you can access:

- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/v1/health

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black .
isort .
```

### Linting
```bash
flake8
```

## Security Features

- Password hashing with bcrypt
- Role-based access control
- Input validation with Pydantic
- SQL injection prevention with SQLAlchemy
- CORS configuration
- Comprehensive error handling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License. 