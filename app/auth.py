from datetime import datetime, timedelta, timezone # file: Password Hashing & verification  jwt token Creation and verification

from jose import JWTError, jwt #Raised when token is Invalid Modified Expired jwt-token encode decode
from passlib.context import CryptContext #Used for password hashing.
# =========================================================
# JWT CONFIGURATION
# =========================================================

SECRET_KEY = "blog-management-secret-key-change-this" #>SECRET_KEY is used to digitally sign JWT tokens so they cannot be modified by clients

ALGORITHM = "HS256" #HS256 is the signing algorithm used to generate and verify JWT signatures

ACCESS_TOKEN_EXPIRE_MINUTES = 60


# =========================================================
# PASSWORD HASHING
# =========================================================

pwd_context = CryptContext( #Passlib object used for password hashing and verification.
    schemes=["bcrypt"], #using bcrypt alg  to pss hashing
    deprecated="auto" #Passlib manage hashing algorithms and upgrades (Future-la old hashing algorithm use pannina automatic-ah warning kudukkum.)
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)#hashing


def verify_password( #verify
    plain_password: str,
    hashed_password: str
) -> bool:

    return pwd_context.verify(
        plain_password,
        hashed_password
    )

 
# =========================================================
# CREATE JWT TOKEN
# =========================================================

def create_access_token(
    data: dict, #JWT-kulla store panna vendiya information sub:userid
    expires_delta: timedelta | None = None
):

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = (
            datetime.now(timezone.utc)
            + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )

    to_encode.update(
        {
            "exp": expire
        }
    )

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt # return JWT string


# =========================================================
# DECODE JWT TOKEN
# =========================================================

def decode_access_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:

        return None