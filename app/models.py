from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    Boolean
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
        nullable=True
    )
    # Authentication provider
# local   -> normal email/password login
# google  -> Google login through Auth0
# facebook -> Facebook login through Auth0
    provider = Column(
    String(50),
    default="local",
    nullable=False
)

# Auth0 unique user identifier
# Example:
# google-oauth2|123456789
# facebook|123456789
    auth0_id = Column(
    String(255),
    unique=True,
    nullable=True,
    index=True
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
        # User -> Subscription Plan
    subscription_plan_id = Column(
        Integer,
        ForeignKey("subscription_plans.id"), #This is a many-users-to-one-plan relationship.
        nullable=True
    )

    subscription_plan = relationship(
        "SubscriptionPlan",
        back_populates="users"
    )
        # User -> Billing History
    billing_history = relationship(
        "BillingHistory",
        back_populates="user",
        cascade="all, delete-orphan"
    ) # User -> Notification 
    notifications = relationship(
    "Notification",
    back_populates="user",
    cascade="all, delete-orphan")

    # One user-ku many AI chat records irukkalam.
    ai_chat_logs = relationship(
    "AIChatLog",
    back_populates="user",
    cascade="all, delete-orphan"
)

# =========================================================
# SUBSCRIPTION PLAN MODEL
# =========================================================

class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(50),
        unique=True,
        nullable=False
    )

    price = Column(
        Integer,
        nullable=False,
        default=0
    )

    max_posts = Column(
        Integer,
        nullable=True
    )

    max_images = Column(
        Integer,
        nullable=True
    )

    max_comments = Column(
        Integer,
        nullable=True
    )

    max_likes = Column(
        Integer,
        nullable=True
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    # SubscriptionPlan -> Users
    users = relationship(
        "User",
        back_populates="subscription_plan"
    )

    # SubscriptionPlan -> Billing History
    billing_history = relationship(
        "BillingHistory",
        back_populates="plan"
    )
# =========================================================
# BILLING HISTORY MODEL    But after one month, you upgrade to Pro.If we only store the current plan, we lose the previous information.llingHistory lets us keep:
# =========================================================

class BillingHistory(Base):
    __tablename__ = "billing_history"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    plan_id = Column(
        Integer,
        ForeignKey("subscription_plans.id"),
        nullable=False
    )

    amount = Column(
        Integer,
        nullable=False
    )

    transaction_id = Column(
        String(100),
        unique=True,
        nullable=False
    )

    invoice_path = Column(
        String(255),
        nullable=True
    )

    start_date = Column(
        DateTime,
        nullable=False
    )

    end_date = Column(
        DateTime,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # BillingHistory -> User
    user = relationship(
        "User",
        back_populates="billing_history"
    )

    # BillingHistory -> SubscriptionPlan
    plan = relationship(
        "SubscriptionPlan",
        back_populates="billing_history"
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
        # Number of times this post was viewed
    views = Column(Integer, default=0, nullable=False)

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
class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    message = Column(String)

    notification_type = Column(String)

    is_read = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    user = relationship(
        "User",
        back_populates="notifications"
    )
    # ============================================================
# AI SUPPORT CHAT LOG
# ============================================================

class AIChatLog(Base):
    
    # Indha table user AI kitta ketta questions
    # and AI kudutha answers-ah save pannum.
    __tablename__ = "ai_chat_logs"

    # Each chat record-ku unique ID.
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    # Chat ketta user-oda ID.
    # users table-oda id-ku connect aagum.
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    # User AI kitta ketta question.
    question = Column(
        String,
        nullable=False
    )
    # AI kudutha answer.
    response = Column(
        String,
        nullable=False
    )
    # Question/answer create aana date and time.
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    # AI chat log belongs to one user.
    user = relationship(
        "User",
        back_populates="ai_chat_logs"
    )