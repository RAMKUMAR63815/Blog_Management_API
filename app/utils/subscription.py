from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models import User


LIMIT_MESSAGE = (
    "You've reached your plan limit. "
    "Kindly upgrade your plan to continue."
)


def get_user_plan(db: Session, user: User):
    """
    Get the subscription plan of the current user.
    """

    if not user.subscription_plan:
        raise HTTPException(
            status_code=403,
            detail="No active subscription plan found."
        )

    return user.subscription_plan


def check_post_limit(
    db: Session,
    user: User,
    current_post_count: int
):
    """
    Check whether the user can create another post.
    """

    plan = get_user_plan(db, user)

    if plan.max_posts is not None:
        if current_post_count >= plan.max_posts:
            raise HTTPException(
                status_code=403,
                detail=LIMIT_MESSAGE
            )
def check_comment_limit(
    db: Session,
    user: User,
    current_comment_count: int
):
    """
    Check whether the user can create another comment.
    """

    plan = get_user_plan(db, user)

    if plan.max_comments is not None:
        if current_comment_count >= plan.max_comments:
            raise HTTPException(
                status_code=403,
                detail=LIMIT_MESSAGE
            )


def check_like_limit(
    db: Session,
    user: User,
    current_like_count: int
):
    """
    Check whether the user can create another like.
    """

    plan = get_user_plan(db, user)

    if plan.max_likes is not None:
        if current_like_count >= plan.max_likes:
            raise HTTPException(
                status_code=403,
                detail=LIMIT_MESSAGE
            )