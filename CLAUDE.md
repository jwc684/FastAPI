# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FastAPI Todo application with user authentication, built using SQLAlchemy ORM and PostgreSQL (production) with support for MySQL and SQLite. The application uses JWT tokens for authentication and includes a web UI with Jinja2 templates.

## Development Commands

### Running the Application
```bash
uvicorn TodoApp.main:app --reload
```

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest TodoApp/test/test_todos.py

# Run with verbose output
pytest -v
```

### Database Migrations (Alembic)
```bash
# Create a new migration
cd TodoApp && alembic revision -m "migration message"

# Run migrations
cd TodoApp && alembic upgrade head

# Rollback migration
cd TodoApp && alembic downgrade -1
```

### Installing Dependencies
```bash
pip install -r requirements.txt
```

## Architecture

### Application Structure

- **TodoApp/main.py**: Main FastAPI application entry point. Mounts static files, includes all routers, and creates database tables on startup. Root path redirects to `/todos/todo-page`.

- **TodoApp/database.py**: Database configuration. Currently configured for PostgreSQL production database. Contains commented configurations for MySQL and SQLite. Uses SQLAlchemy session management with `SessionLocal` factory.

- **TodoApp/models.py**: SQLAlchemy ORM models:
  - `Users`: User accounts with authentication fields (email, username, hashed_password, role, phone_number)
  - `Todos`: Todo items with foreign key to `Users` via `owner_id`

### Router Architecture

All routers follow a pattern of:
1. Pydantic models for request validation
2. `get_db()` dependency for database sessions
3. Separate page endpoints (render templates) and API endpoints (JSON responses)
4. Type-annotated dependencies using `Annotated[...]`

**TodoApp/routers/auth.py**:
- JWT-based authentication using python-jose
- BCrypt password hashing via passlib
- OAuth2 password bearer flow
- `get_current_user()` dependency extracts user from JWT token
- Token expiration: 20 minutes
- Template pages: login, register

**TodoApp/routers/todos.py**:
- User-scoped todo CRUD operations (users only see their own todos)
- All operations require authentication via `user_dependency`
- Template pages: todo list, add todo, edit todo
- Cookie-based auth for template pages, OAuth2 bearer for API endpoints

**TodoApp/routers/admin.py**:
- Admin-only endpoints (role-based access control)

**TodoApp/routers/users.py**:
- User profile management endpoints

### Authentication Flow

1. User credentials → `/auth/token` → JWT access token
2. Token stored in cookie (for web UI) or Authorization header (for API)
3. `get_current_user()` validates token and extracts user info
4. Routers use `user_dependency` to require authentication
5. Template pages check cookies, redirect to login if missing/invalid

### Testing Architecture

**TodoApp/test/utils.py**: Shared test configuration
- SQLite in-memory test database (`testdb.db`)
- `override_get_db()`: Test database session dependency
- `override_get_current_user()`: Mocked user (username: 'jay', id: 1, role: 'admin')
- Fixtures: `test_todo`, `test_user` with automatic cleanup

Test files override the main app's dependencies to use test database and mocked auth.

## Database Configuration

The application supports multiple databases via `TodoApp/database.py`:
- **Production**: PostgreSQL (currently active)
- **Alternative**: MySQL via PyMySQL (commented)
- **Development**: SQLite (commented)

When switching databases, update the `SQLALCHEMY_DATABASE_URL` and uncomment the appropriate engine configuration.

## Static Assets and Templates

- **TodoApp/static/**: CSS and JavaScript files mounted at `/static`
- **TodoApp/templates/**: Jinja2 HTML templates
  - Uses `layout.html` and `navbar.html` for consistent UI
  - Template pages receive `request` and `user` context

## Legacy Files

`books.py` and `books2.py` are example/tutorial files demonstrating basic FastAPI concepts and are not part of the main application.
