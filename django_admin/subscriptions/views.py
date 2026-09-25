from django.shortcuts import render
# Django HTML template-a browser-ku return panna use pannuvom
# Business Logic Like FastAPI routers


# =========================================================
# LOGIN PAGE
# =========================================================

def login_view(request):
    # Login HTML page-a browser-la display pannum
    # IMPORTANT:
    # Login page-ku automatic dashboard redirect
    # inga irukka koodathu.
    return render(
        request,
        "subscriptions/login.html"
    )
# =========================================================
# SIGNUP PAGE
# =========================================================

def signup_view(request):

    return render(
        request,
        "subscriptions/signup.html"
    )



# =========================================================
# DASHBOARD
# =========================================================

def dashboard(request):
    # Browser-la /dashboard/ request vandha,
    # indha function execute aagum.

    # User Dashboard HTML page-a render pannum
    return render(
        request,
        "subscriptions/dashboard.html"
    )


# =========================================================
# AUTH0 LOGIN SUCCESS
# =========================================================

def auth_success(request):

    # Auth0 login successful after callback.
    # Token is handled by auth_success.html JavaScript.
    return render(
        request,
        "subscriptions/auth_success.html"
    )