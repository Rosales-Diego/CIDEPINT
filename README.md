# Centro de Investigación de Pinturas (Paint Research Center)

## Overview

This project was developed as part of the **Proyecto de Software** course at **Facultad de Informática, Universidad Nacional de La Plata (UNLP)** in 2023.

The application is a web platform designed for a paint research center, enabling users to discover and communicate with different institutions related to paint research and services. The project consists of two main components:

- **Admin** (Backend): Flask-based administrative interface
- **Portal** (Frontend): Vue.js-based public-facing portal

Each component has its own README file with detailed instructions on how to set up and run them.

## Developers

This project was developed by:

- **Diego Rosales**
- **Josue Carrera**
- **Valentin Dome**
- **Vanessa Astrada**

## Technologies Used

### Backend (Admin)
- **Python 3.8.10**
- **Flask** - Web framework
- **PostgreSQL** - Database
- **SQLAlchemy** - ORM
- **Flask-Session** - Session management
- **Flask-Bcrypt** - Password hashing
- **Flask-Mail** - Email functionality
- **Flask-JWT-Extended** - JWT authentication
- **Flask-CORS** - Cross-origin resource sharing
- **Authlib** - OAuth integration
- **Poetry** - Dependency management

### Frontend (Portal)
- **Vue.js 3** - Progressive JavaScript framework
- **Vite** - Build tool and development server
- **Vue Router** - Client-side routing
- **Pinia** - State management
- **Axios** - HTTP client
- **Leaflet** / **Vue3-Leaflet** - Interactive maps
- **Chart.js** / **Vue-ChartJS** - Data visualization
- **Moment.js** - Date/time manipulation

## Project Structure

```
grupo24/
├── admin/          # Backend Flask application
│   ├── src/        # Source code
│   ├── app.py      # Application entry point
│   └── README.md   # Backend setup instructions
├── portal/         # Frontend Vue.js application
│   ├── src/        # Source code
│   └── README.md   # Frontend setup instructions
└── README.md       # This file
```

## Getting Started

To run this project, please refer to the specific README files in each component:

- **Backend**: See [admin/README.md](admin/README.md) for backend setup and running instructions
- **Frontend**: See [portal/README.md](portal/README.md) for frontend setup and running instructions

## Disclaimer

⚠️ **This project is a student work from 2023 and should be considered a learning exercise.**

- **Refactoring needed**: There is significant refactoring work remaining to improve code quality, structure, and maintainability.
- **Incomplete features**: Some functionalities may be incomplete or not fully implemented.
- **Production readiness**: This code is not production-ready and would require additional work, testing, and security hardening before deployment.

## License

This is an academic project developed for educational purposes at UNLP.
