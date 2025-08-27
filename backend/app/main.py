from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import prompt

app = FastAPI(title="Cognify Backend", version="0.1.0")

# Basic CORS; tighten for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(prompt.router, prefix="/api")

@app.get("/")
def root():
    return {"status": "ok", "service": "cognify-backend"}