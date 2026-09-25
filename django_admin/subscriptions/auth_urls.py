from django.urls import path

from .views import (
    dashboard,
    auth_success,
    login_view,
    signup_view
)


urlpatterns = [

    # =========================================================
    # LOGIN
    # =========================================================

    path(
        "",
        login_view,
        name="login"
    ),


    # =========================================================
    # SIGNUP
    # =========================================================

    path(
        "signup/",
        signup_view,
        name="signup"
    ),


    # =========================================================
    # AUTH0 SUCCESS
    # =========================================================

    path(
        "auth-success/",
        auth_success,
        name="auth_success"
    ),

]