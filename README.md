
# Pharmacy Management System - Backend

This is the backend for the **Pharmacy Management System**, built with Django and Django REST Framework (DRF), designed to handle all necessary features and provide secure endpoints for user and role management, medication management, refill requests, and audit logging.

---


## Entity Relationship Diagram (ERD):
![alt erd](https://github.com/ehapsamy0/pyramids_pharmacy_task/blob/main/my_project_schema.png)


## Features

### User Management
- **Registration & Authentication**: Secure JWT-based login and registration with role-based access control.
- **Roles**: Support for two main roles - Patients and Pharmacists, each with specific permissions and views.
- **Role-Based Profiles**: Automated creation of patient or pharmacist profiles upon registration.

### Medication Management
- **Medication List**: Allows patients to view available medications.
- **Refill Requests**: Patients can submit requests for medication refills, and pharmacists can manage pending requests.
- **Pharmacist Dashboard**: Displays pending and completed refills, along with detailed tracking.

### Audit Logging
- **HIPAA Compliance**: Tracks significant actions like user logins, medication requests, and fulfillment with `django-auditlog` for secure monitoring and audit trails.

### API Documentation
- **DRF Spectacular**: Auto-generated API documentation for endpoints, accessible at `/api/docs`.

---

## Setup & Installation

### Prerequisites
- **Docker** and **Docker Compose** installed on your machine.
- **PostgreSQL** database configuration for development and production (configured for AWS RDS or a similar service).

### Environment Variables

Create a `.env` file in the project root and include the following:

```dotenv
# Django settings
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=*

# Database settings
POSTGRES_DB=pharmacy_db
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_HOST=db  # or the RDS endpoint if using AWS
POSTGRES_PORT=5432

# JWT settings
JWT_SECRET_KEY=your-jwt-secret
```

---

## Running the Project with Docker

### Makefile Commands

The provided `Makefile` includes commands to streamline the process of managing Docker containers, running migrations, and interacting with the Django shell. Here’s a summary of each command:

- **Build and Run Containers**:
  - `make up`: Run the containers in the foreground.
  - `make upd`: Run the containers in the background (detached mode).
  - `make build`: Build the containers.

- **Manage Django Project**:
  - `make shell`: Open the Django shell.
  - `make bash`: Open a bash shell in the Django container.
  - `make makemigrations`: Create new database migrations based on model changes.
  - `make migrate`: Apply migrations to the database.
  - `make superuser`: Create a Django superuser for admin access.
  - `make urls`: Show all available URLs in the Django project.
  - `make logs`: View real-time logs for all containers.

- **Testing**:
  - `make test`: Run Django unit tests.
  - `make pytest`: Run tests using pytest.
  - `make mypy`: Run type-checking with mypy.

- **Maintenance**:
  - `make down`: Stop all containers.
  - `make destroy`: Stop and remove all containers with volumes.
  - `make rm_pyc`: Clean up Python cache files.

### Running the Project

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/pharmacy-management-backend.git
   cd pharmacy-management-backend
   ```

2. **Setup `.env`**:
   Create a `.env` file and configure the necessary environment variables.

3. **Run the Project**:
   To build and start the project, use the following command:
   ```bash
   make upbuild
   ```

4. **Access the Application**:
   - **Django API**: Visit `http://localhost:8000` (or the appropriate port configured in `docker-compose.local.yml`).
   - **Admin Panel**: Access at `http://localhost:8000/admin`.
   - **API Documentation**: Available at `/api/docs` for API specs and details.

---

## Project Structure

```plaintext
pharmacy-management-backend/
├── config/
│   ├── settings/               # Django settings (base, local, production)
│   ├── urls.py                 # Main URL configurations
│   └── wsgi.py                 # WSGI configuration
├── apps/
│   ├── users/                  # User management and profiles
│   ├── medications/            # Medication and refill requests
│   └── dashboard/              # Dashboard for pharmacist
├── local.yml                   # Docker Compose configuration for local development
├── Makefile                    # Commands for managing the project
└── README.md                   # Project documentation
```

---

## Troubleshooting

1. **Database Connection Issues**:
   Ensure that the database credentials in `.env` match the configuration in `docker-compose.local.yml`.

2. **Container Startup Failures**:
   Use `make logs` to check logs and identify issues. Rebuild if necessary with `make build`.

3. **Testing Failures**:
   Run `make test` for standard Django tests or `make pytest` if using pytest.

---

## Additional Notes

- **Environment**: This setup is configured for local development (`env=local`), with PostgreSQL as the database.
- **API Security**: JWT tokens are used for authentication, and all sensitive actions are logged for audit purposes.
- **Docker & PostgreSQL**: This project uses Docker to manage containers and can be easily deployed to cloud services like AWS ECS for production with an RDS PostgreSQL instance.

For further details, consult the project’s API documentation or reach out to the maintainer.
