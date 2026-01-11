# Admin Backend - Paint Research Center

This is the Flask-based backend API for the Paint Research Center administrative panel. It provides authentication, data management, and institutional communication features.

## Prerequisites

- **Python 3.8.10** installed on your system
- **PostgreSQL 12+** running and accessible on `localhost:5432`
- **Poetry** (Python dependency manager)

## Installation & Setup

All commands should be executed from the `/admin` directory unless otherwise specified.

### 1. Navigate to the Admin Directory

```bash
cd /path/to/admin
```

### 2. Create a Python Virtual Environment

If you don't already have a virtual environment set up, create one using Python 3.8.10:

```bash
python3.8 -m venv .venv
source .venv/bin/activate   # On macOS/Linux
# or
.venv\Scripts\activate       # On Windows
```

### 3. Install Dependencies

Use Poetry to install all required dependencies:

```bash
poetry install
```

### 4. Set Up Environment Variables

The project uses a `.envrc` file to manage environment variables. You can either:

**Option A: Using direnv (recommended)**
- Install direnv: `brew install direnv`
- The `.envrc` file will be automatically loaded when you enter the `/admin` directory

**Option B: Manually source the file**
```bash
source .envrc
```

**Option C: Set variables in your shell**
Copy the `.envrc` file and fill in the values with your configuration:

```bash
export DB_USER="your_database_user"
export DB_PASS="your_database_password"
export DB_HOST="localhost"
export DB_NAME="your_database_name"
export SECRET_KEY="your_secret_key"
export JWT_SECRET_KEY="your_jwt_secret_key"
export MAIL_USERNAME="your_email@gmail.com"
export MAIL_PASSWORD="your_email_app_password"
export GOOGLE_CLIENT_ID="your_google_client_id"
export GOOGLE_CLIENT_SECRET="your_google_client_secret"
export OAUTH_SENDER="your_oauth_sender_email@gmail.com"
export ENDPOINT_DB_USER="your_endpoint_user"
export ENDPOINT_DB_PASSWORD="your_endpoint_password"
```

### 5. Create the PostgreSQL Database

Before running the application, create the database. Use the values from your `.envrc` file:

```bash
psql -h localhost -U postgres -c "CREATE DATABASE $DB_NAME;"
```

Or with your specific user:

```bash
psql -h localhost -U $DB_USER -c "CREATE DATABASE $DB_NAME;"
```

## Running the Application

All commands should be executed from the `/admin` directory.

### 1. Load Environment Variables

If you haven't already, load your `.envrc` file:

```bash
source .envrc
```

### 2. Reset the Database

To drop all tables and recreate them from scratch:

```bash
poetry run flask resetdb
```

### 3. Seed Sample Data

To populate the database with initial data and test users:

```bash
poetry run flask seedsdb
```

### 4. Start the Flask Development Server

Run the application with SSL context (adhoc):

```bash
poetry run flask run
```

The server will start at `https://127.0.0.1:5000`

To run on a different port:

```bash
poetry run flask run --port=5001
```

## Login Credentials

After seeding the database, you can log in with the following test account:

- **Email**: `boca@gmail.com`
- **Password**: `123`

## Project Structure

```
admin/
├── src/
│   ├── core/              # Core application logic
│   ├── web/               # Flask app factory and routes
│   │   ├── __init__.py    # Application factory (create_app)
│   │   ├── routes/        # API endpoints
│   │   ├── models/        # SQLAlchemy models
│   │   └── schemas/       # Marshmallow schemas
│   └── tests/             # Unit tests
├── app.py                 # Application entry point
├── pyproject.toml         # Poetry dependencies
└── README.md              # This file
```

## Available Commands

All commands should be executed from the `/admin` directory:

```bash
# Load environment variables
source .envrc

# Run the development server
poetry run flask run

# Enter Flask shell
poetry run flask shell

# Reset the database (drop all tables and recreate)
poetry run flask resetdb

# Seed sample data
poetry run flask seedsdb

# Format code
poetry run black src/
```

## Troubleshooting

### PostgreSQL Connection Error

If you get `connection refused` on port 5432:

```bash
# Check if PostgreSQL is running
brew services list

# Start PostgreSQL (macOS with Homebrew)
brew services start postgresql

# Or verify the connection
psql -h localhost -U $DB_USER
```

### Port Already in Use

If port 5000 is already in use:

```bash
poetry run flask run --port=5001
```

### Database Errors

If you have database errors, reset everything:

```bash
poetry run flask resetdb
poetry run flask seedsdb
```

### Virtual Environment Issues

If your dependencies aren't loading correctly:

```bash
deactivate
source .venv/bin/activate
poetry install
```

## Development Notes

- The application uses Flask-SQLAlchemy for ORM operations
- Authentication is handled with Flask-JWT-Extended for API tokens
- Email functionality requires proper SMTP configuration
- CORS is enabled for frontend communication with the Vue.js portal

## Next Steps

Once the backend is running, start the frontend portal by following the instructions in `portal/README.md`.

