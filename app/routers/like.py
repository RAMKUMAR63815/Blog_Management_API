from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Post, Like
from ..schemas import LikeResponse
from ..dependencies import get_current_user
from ..utils.email import send_like_notification

router = APIRouter(
    prefix="/likes",
    tags=["Likes"]
)

@router.post(
    "/posts/{post_id}",
    response_model=LikeResponse,
    status_code=status.HTTP_201_CREATED
)
def like_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    post = db.query(Post).filter(
        Post.id == post_id
    ).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    existing_like = db.query(Like).filter(
        Like.post_id == post_id,
        Like.user_id == current_user.id
    ).first()

    if existing_like:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already liked this post"
        )

    new_like = Like(
        post_id=post_id,
        user_id=current_user.id
    )

    db.add(new_like)
    db.commit()

    # Send email to post owner
    if post.author_id != current_user.id:
        send_like_notification(
            post_author_email=post.author.email,
            liker_username=current_user.username,
            post_title=post.title
        )

    return {
        "message": "Post liked successfully",
        "post_id": post_id
    }


@router.delete(
    "/posts/{post_id}",
    response_model=LikeResponse
)
def unlike_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    post = db.query(Post).filter(
        Post.id == post_id
    ).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    existing_like = db.query(Like).filter(
        Like.post_id == post_id,
        Like.user_id == current_user.id
    ).first()

    if existing_like is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have not liked this post"
        )

    db.delete(existing_like)
    db.commit()

    return {
        "message": "Post unliked successfully",
        "post_id": post_id
    }


@router.get("/posts/{post_id}/count")
def get_like_count(
    post_id: int,
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(
        Post.id == post_id
    ).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    count = db.query(Like).filter(
        Like.post_id == post_id
    ).count()

    return {
        "post_id": post_id,
        "like_count": count
    }