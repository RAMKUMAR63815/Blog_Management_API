from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import get_current_user
from ..models import Notification
from ..schemas import NotificationResponse


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)

@router.get(
    "/",
    response_model=list[NotificationResponse]
)
def get_notifications(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return (
        db.query(Notification)
        .filter(
            Notification.user_id ==
            current_user.id
        )
        .order_by(
            Notification.created_at.desc()
        )
        .all()
    )


@router.put("/read/{notification_id}")
def mark_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Find the notification
    # AND make sure it belongs to the logged-in user
    notification = (
        db.query(Notification)
        .filter(
            Notification.id == notification_id,#and
            Notification.user_id == current_user.id
        )
        .first()
    )

    # If notification does not exist
    # or belongs to another user
    if notification is None:
        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )
        # Already read
    if notification.is_read:
        return {
            "message": "Notification already read"
        }

    # Change unread -> read
    notification.is_read = True

    # Save change to database
    db.commit()

    return {
        "message": "Notification marked as read"
    }


@router.put("/read-all")
def mark_all_read(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    notifications = (
        db.query(Notification)
        .filter(
            Notification.user_id ==
            current_user.id
        )
        .all()
    )

    for n in notifications:
        n.is_read = True

    db.commit()

    return {
        "message": "All notifications marked read"
    }