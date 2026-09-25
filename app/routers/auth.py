from datetime import timedelta
import os

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse

from app.services.auth0_service import oauth

from ..database import get_db
from ..models import User
from ..schemas import (
    UserRegister,
    UserResponse,
    LoginRequest,
    TokenResponse
)
from ..auth import (
    hash_password,
    verify_password,
    create_access_token
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://127.0.0.1:8001"
)


# =========================================================
# REGISTER
# =========================================================

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):

    # Check username

    existing_username = db.query(User).filter(
        User.username == user_data.username
    ).first()

    if existing_username:

        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )


    # Check email

    existing_email = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if existing_email:

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )


    # Hash password

    hashed_password = hash_password(
        user_data.password
    )


    # Create user

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_password,
        provider="local"
    )


    db.add(new_user)

    db.commit()

    db.refresh(new_user)


    return new_user


# =========================================================
# SIGNUP
# =========================================================
# Requirement:
# /auth/signup/
#
# We keep /auth/register also working so existing
# functionality is not broken.

@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def signup(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):

    # Check username

    existing_username = db.query(User).filter(
        User.username == user_data.username
    ).first()

    if existing_username:

        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )


    # Check email

    existing_email = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if existing_email:

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )


    # Hash password

    hashed_password = hash_password(
        user_data.password
    )


    # Create local user

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_password,
        provider="local"
    )


    db.add(new_user)

    db.commit()

    db.refresh(new_user)


    return new_user


# =========================================================
# LOGIN
# =========================================================

@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):

    # IMPORTANT:
    # LoginRequest uses email.
    # Frontend must send "email", not "username".

    user = db.query(User).filter(
        User.email == login_data.email
    ).first()


    if user is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )


    # Local account must have a password.

    if not user.password:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=(
                "This account uses social login. "
                "Please continue with Google or Facebook."
            )
        )


    if not verify_password(
        login_data.password,
        user.password
    ):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )


    # Create application JWT

    access_token = create_access_token(

        data={
            "sub": str(user.id),
            "username": user.username,
            "user_id": user.id,
            "provider": user.provider
        },

        expires_delta=timedelta(hours=1)

    )


    return {

        "access_token": access_token,

        "token_type": "bearer"

    }


# =========================================================
# GOOGLE LOGIN
# =========================================================

@router.get(
    "/login/google"
)
async def google_login(
    request: Request
):

    redirect_uri = os.getenv(
        "AUTH0_CALLBACK_URL"
    )


    return await oauth.auth0.authorize_redirect(

        request,

        redirect_uri,

        connection="google-oauth2"

    )


# =========================================================
# FACEBOOK LOGIN
# =========================================================

@router.get(
    "/login/facebook"
)
async def facebook_login(
    request: Request
):

    redirect_uri = os.getenv(
        "AUTH0_CALLBACK_URL"
    )


    return await oauth.auth0.authorize_redirect(

        request,

        redirect_uri,

        connection="facebook"

    )


# =========================================================
# AUTH0 CALLBACK
# =========================================================

@router.get(
    "/callback"
)
async def auth0_callback(

    request: Request,

    db: Session = Depends(get_db)

):

    try:

        # =================================================
        # STEP 1
        # Exchange Auth0 authorization code for tokens
        # =================================================

        token = await oauth.auth0.authorize_access_token(
            request
        )


        # =================================================
        # STEP 2
        # Get Auth0 user information
        # =================================================

        userinfo = token.get(
            "userinfo"
        )


        if not userinfo:

            userinfo_response = await oauth.auth0.get(

                "userinfo",

                token=token

            )

            userinfo = userinfo_response.json()


        # =================================================
        # STEP 3
        # Read Auth0 user information
        # =================================================

        auth0_id = userinfo.get(
            "sub"
        )

        email = userinfo.get(
            "email"
        )

        name = (

            userinfo.get("name")

            or userinfo.get("nickname")

            or "Auth0 User"

        )


        if not auth0_id:

            raise HTTPException(

                status_code=400,

                detail="Auth0 user ID is missing"

            )


        if not email:

            raise HTTPException(

                status_code=400,

                detail="Email was not provided by Auth0"

            )


        # =================================================
        # STEP 4
        # Determine provider
        # =================================================

        if auth0_id.startswith(
            "google-oauth2|"
        ):

            provider = "google"


        elif auth0_id.startswith(
            "facebook|"
        ):

            provider = "facebook"


        else:

            provider = "auth0"


        # =================================================
        # STEP 5
        # Find user using Auth0 ID
        # =================================================

        user = db.query(User).filter(

            User.auth0_id == auth0_id

        ).first()


        # =================================================
        # STEP 6
        # If not found, find using email
        # =================================================

        if not user:

            user = db.query(User).filter(

                User.email == email

            ).first()


        # =================================================
        # STEP 7
        # Create user on first social login
        # =================================================

        if not user:

            username = (

                userinfo.get("nickname")

                or name

                or email.split("@")[0]

            )


            # Convert username to safe length.

            username = username[:50]


            base_username = username

            counter = 1


            while db.query(User).filter(

                User.username == username

            ).first():

                username = (
                    f"{base_username}{counter}"
                )[:50]

                counter += 1


            user = User(

                username=username,

                email=email,

                password=None,

                provider=provider,

                auth0_id=auth0_id

            )


            db.add(user)

            db.commit()

            db.refresh(user)


        else:

            # =================================================
            # Existing user
            # =================================================

            user.auth0_id = auth0_id

            user.provider = provider


            if not user.username:

                user.username = name[:50]


            db.commit()

            db.refresh(user)


        # =================================================
        # STEP 8
        # Create OUR application's JWT
        # =================================================

        access_token = create_access_token(

            data={

                "sub": str(user.id),

                "username": user.username,

                "user_id": user.id,

                "provider": user.provider

            },

            expires_delta=timedelta(hours=1)

        )


        # =================================================
        # STEP 9
        # Redirect to Django auth-success page
        # =================================================

        return RedirectResponse(

            url=(

                f"{FRONTEND_URL}"

                f"/login/auth-success/"

                f"?token={access_token}"

            )

        )


    except Exception as e:

        print(
            "Auth0 callback error:",
            str(e)
        )


        # =================================================
        # STEP 10
        # Redirect to Django login page when Auth0 fails
        # =================================================

        return RedirectResponse(

            url=(

                f"{FRONTEND_URL}"

                f"/login/"

                f"?error=authentication_failed"

            )

        )