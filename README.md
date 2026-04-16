# Projects API

REST API built as a backend engineering study project, focused on clean architecture, domain rules, and layered design.

Originally created as a backend for a portfolio website, this project evolved into a standalone system to explore backend structure, validation, and application design.

## Overview

This API manages software project data and exposes endpoints for retrieving and maintaining project information.

The focus is to demonstrate:

- clear separation of responsibilities  
- domain logic independent from frameworks  
- structured backend architecture  

---


## Architecture

The application follows a layered structure:

- **API layer** – FastAPI routes
- **Service layer** – application logic and domain rules
- **Repository layer** – database access abstraction
- **Unit of Work** – transaction management

This separation allows domain logic to be tested independently from the web framework and database implementation.

---

## Features

- CRUD operations for projects
- Public endpoints for retrieving published portfolio projects
- Language filtering (`lang`)
- Pagination (`limit`, `offset`)
- Rate limiting on public endpoints
- Domain-focused tests using pytest
- Docker image and Dev Containers for reproducible environments
- Continuous integration with code quality and security checks

---
## Endpoints

### Public Endpoints

**GET /projects/**  
List published projects.

Optional query parameters:
- `lang`
- `limit`
- `offset`

**GET /projects/{project_slug}**  
Retrieve a published project by slug.

Optional query parameters:
- `lang`

### Admin Endpoints

All admin routes require authentication via API key.

**POST /admin/projects/**  
Create a new project.

**GET /admin/projects/**  
List all projects, including unpublished ones.

Optional query parameters:
- `lang`
- `limit`
- `offset`

**GET /admin/projects/{project_id}**  
Retrieve a project by id.

Optional query parameters:
- `lang`

**PATCH /admin/projects/{project_id}**  
Partially update a project.

**DELETE /admin/projects/{project_id}**  
Delete a project.

**POST /admin/projects/{project_id}/publish**  
Publish a project.

### Health Check

**GET /health**  
Returns application status.

---

## Tech Stack

| Category | Technology |
|---|---|
| Language | Python |
| Framework | FastAPI |
| Database | PostgreSQL |
| ORM & Migrations | SQLAlchemy, Alembic |
| Validation | Pydantic |
| Testing | Pytest |
| Containerization | Docker |
| Code Quality & Security | Ruff, Bandit, SonarCloud |
| CI/CD | GitHub Actions |
| Deployment | Railway |

---
## Roadmap

| Phase | Scope | Status |
|------|------|--------|
| 1. Core API | CRUD, layering, Unit of Work | Done |
| 2. Public API | Filtering, pagination | Done |
| 3. Hardening | Rate limiting, validation | Done |
| 4. Configuration | Environment validation (Pydantic) | In Progress |
| 5. Containerization | Docker setup | Done |
| 6. Production Setup | Nginx + Compose | Planned |
| 7. Observability | Logging improvements | Planned |
| 8. Security | Environment and API hardening | Planned |

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
