from fastapi import FastAPI, Request
from src.api.routes import admin, public
from src.api.routes import health
from fastapi.responses import JSONResponse
from src.domain.exceptions import DomainError
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import _rate_limit_exceeded_handler
from src.api.limiter import limiter


app = FastAPI(
    title="Projects API",
    description="REST API for managing and exposing portfolio projects.",
    version="1.0.0",
)

app.include_router(admin.router)
app.include_router(public.router)
app.include_router(health.router)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)


@app.get("/")
def root():
    return {"message": "Welcome to my Projects API"}


@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
            }
        },
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "internal_server_error",
                "message": "An unexpected error occurred",
            }
        },
    )
