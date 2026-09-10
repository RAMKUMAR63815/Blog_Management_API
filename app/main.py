from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine

# Import models so SQLAlchemy knows all tables
from . import models

# Import routers
from .routers import auth
from .routers import post
from .routers import comment
from .routers import like


# =========================================================
# CREATE DATABASE TABLES
# =========================================================

Base.metadata.create_all(
    bind=engine
)


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="Blog Management API",
    description=(
        "A mini blogging system built using "
        "FastAPI, SQLite, SQLAlchemy and JWT authentication."
    ),
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():

    return {
        "message": "Blog Management API is running",
        "docs": "/docs"
    }


# =========================================================
# REGISTER ROUTERS
# =========================================================

app.include_router(
    auth.router
)

app.include_router(
    post.router
)

app.include_router(
    comment.router
)

app.include_router(
    like.router
)