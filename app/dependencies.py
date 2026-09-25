from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from .database import get_db
from .models import User
from .auth import decode_access_token


# =========================================================
# BEARER AUTHENTICATION
# =========================================================

security = HTTPBearer()
# HTTPBearer() reads the Bearer token from:
# Authorization: Bearer <token>


# =========================================================
# GET CURRENT USER
# =========================================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    # -----------------------------------------------------
    # GET TOKEN
    # -----------------------------------------------------

    token = credentials.credentials

    # -----------------------------------------------------
    # DECODE JWT
    # -----------------------------------------------------

    payload = decode_access_token(token)

    if payload is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    # -----------------------------------------------------
    # FIND USER
    # -----------------------------------------------------
    #
    # Your application has two possible token formats:
    #
    # Normal login:
    # {
    #     "sub": "6",
    #     ...
    # }
    #
    # Auth0/social login:
    # {
    #     "sub": "6",
    #     "user_id": 6,
    #     ...
    # }
    #
    # So first use user_id if it exists.
    # Otherwise use sub.
    # -----------------------------------------------------

    user_id = payload.get("user_id")

    if user_id is None:
        user_id = payload.get("sub")

    if user_id is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: user ID missing"
        )

    # -----------------------------------------------------
    # CONVERT USER ID TO INTEGER
    # -----------------------------------------------------

    try:

        user_id = int(user_id)

    except (ValueError, TypeError):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID in token"
        )

    # -----------------------------------------------------
    # FIND USER IN DATABASE
    # -----------------------------------------------------

    user = (
        db.query(User)
        .filter(
            User.id == user_id
        )
        .first()
    )

    if user is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    # -----------------------------------------------------
    # RETURN DATABASE USER
    # -----------------------------------------------------

    return user