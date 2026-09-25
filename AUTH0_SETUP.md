# Auth0 Authentication Setup

## Features

- Email/password login
- Email/password signup
- Google login
- Facebook login
- Auth0 callback
- JWT authentication
- Automatic user creation for social login

## Auth0 Configuration

Allowed Callback URL:

http://127.0.0.1:8000/auth/callback

Allowed Web Origins:

http://127.0.0.1:8001

Application:

FastAPI Blog Management API

Connections:

- Google
- Facebook

## Local URLs

FastAPI: AUTH0_SETUP.md	
http://127.0.0.1:8000

Login:
http://127.0.0.1:8001/login/

Dashboard:
http://127.0.0.1:8001/dashboard/

## Testing

1. Open the login page.
2. Test email/password login.
3. Test signup.
4. Click Continue with Google.
5. Complete Google authentication.
6. Verify redirect to dashboard.
7. Click Continue with Facebook.
8. Complete Facebook authentication.
9. Verify redirect to dashboard.
10. Verify the user's provider and Auth0 ID in the database.