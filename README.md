# Technical Documentation — FastAPI Art Portfolio
## Overview

This project is a **modern asynchronous web application** built with Python and FastAPI to demonstrate:

- Scalable backend architecture

- Async database access

- Many-to-many relational modeling

- Service-layer business logic

- Interactive frontend integration using Jinja2 + JavaScript

The system functions as an **art portfolio management platform** supporting:

- Artwork upload and metadata management

- Tag-based search and filtering

- Pagination

- Image storage and processing
  
## System Architecture

The project follows a **layered architecture pattern**:

```
Presentation Layer
├── Jinja2 Templates
├── JavaScript Fetch API

Application Layer
├── Routers (API endpoints)
├── Services (business logic)

Domain Layer
├── SQLAlchemy ORM models
├── Pydantic schemas

Infrastructure Layer
├── PostgreSQL database
├── Async SQLAlchemy engine
├── File system storage for images
```
Key design goals:

- Separation of concerns

- Testability

- Maintainability

- Async scalability

## Technology Stack
### Backend

- FastAPI

- Python 3.11+

- SQLAlchemy 2.x (Async ORM)

- Asyncpg PostgreSQL driver

### Frontend

- Jinja2 templating

- Bootstrap UI components

- Vanilla JavaScript Fetch API

### Storage

- PostgreSQL relational database

- File system storage for images
