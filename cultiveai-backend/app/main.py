import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import PROJECT_NAME, API_V1_STR
from .api.endpoints import auth, analysis, clients, properties

app = FastAPI(
    title=PROJECT_NAME,
    description="API para análise de pastagens degradadas usando NDVI e IA",
    version="1.0.0"
)

cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
origins = [origin.strip() for origin in cors_origins.split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=f"{API_V1_STR}/auth", tags=["auth"])
app.include_router(clients.router, prefix=f"{API_V1_STR}/clients", tags=["clients"])
app.include_router(properties.router, prefix=f"{API_V1_STR}/properties", tags=["properties"])
app.include_router(analysis.router, prefix=f"{API_V1_STR}/analysis", tags=["analysis"])


@app.on_event("startup")
def on_startup():
    from .db.base import Base
    from .db.session import engine
    Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": f"Bem-vindo à API do {PROJECT_NAME}"}