from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict


# =========================================================
# USER SCHEMAS
# =========================================================

class UserRegister(BaseModel):
    username: str = Field(
        ...,#-->REQUIRED FIELD
        min_length=3,
        max_length=50
    )

    email: EmailStr

    password: str = Field(
        ...,
        min_length=6,
        max_length=100
    )


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# LOGIN SCHEMA
# =========================================================

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


# =========================================================
# POST SCHEMAS
# =========================================================

class PostCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=3,
        max_length=200
    )

    content: str = Field(
        ...,
        min_length=10
    )
    image: str | None = None

class PostUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=3,
        max_length=200
    )

    content: str | None = Field(
        default=None,
        min_length=10
    )
    image: str | None = None


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    created_at: datetime
    image: str | None = None

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# COMMENT SCHEMAS
# =========================================================

class CommentCreate(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=1000
    )


class CommentResponse(BaseModel):
    id: int
    post_id: int
    user_id: int
    text: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# LIKE RESPONSE
# =========================================================

class LikeResponse(BaseModel):
    message: str
    post_id: int
#===========================================================
# NOTIFICATION SCHEMA
#===========================================================
class NotificationResponse(BaseModel):
    id: int
    message: str
    notification_type: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True