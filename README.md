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
  !(./AnimatedGif/animatedGif.gif)
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
## Database Design
### Core Entities
#### Artwork

Represents an uploaded artwork.

Fields:

- id (Primary Key)

- title

- image_filename

- comments

Relationships:

- Many-to-many relationship with Tags

### Tag

Represents searchable metadata.

Fields:

- id

- name

Relationships:

- Many-to-many relationship with Artwork

## Many-to-Many Relationship Model

Implemented using an association table:

```
artwork_tags = Table(
    "artwork_tags",
    Base.metadata,
    Column("artwork_id", ForeignKey("artworks.id")),
    Column("tag_id", ForeignKey("tags.id")),
)
```
This allows:

- Flexible tagging

- Efficient search filtering

- Normalized database structure


## Async Database Layer

The application uses SQLAlchemy 2.x async patterns:

### Engine Configuration
```
engine = create_async_engine(DATABASE_URL, echo=True)
Session Factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)
```
Key design decisions:

- expire_on_commit=False prevents unnecessary database refresh queries.

- Async sessions improve request concurrency.

## Dependency Injection
FastAPI dependency injection is used for request-scoped database sessions:
```
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
```
Benefits:

- Prevents session leakage

- Ensures proper cleanup

- Supports concurrent request handling

## Service Layer Pattern

Business logic is isolated inside service modules.

Example:

Tag processing logic is centralized in:
```
services/tag_service.py
```
This prevents:

- Router logic bloat

- Code duplication

- Tight coupling between presentation and domain layers

## Tag Processing

Tags are processed using:

- Normalization (lowercase + trimming)

- Database lookup

- Conditional creation of missing tags

- Relationship assignment

Performance optimizations:

- Single request database lookups

- Reduced ORM round trips

## Image Handling

Uploaded images are:

- Resized using Pillow

- Stored in filesystem storage

Database only stores:

- image_filename

This avoids:

- Database blob storage overhead

- Improves scalability

Image paths are dynamically generated via model properties.

## Frontend Interaction Model

The frontend uses:

- Jinja2 server rendering

- JavaScript event listeners

- Fetch API for updates

- Data is passed to JavaScript using JSON serialization:
```
data-artwork='{{ artwork | tojson | safe }}'
```
This prevents template injection vulnerabilities.

## Pagination Strategy

Pagination is implemented using SQL-level limits:

```
.offset((page - 1) * PAGE_SIZE)
.limit(PAGE_SIZE)
```

Advantages:

- Reduces memory usage

- Improves response performance

## Security Considerations
### Template Security

Uses ```|tojson``` filtering to prevent JavaScript injection.

### Database Safety

- Parameterized ORM queries

- No raw SQL string interpolation

### Environment Configuration

Sensitive values are stored in:
```
.env
```
Loaded using python-dotenv.

## Performance Considerations

Optimizations applied:

- Async database IO

- Lazy loading of relationships

- Reduced ORM query duplication

- Server-side pagination

## Code Organization
```
database/
models/
routers/
schemas/
services/
templates/
static/
```
This follows Python backend best practices.

## Running Locally
Install dependencies

Using uv:
```
uv venv
uv sync
```
## Configure Environment
Create ```.env:```
```
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/artportfolio
```
## Start Application
```
uv run uvicorn main:app --reload
```
Access:
```
http://127.0.0.1:8000
```

## Potential Future Improvements

Possible extensions include:

### Backend

- Full-text search indexing

- Authentication and authorization

- Redis caching layer

- Graph-based tag search ranking

### Frontend

- SPA-style dynamic updates

- Drag and drop uploads

### Infrastructure

- Containerized deployment (Docker)

- Cloud storage integration

## Key Engineering Principles Demonstrated

- Separation of concerns

- Asynchronous request handling

- Relational database normalization

- Secure templating

- Service-oriented backend design

## Author Notes

This project demonstrates practical experience with:

- Modern Python web architecture

- Async database programming

- Full-stack integration patterns

## Portfolio Value

This project demonstrates competency in:

- Backend API design

- Database modeling

- Frontend/backend integration

- Performance-aware web design

