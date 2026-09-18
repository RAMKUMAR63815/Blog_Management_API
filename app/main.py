from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .database import Base, engine

# Import models so SQLAlchemy knows all tables
from . import models

# Import routers
from .routers import auth
from .routers import post
from .routers import comment
from .routers import like
from .routers.subscription import router as subscription_router

# =========================================================
# CREATE DATABASE TABLES
# =========================================================

Base.metadata.create_all( #SQLAlchemy-kku "enna enna tables irukku, avanga columns enna" nu therinja information.Metadata-la irukkura tables database-la create pannunga.
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

app.add_middleware( #Frontend and backend different origins-la run aagumbodhu browser communication allow panna.
    CORSMiddleware,#Add this extra request/response processing
    allow_origins=["*"],#any orgin are allowed 
    allow_credentials=True,#Frontend-la irukkura login cookie/credentials-ai backend-ku send panna allow pannum.
    allow_methods=["*"],#all HTTP methods(GET,POST,PUT,DELETE)
    allow_headers=["*"] #HTTP request headers(Authorization: Bearer)
)
#mount - make this folder accessible/connect/attach through this URL path.

app.mount(
    "/media", #When a browser requests something starting with /media, use the media folder why its use means it not automattically allowed to access insode the file under media.
    StaticFiles(directory="media"),#StaticFiles does not upload the image.It only says: If a file already exists inside media, allow the browser/client to access it.”
    name="media" #internal name for this mounted route
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
app.include_router(subscription_router)