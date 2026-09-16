from fastapi import Depends, HTTPException, status #-->Multiple API endpoints-ku common-ah thevai padra logic-a oru place-la store panra file.
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session #-->Python application-um database-um interact panna use panra working connection/session object for CRUD operation.

from .database import get_db
from .models import User
from .auth import decode_access_token


# =========================================================
# BEARER AUTHENTICATION
# =========================================================

security = HTTPBearer()#-->HTTPBearer() reads the Bearer token


# =========================================================
# GET CURRENT USER
# =========================================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db) #--> indha function-ku thevaiyana value-a nee automatically provide pannu
):

    token = credentials.credentials

    payload = decode_access_token(token)#>verify signature and expiry

    if payload is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    user_id = payload.get("sub")

    if user_id is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    try:
        user_id = int(user_id)

    except ValueError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID in token"
        )

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if user is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user