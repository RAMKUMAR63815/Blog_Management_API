import os

from dotenv import load_dotenv
from authlib.integrations.starlette_client import OAuth


load_dotenv()


AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")


print("AUTH0_DOMAIN =", AUTH0_DOMAIN)
print("AUTH0_CLIENT_ID loaded =", bool(AUTH0_CLIENT_ID))
print("AUTH0_CLIENT_SECRET loaded =", bool(AUTH0_CLIENT_SECRET))


oauth = OAuth()


oauth.register(
    name="auth0",

    client_id=AUTH0_CLIENT_ID,

    client_secret=AUTH0_CLIENT_SECRET,

    authorize_url=f"https://{AUTH0_DOMAIN}/authorize",

    access_token_url=f"https://{AUTH0_DOMAIN}/oauth/token",

    api_base_url=f"https://{AUTH0_DOMAIN}/",

    userinfo_endpoint=f"https://{AUTH0_DOMAIN}/userinfo",

    jwks_uri=f"https://{AUTH0_DOMAIN}/.well-known/jwks.json",

    issuer=f"https://{AUTH0_DOMAIN}/",

    client_kwargs={
        "scope": "openid profile email"
    }
)