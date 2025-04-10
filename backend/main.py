from db.base import Base
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth
from db.db import engine

app = FastAPI()

origins = ["http://localhost", "http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.get("/")
def root():
    return "Hello, World!!!!"

Base.metadata.create_all(bind=engine)