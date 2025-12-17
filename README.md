# Projects API

A RESTful API built with **FastAPI** to manage portfolio projects and their related technology stacks, with a strong focus on **clean architecture**, **separation of concerns**, and **backend best practices**.

---

## Features

- Projects CRUD
- Multi-language support (pt / en) for project descriptions
- Many-to-many relationship between projects and technology stacks
- Domain-level validations (status, slug uniqueness, deploy dates)
- Database session dependency injection (FastAPI + SQLAlchemy)
- Layered architecture (router / service / domain)

---

## Architecture

- **Routers**: HTTP endpoints and dependency injection
- **Services**: business logic and orchestration
- **Domain**: domain rules and validations
- **Models**: ORM mappings (SQLAlchemy)
- **Schemas**: input/output contracts (Pydantic)

---

## Tech Stack

- **Python**
- **FastAPI** – API framework
- **SQLAlchemy** – ORM
- **PostgreSQL** – relational database
- **Pydantic** – data validation

---

## What's next:

- Authentication (JWT)
- Structured logging
- Automated tests
- Media management (images and external links per project)
- Deployment

---

## Status

Work in progress.  
The project is under active development, with an emphasis on learning and applying backend engineering best practices.
