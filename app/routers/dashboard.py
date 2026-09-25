from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..database import get_db
from ..dependencies import get_current_user
from ..models import Post, Comment, Like


# =========================================================
# DASHBOARD ROUTER
# =========================================================

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


# =========================================================
# DASHBOARD STATISTICS
# =========================================================

@router.get("/")
def get_dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    # =====================================================
    # TOTAL POSTS
    # =====================================================

    total_posts = (
        db.query(Post)
        .filter(
            Post.author_id == current_user.id
        )
        .count()
    )


    # =====================================================
    # TOTAL COMMENTS MADE BY CURRENT USER
    # =====================================================

    total_comments = (
        db.query(Comment)
        .filter(
            Comment.user_id == current_user.id
        )
        .count()
    )


    # =====================================================
    # TOTAL LIKES RECEIVED ON CURRENT USER'S POSTS
    # =====================================================

    total_likes_received = (
        db.query(Like)
        .join(
            Post,
            Like.post_id == Post.id
        )
        .filter(
            Post.author_id == current_user.id
        )
        .count()
    )


    # =====================================================
    # LIKES PER POST
    # =====================================================

    likes_per_post = (
        db.query(
            Post.title,
            func.count(Like.id).label("likes")
        )
        .outerjoin(
            Like,
            Like.post_id == Post.id
        )
        .filter(
            Post.author_id == current_user.id
        )
        .group_by(
            Post.id
        )
        .all()
    )


    # =====================================================
    # COMMENTS PER POST
    # =====================================================

    comments_per_post = (
        db.query(
            Post.title,
            func.count(Comment.id).label("comments")
        )
        .outerjoin(
            Comment,
            Comment.post_id == Post.id
        )
        .filter(
            Post.author_id == current_user.id
        )
        .group_by(
            Post.id
        )
        .all()
    )


    # =====================================================
    # TOTAL VIEWS
    # =====================================================

    total_views = (
        db.query(
            func.sum(Post.views)
        )
        .filter(
            Post.author_id == current_user.id
        )
        .scalar()
        or 0
    )


    # =====================================================
    # JSON RESPONSE
    # =====================================================

    return {

        "total_posts": total_posts,

        "total_comments": total_comments,

        "total_likes_received": total_likes_received,

        "total_views": total_views,


        # =================================================
        # LIKES PER POST
        # =================================================

        "likes_per_post": [

            {
                "title": row.title,
                "likes": row.likes
            }

            for row in likes_per_post

        ],


        # =================================================
        # COMMENTS PER POST
        # =================================================

        "comments_per_post": [

            {
                "title": row.title,
                "comments": row.comments
            }

            for row in comments_per_post

        ]

    }


# =========================================================
# CHART DATA
# =========================================================

@router.get("/chart-data")
def get_chart_data(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    # =====================================================
    # LIKES PER POST
    # =====================================================

    likes_per_post = (
        db.query(
            Post.title,
            func.count(Like.id).label("likes")
        )
        .outerjoin(
            Like,
            Like.post_id == Post.id
        )
        .filter(
            Post.author_id == current_user.id
        )
        .group_by(
            Post.id
        )
        .all()
    )


    # =====================================================
    # COMMENTS PER POST
    # =====================================================

    comments_per_post = (
        db.query(
            Post.title,
            func.count(Comment.id).label("comments")
        )
        .outerjoin(
            Comment,
            Comment.post_id == Post.id
        )
        .filter(
            Post.author_id == current_user.id
        )
        .group_by(
            Post.id
        )
        .all()
    )


    # =====================================================
    # JSON RESPONSE
    # =====================================================

    return {

        "likes": [

            {
                "title": row.title,
                "count": row.likes
            }

            for row in likes_per_post

        ],

        "comments": [

            {
                "title": row.title,
                "count": row.comments
            }

            for row in comments_per_post

        ]

    }

#outer : returns both matching and non-matching rows from two tables

#Analytics Query: Dashboard statistics generate panna aggregation-based analytics queries use panninen

#Likes/comments per post should be shown graphically.

#So first backend-la Chart.js-ku required data prepare pannuvom.