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
    current_user = Depends(get_current_user)
):
    notification = (
        db.query(Notification)
        .filter(
            Notification.id ==
            notification_id,
            Notification.user_id ==
            current_user.id
        )
        .first()
    )

    notification.is_read = True

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