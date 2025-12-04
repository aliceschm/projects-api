from fastapi import FastAPI
from src.routers import routes_projects

app = FastAPI()

app.include_router(routes_projects.router)

@app.get("/")
def root():
    return {"message": "API de projetos do portfólio funcionando!"}
