# Projects API

REST API designed to manage and expose software projects for a personal portfolio.

The system provides a backend for storing project metadata, exposing public endpoints used by the portfolio website, and supporting future administrative tooling.

---

## Live API

**Base URL**  
https://projects-api-production-f245.up.railway.app

**Swagger UI**  
https://projects-api-production-f245.up.railway.app/docs

**Public endpoint**
GET /projects/

Optional query parameters:

- `lang` – filter project descriptions by language
- `limit` – number of projects to return
- `offset` – number of projects to skip (pagination)

Example:
https://projects-api-production-f245.up.railway.app/projects/?lang=en&limit=2&offset=0

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

## Tech Stack

| Category | Technology |
|--------|--------|
| Language | Python |
| Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Validation | Pydantic |
| Testing | Pytest |
| Containerization | Docker |
| Linting | Ruff |
| Security checks | Bandit |
| Code quality | SonarCloud |
| CI/CD | GitHub Actions |
| Deployment | Railway |

---

## Project Vision

The goal of this project is to provide a structured backend for managing and publishing portfolio projects.

The API acts as the data source for a portfolio website while also serving as an internal tool for managing project information.

Future iterations may expand the system with additional capabilities such as authentication, media management, and optional administrative tooling.

---

## Roadmap

| Phase | Scope | Status |
|------|------|------|
| 1. Core API | CRUD operations, service layer, repository pattern, Unit of Work | ✅ Implemented |
| 2. Public Portfolio API | Endpoints exposing published projects | ✅ Implemented |
| 3. API Hardening | Rate limiting and pagination | ✅ Implemented |
| 4. Project Media | Support for project images and galleries | ⏳ Planned |
| 5. Authentication | JWT authentication for admin routes | ⏳ Planned |
| 6. Test Expansion | Broader automated test coverage | ⏳ Planned |
