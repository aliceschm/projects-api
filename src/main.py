from fastapi import FastAPI
from src.routers.projects import admin, public
from fastapi.responses import JSONResponse
from src.domain.exceptions import InvalidDeployDateError,SlugAlreadyExistsError, InvalidStatusError, ProjectNotFoundError, ProjectNotPublishableError


app = FastAPI()

app.include_router(admin.router)
app.include_router(public.router)

@app.get("/")
def root():
    return {"message": "Welcome to my Projects API"}

@app.exception_handler(InvalidDeployDateError)
def invalid_deploy_date_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": "Deploy date cannot be in the future"},
    )


@app.exception_handler(SlugAlreadyExistsError)
def slug_exists_handler(request, exc):
    return JSONResponse(
        status_code=409,
        content={"detail": "Slug already exists"},
    )


@app.exception_handler(InvalidStatusError)
def invalid_status_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": "Invalid status"},
    )


@app.exception_handler(ProjectNotFoundError)
def project_not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "Project not found"}
    )

@app.exception_handler(ProjectNotPublishableError)
def project_not_publishable_handler(request, exc):
    return JSONResponse(
        status_code=424,
        content={"detail": str(exc)}
    )