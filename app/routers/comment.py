from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    BackgroundTasks  # NEW: Runs email notification in background
)

from sqlalchemy.orm import Session
from ..models import Notification

from ..database import get_db
from ..models import Post, Comment
from ..schemas import CommentCreate, CommentResponse
from ..dependencies import get_current_user

# NEW:
# Notification functions are now handled by notification_service.py
from ..services.notification_service import send_comment_notification

from ..utils.subscription import check_comment_limit


router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)


@router.post(
    "/posts/{post_id}",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED
)
def add_comment(
    # add_comment() function user
    # /posts/{post_id}/comments API call pannumbodhu execute aagum.
    #
    # Function bracket-kulla irukkuradhu parameters.
    #
    # post_id URL-la irundhu varum,
    # comment_data request body-la irundhu varum,
    # db database session-a Depends(get_db) kudukkum,
    # current_user JWT token decode pannitu
    # login user information-a
    # Depends(get_current_user) kudukkum.
    #
    # This is called Dependency Injection in FastAPI.

    post_id: int,

    comment_data: CommentCreate,

    # NEW:
    # BackgroundTasks allows email notification
    # to execute after the API response
    background_tasks: BackgroundTasks,

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)
    # Reads JWT token
    # Decodes token
    # Finds user in DB
    # Returns User object
):
    post = db.query(Post).filter(
        Post.id == post_id
    ).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    # Check user's subscription comment limit
    current_comment_count = db.query(Comment).filter(
        Comment.user_id == current_user.id
    ).count()

    check_comment_limit(
        db=db,
        user=current_user,
        current_comment_count=current_comment_count
    )

    new_comment = Comment(
        post_id=post.id,
        user_id=current_user.id,
        text=comment_data.text
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    # Send email to post owner
    if post.author_id != current_user.id:
        # "Comment podra user-um Post owner-um same person-a
        # If different user means send notification"

        # ====================================================
        # NEW:
        # Add email notification to BackgroundTasks
        # ====================================================

        background_tasks.add_task(
            send_comment_notification,

            post_author_email=post.author.email,
            commenter_username=current_user.username,
            post_title=post.title,
            comment_text=comment_data.text
        )
    notification = Notification(
    user_id=post.author_id,
    message=f"{current_user.username} commented on your post",
    notification_type="comment"
)

    db.add(notification)
    db.commit()

        # IMPORTANT:
        # We are not directly calling:
        #
        # send_comment_notification(...)
        #
        # Instead we use:
        #
        # background_tasks.add_task(...)
        #
        # FastAPI schedules this function as a background task.
        #
        # The API does not need to wait for the SMTP
        # email operation before completing the request.

    return new_comment


@router.get(
    "/posts/{post_id}",
    response_model=list[CommentResponse]
)
def get_comments(
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

    comments = db.query(Comment).filter(
        Comment.post_id == post_id
    ).order_by(
        Comment.created_at.asc()
    ).all()

    return comments