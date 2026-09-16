from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    UniqueConstraint
)

from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base


# =========================================================
# USER MODEL
# =========================================================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    email = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    password = Column(
        String(255),
        nullable=False
    )

    # User -> Posts
    posts = relationship(
        "Post",
        back_populates="author",
        cascade="all, delete-orphan"
    )

    # User -> Comments
    comments = relationship(
        "Comment",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    # User -> Likes
    likes = relationship(
        "Like",
        back_populates="user",
        cascade="all, delete-orphan"
    )


# =========================================================
# POST MODEL
# =========================================================

class Post(Base):
    __tablename__ = "posts"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String(200),
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )

    image = Column (String(255), nullable=True)

    author_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Post -> User
    author = relationship(
        "User",
        back_populates="posts"
    )

    # Post -> Comments
    comments = relationship(
        "Comment",
        back_populates="post",
        cascade="all, delete-orphan"
    )

    # Post -> Likes
    likes = relationship(
        "Like",
        back_populates="post",
        cascade="all, delete-orphan"
    )


# =========================================================
# COMMENT MODEL
# =========================================================

class Comment(Base):
    __tablename__ = "comments"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    post_id = Column(
        Integer,
        ForeignKey("posts.id"),
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    text = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Comment -> Post
    post = relationship(
        "Post",
        back_populates="comments"
    )

    # Comment -> User
    user = relationship(
        "User",
        back_populates="comments"
    )


# =========================================================
# LIKE MODEL
# =========================================================

class Like(Base):
    __tablename__ = "likes"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    post_id = Column(
        Integer,
        ForeignKey("posts.id"),
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    # Prevent same user from liking same post multiple times
    __table_args__ = (
        UniqueConstraint(
            "post_id",
            "user_id",
            name="unique_post_user_like"
        ),
    )

    # Like -> Post
    post = relationship(
        "Post",
        back_populates="likes"
    )

    # Like -> User
    user = relationship(
        "User",
        back_populates="likes"
    )