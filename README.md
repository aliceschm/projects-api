# Projects API

REST API designed to manage and expose software projects for a personal portfolio.

The system provides a backend for storing project metadata, exposing public endpoints used by the portfolio website, and supporting future administrative tooling.

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
- API Key authentication for protected routes
- Domain-focused tests using pytest
- Docker image and Dev Containers for reproducible environments
- Continuous integration with code quality and security checks

---

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Pytest
- Docker
- Ruff
- Bandit
- SonarCloud
- GitHub Actions

---

## Project Vision

The final goal of this project is to provide a complete backend for managing and publishing portfolio projects.

The system will support:

- A public API used by the portfolio website to display projects
- An admin dashboard for managing project data
- Secure authentication for administrative operations
- Automated workflows for maintaining project content

---

## Roadmap

| Phase | Scope | Status |
|------|------|------|
| 1. Core API | CRUD operations, service layer, repository pattern, UoW | ✅ Implemented |
| 2. Public Portfolio API | Endpoints exposing published projects | ✅ Implemented |
| 3. Security Hardening | Rate limiting and stronger API protection | 🔄 Planned |
| 4. Authentication | JWT authentication for admin dashboard | ⏳ Planned |
| 5. Admin Dashboard | Interface for managing portfolio projects | ⏳ Planned |
| 6. Test Expansion | Broader automated test coverage | ⏳ Planned |
