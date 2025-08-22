from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import PROJECT_NAME, API_V1_STR
from .api.endpoints import auth, analysis

app = FastAPI(title=PROJECT_NAME)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=f"{API_V1_STR}/auth", tags=["auth"])
app.include_router(analysis.router, prefix=f"{API_V1_STR}/analysis", tags=["analysis"])

@app.get("/")
def read_root():
    return {"message": f"Bem-vindo à API do {PROJECT_NAME}"}