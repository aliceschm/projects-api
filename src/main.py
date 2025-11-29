from fastapi import FastAPI
from src.routers import projects

app = FastAPI()

app.include_router(projects.router)

@app.get("/")
def root():
    return {"message": "API de projetos do portfólio funcionando!"}
